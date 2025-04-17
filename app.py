import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import os
import re
import json
from datetime import date
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "5000"))

if not API_KEY:
    app.logger.error("Erro Crítico: Chave da API Gemini não encontrada no .env.")
    exit("API Key não configurada. Encerrando.")

app.logger.info(f"Servidor configurado para executar em: {API_HOST}:{API_PORT}")

genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")
app.logger.info(f"Inicializando modelo Gemini: {MODEL_NAME}")

try:
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    app.logger.info("Modelo Gemini inicializado com sucesso.")
except Exception as e:
    app.logger.error(f"Erro Crítico ao inicializar o modelo Gemini '{MODEL_NAME}': {e}")
    exit("Falha ao inicializar o modelo Gemini. Encerrando.")

def extract_video_id(url):
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def get_youtube_transcript(video_id):
    transcript_text = None
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages_to_try = ['pt', 'pt-BR', 'en']

        found_transcript = None
        transcript_type = "Nenhum"

        try:
            found_transcript = transcript_list.find_manually_created_transcript(languages_to_try)
            transcript_type = "Manual"
            app.logger.info(f"Legenda {transcript_type} encontrada (Idioma: {found_transcript.language_code}).")
        except NoTranscriptFound:
            app.logger.info("Legenda manual não encontrada nos idiomas preferenciais. Tentando legenda gerada...")
            try:
                found_transcript = transcript_list.find_generated_transcript(languages_to_try)
                transcript_type = "Gerada"
                app.logger.info(f"Legenda {transcript_type} encontrada (Idioma: {found_transcript.language_code}).")
            except NoTranscriptFound:
                app.logger.info("Nenhuma legenda (manual ou gerada) encontrada. Tentando qualquer idioma...")
                try:
                    available_langs = [t.language_code for t in transcript_list]
                    if not available_langs:
                        raise NoTranscriptFound("Nenhum idioma disponível.")
                    app.logger.info(f"Idiomas disponíveis: {available_langs}. Tentando o primeiro...")
                    found_transcript = transcript_list.find_transcript(available_langs)
                    transcript_type = "Disponível (Fallback)"
                    app.logger.info(f"Usando legenda {transcript_type} no idioma: {found_transcript.language_code}")
                except NoTranscriptFound:
                    return "Erro: Nenhuma legenda de qualquer tipo encontrada."

        if found_transcript:
            try:
                fetched_data = found_transcript.fetch()
                if isinstance(fetched_data, list) and fetched_data and isinstance(fetched_data[0], dict):
                    transcript_text = " ".join([entry['text'] for entry in fetched_data])
                elif fetched_data:
                     app.logger.warning(f"Formato inesperado da legenda {transcript_type}. Tentando str().")
                     transcript_text = str(fetched_data)
                else:
                     app.logger.warning("fetch() retornou dados vazios.")
                     transcript_text = ""

            except Exception as fetch_err:
                 app.logger.error(f"Erro ao processar dados da legenda {transcript_type}: {fetch_err}")
                 return f"Erro ao processar dados da legenda {transcript_type}: {fetch_err}"

        return transcript_text

    except TranscriptsDisabled:
        return "Erro: As legendas estão desativadas para este vídeo."
    except Exception as e:
        app.logger.error(f"Erro inesperado ao buscar transcrição: {e}\n{traceback.format_exc()}")
        return f"Erro inesperado ao buscar transcrição: {e}"

def analyze_video_with_gemini(transcript, video_url, video_title="Desconhecido", opcoes_analise=None):
    if isinstance(transcript, str) and transcript.startswith("Erro:"):
        return {"erro": transcript}

    if not transcript:
        return {"erro": "A transcrição está vazia ou não pôde ser obtida."}
    
    if opcoes_analise is None:
        opcoes_analise = {
            "extrairAcordes": True,
            "detectarInstrumentos": True,
            "analisarEstrutura": True,
            "extrairTablatura": True
        }
    
    instrucoes_extras = ""
    if opcoes_analise.get("extrairAcordes", True):
        instrucoes_extras += """
        4. Identifique TODOS os acordes mencionados na transcrição e adicione-os ao JSON:
           "acordesIdentificados": ["C", "Am", "F", "G", ...],
        """
    
    if opcoes_analise.get("detectarInstrumentos", True):
        instrucoes_extras += """
        5. Identifique TODOS os instrumentos mencionados na transcrição e adicione-os ao JSON:
           "instrumentosIdentificados": ["Violão", "Guitarra", "Baixo", ...],
        """
    
    if opcoes_analise.get("analisarEstrutura", True):
        instrucoes_extras += """
        6. Analise a estrutura musical mencionada no vídeo:
           "estruturaMusical": {
              "partes": ["Intro", "Verso", "Refrão", ...],
              "progressao": "Descreva a progressão harmônica mencionada",
              "tonalidade": "Mencione a tonalidade da música, se identificada"
           },
        """
    
    if opcoes_analise.get("extrairTablatura", True):
        instrucoes_extras += """
        7. Se houver menção a tablatura, adicione ao JSON:
           "tablatura": {
              "presente": true/false,
              "observacoes": "Descrição sobre a tablatura mencionada no vídeo"
           },
        """

    prompt = f"""
    Você é um especialista em pedagogia musical e análise de conteúdo de vídeo.
    Sua tarefa é avaliar um vídeo tutorial de música do YouTube com base em sua transcrição.

    Vídeo URL: {video_url}
    Título: {video_title}
    Transcrição do Vídeo:
    --- START TRANSCRIPT ---
    {transcript}
    --- END TRANSCRIPT ---

    Por favor, avalie o vídeo e retorne sua análise no formato JSON abaixo, preenchendo os campos `pontuacao` (1 a 5) e `observacoes`:

    {{
      "avaliacaoVideo": "{video_title}",
      "urlVideo": "{video_url}",
      "dataAvaliacao": "{date.today().isoformat()}",
      "avaliador": "Gemini API ({MODEL_NAME})",
      "pontosAvaliacao": {{
        "didaticaExplicacao": {{
          "pontuacao": null,
          "observacoes": "Avalie: Clareza na explicação das partes da música, estrutura do ensino (segmentação, introdução, prática lenta, conclusão), uso de exemplos, ritmo da aula, se facilita o aprendizado."
        }},
        "linguagemUtilizada": {{
          "pontuacao": null,
          "observacoes": "Avalie: Clareza da linguagem (evita jargões excessivos sem explicação?), objetividade, tom de voz (perceptível pela transcrição - ex: encorajador, monótono), adequação ao público alvo implícito, dicção (inferida pela clareza do texto)."
        }},
        "adequacaoNivel": {{
          "nivelEstimadoVideo": "Descreva o nível estimado (Ex: Iniciante, Intermediário, Avançado) com base na complexidade do conteúdo.",
          "complexidadeAcordes": {{
            "tipos": "Liste os tipos de acordes mencionados ou implícitos (Ex: Naturais, Com Pestana, Suspensos, etc.). Se não houver acordes (ex: baixo/solo), mencione isso.",
            "contagemAproximada": "Estime a quantidade (Ex: Poucos (1-4), Moderado (5-10), Muitos (10+), N/A)."
          }},
          "complexidadeTecnica": "Liste as técnicas principais ensinadas (Ex: Ritmo simples, Batidas complexas, Dedilhado, Tapping, Pizzicato, Palhetada, etc.).",
          "pontuacao": null,
          "observacoes": "Avalie se a complexidade (acordes, técnicas) ensinada e a didática utilizada são apropriadas para o nível estimado do vídeo. A dificuldade está bem balanceada com a forma de ensinar?"
        }}
      }},
      "pontuacaoGeral": null,
      "comentariosGerais": "Forneça um breve resumo geral da qualidade do vídeo como tutorial."
      {instrucoes_extras}
    }}

    Instruções importantes:
    1. Preencha TODOS os campos `pontuacao` com um número inteiro entre 1 e 5.
    2. Preencha TODOS os campos descritivos com texto relevante e específico para a transcrição fornecida.
    3. Retorne APENAS o objeto JSON completo, sem explicações adicionais.
    """
    
    response = None
    try:
        response = model.generate_content(prompt)

        if hasattr(response, 'text'):
            json_text = response.text.strip()
            start_index = json_text.find('{')
            end_index = json_text.rfind('}')
            if start_index != -1 and end_index != -1 and end_index > start_index:
                json_text = json_text[start_index:end_index+1]
            else:
                if json_text.startswith("```json"): json_text = json_text[7:]
                if json_text.endswith("```"): json_text = json_text[:-3]
                json_text = json_text.strip()

            analysis_result = json.loads(json_text)
            return analysis_result
        else:
            app.logger.error(f"A resposta da API Gemini não contém texto. Resposta: {response}")
            error_msg = "Resposta inválida da API Gemini."
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                error_msg += f" Feedback: {response.prompt_feedback}"
            return {"erro": error_msg}

    except json.JSONDecodeError as e:
        app.logger.error(f"Erro ao decodificar JSON da resposta do Gemini: {e}")
        raw_text = response.text if (response and hasattr(response, 'text')) else "N/A"
        app.logger.error(f"Resposta Bruta: {raw_text}")
        return {"erro": "Falha ao decodificar a resposta JSON da API Gemini.", "resposta_bruta_ver_logs": True}
    except Exception as e:
        app.logger.error(f"Erro durante a chamada da API Gemini: {e}\n{traceback.format_exc()}")
        feedback = "N/A"
        if response and hasattr(response, 'prompt_feedback'):
             feedback = response.prompt_feedback
        app.logger.error(f"Detalhes do feedback: {feedback}")
        return {"erro": f"Erro ao chamar a API Gemini: {e}"}

@app.route('/analyze', methods=['POST'])
def analyze_video_endpoint():
    app.logger.info("Recebida requisição POST em /analyze")

    data = request.get_json()
    if not data or 'url' not in data:
        app.logger.warning("Requisição inválida: JSON ausente ou sem chave 'url'.")
        return jsonify({"erro": "JSON inválido ou chave 'url' ausente."}), 400

    video_url = data['url']
    app.logger.info(f"URL recebida: {video_url}")
    
    opcoes_analise = data.get('optionsAnalise', None)
    if opcoes_analise:
        app.logger.info(f"Opções de análise recebidas: {opcoes_analise}")

    video_id = extract_video_id(video_url)
    if not video_id:
        app.logger.warning(f"URL inválida ou ID não extraído: {video_url}")
        return jsonify({"erro": "URL do YouTube inválida ou não foi possível extrair o ID."}), 400
    app.logger.info(f"ID do vídeo extraído: {video_id}")

    video_title = f"Vídeo ID {video_id}"

    app.logger.info("Buscando transcrição...")
    transcript = get_youtube_transcript(video_id)

    if isinstance(transcript, str) and transcript.startswith("Erro:"):
        app.logger.error(f"Erro ao obter transcrição para ID {video_id}: {transcript}")
        status_code = 404 if "desativadas" in transcript or "não encontrada" in transcript else 500
        return jsonify({"erro": transcript}), status_code
    elif not transcript:
         app.logger.warning(f"Transcrição vazia retornada para ID {video_id}")
         return jsonify({"erro": "Transcrição não encontrada ou vazia."}), 404

    app.logger.info(f"Transcrição obtida para ID {video_id} (trecho): {transcript[:100]}...")

    app.logger.info("Enviando para análise do Gemini...")
    analysis_result = analyze_video_with_gemini(transcript, video_url, video_title, opcoes_analise)

    if "erro" in analysis_result:
        app.logger.error(f"Erro na análise do Gemini para ID {video_id}: {analysis_result['erro']}")
        return jsonify(analysis_result), 500
    else:
        app.logger.info(f"Análise concluída com sucesso para ID {video_id}.")
        return jsonify(analysis_result), 200
    
@app.route('/')
def index():
    app.logger.info(f"Servindo index.html. API host/port: {API_HOST}:{API_PORT}")
    
    try:
         return render_template('index.html', api_host=API_HOST, api_port=API_PORT)
    except Exception as e:
         app.logger.error(f"Erro ao renderizar template 'index.html': {e}")
         return "Erro interno: Não foi possível encontrar o template da página.", 500
    
if __name__ == '__main__':
    app.run(debug=True, host=API_HOST, port=API_PORT)
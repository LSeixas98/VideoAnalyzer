[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Portuguese](https://img.shields.io/badge/Idioma-Português-green.svg)](README.pt-br.md)

# Analisador de Vídeo Tutorial de Música

Uma aplicação web que utiliza IA para analisar vídeos tutoriais de música do YouTube, fornecendo insights sobre a qualidade didática e conteúdo musical através da transcrição.

![GitHub](https://img.shields.io/github/license/LSeixas98/VideoAnalyzer)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.2.3-green)

## 📋 Descrição

Esta aplicação permite que professores, estudantes e criadores de conteúdo musical possam analisar a qualidade pedagógica e a estrutura musical de tutoriais em vídeo no YouTube. O sistema:

- Extrai automaticamente a transcrição do vídeo
- Utiliza o Google Gemini 1.5 Flash para análise avançada
- Avalia a didática, linguagem e adequação do nível
- Identifica instrumentos, acordes e estrutura musical
- Fornece pontuações e feedback detalhado

## 🚀 Funcionalidades

- **Análise personalizada:** Selecione quais aspectos deseja analisar (acordes, instrumentos, estrutura musical, tablatura)
- **Suporte multilíngue:** Transcrições em português, inglês e outros idiomas
- **Interface intuitiva:** Design responsivo para uso em qualquer dispositivo
- **Visualização em tabela:** Veja os resultados em formato tabular estruturado
- **Visualização JSON:** Alternativa mais técnica com dados expansíveis/retráteis
- **Análise detalhada:** Saída estruturada para fácil interpretação e integração com outros sistemas

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Chave de API do Google Gemini (veja as instruções de configuração)
- Conexão com a Internet

## ⚙️ Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/LSeixas98/VideoAnalyzer.git
   cd VideoAnalyzer
   ```

2. **Instale as dependências:**
   ```bash
   # Método recomendado: usar ambiente virtual
   python -m venv venv
   
   # Ativar o ambiente virtual
   # No Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # No Windows CMD:
   venv\Scripts\activate.bat
   # No Linux/macOS:
   source venv/bin/activate
   
   # Instalar as dependências no ambiente virtual
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```
   # Configuração da API Gemini
   GEMINI_API_KEY=sua_chave_api_aqui
   GEMINI_MODEL=gemini-1.5-flash-latest

   # Configuração do servidor
   API_HOST=127.0.0.1
   API_PORT=5000
   ```

   Para uso em rede local, atualize o `API_HOST` com o IP da sua máquina:
   ```
   API_HOST=192.168.1.100  # Substitua pelo seu IP na rede local
   ```

## 🔧 Uso

1. **Inicie o servidor:**
   ```bash
   python app.py
   ```

2. **Acesse a aplicação:**
   Abra um navegador e acesse:
   ```
   http://localhost:5000  # Para acesso local
   # OU
   http://192.168.1.100:5000  # Para acesso na rede local (substitua pelo seu IP)
   ```

3. **Utilize a aplicação:**
   - Cole a URL do YouTube no campo de entrada
   - Selecione as opções de análise desejadas
   - Clique em "Analisar"
   - Aguarde o processamento (pode levar alguns instantes)
   - Alterne entre as visualizações de tabela e JSON para ver os resultados

## 🔧 Solução de Problemas

### Problemas com Permissões do pip no Windows

Se você encontrar erros de permissão como `[WinError 5] Acesso negado` ao instalar pacotes com pip, tente as seguintes soluções:

1. **Utilize ambientes virtuais** (recomendado):
   ```bash
   # Navegue até o diretório do projeto
   cd caminho/para/VideoAnalyzer
   
   # Crie um ambiente virtual
   python -m venv .venv
   
   # Ative o ambiente virtual
   # No PowerShell:
   .\.venv\Scripts\Activate.ps1
   # No CMD:
   .\.venv\Scripts\activate.bat
   
   # Instale as dependências no ambiente virtual
   python -m pip install -r requirements.txt
   ```

2. **Execute como administrador**:
   Se preferir instalar globalmente, execute o prompt de comando ou PowerShell como administrador.

3. **Instale apenas para o usuário atual**:
   ```bash
   pip install -r requirements.txt --user
   ```

### Módulos não encontrados

Se receber o erro `ModuleNotFoundError: No module named 'google'` ou similar:

1. Verifique se está usando o ambiente virtual correto (caso tenha criado um)
2. Confirme que todas as dependências foram instaladas:
   ```bash
   pip list
   ```
3. Reinstale as dependências específicas:
   ```bash
   pip install google-generativeai youtube-transcript-api
   ```

## 📂 Estrutura do Projeto

```
analisador-video-musical/
│
├── app.py                # Aplicação principal
├── requirements.txt      # Dependências do projeto
├── .env                  # Arquivo de configuração (não incluído no repositório)
├── README.md             # Este arquivo
├── LICENSE               # Licença do projeto
│
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── styles.css    # Estilos da aplicação
│   │
│   └── js/
│       └── script.js     # JavaScript da aplicação
│
└── templates/            # Templates HTML
    └── index.html        # Interface principal
```

## 🧩 Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **API de Legendas:** YouTube Transcript API
- **IA:** Google Gemini 1.5 Flash
- **Formatação de Dados:** JSON
- **Configuração:** python-dotenv

## ✅ Exemplo de Resposta

A API retorna um JSON estruturado com a análise detalhada do vídeo, por exemplo:

```json
{
  "avaliacaoVideo": "Vídeo ID xyzABC123",
  "urlVideo": "https://www.youtube.com/watch?v=xyzABC123",
  "dataAvaliacao": "2025-04-16",
  "avaliador": "Gemini API (gemini-1.5-flash-latest)",
  "pontosAvaliacao": {
    "didaticaExplicacao": {
      "pontuacao": 4,
      "observacoes": "Explicação clara e bem estruturada..."
    },
    "linguagemUtilizada": {
      "pontuacao": 5,
      "observacoes": "Linguagem acessível e adequada ao público..."
    },
    "adequacaoNivel": {
      "nivelEstimadoVideo": "Intermediário",
      "complexidadeAcordes": {
        "tipos": "Naturais, Com Pestana, Suspensos",
        "contagemAproximada": "Moderado (5-10)"
      },
      "complexidadeTecnica": "Dedilhado, Palhetada alternada",
      "pontuacao": 4,
      "observacoes": "Conteúdo bem balanceado para o nível proposto..."
    }
  },
  "pontuacaoGeral": 4,
  "comentariosGerais": "Excelente tutorial com boa didática...",
  "acordesIdentificados": ["C", "Am", "F", "G7"],
  "instrumentosIdentificados": ["Violão", "Guitarra"],
  "estruturaMusical": {
    "partes": ["Intro", "Verso", "Refrão"],
    "progressao": "I-vi-IV-V em Dó Maior",
    "tonalidade": "Dó Maior"
  },
  "tablatura": {
    "presente": true,
    "observacoes": "Tablatura para introdução mostrada aos 2:45"
  }
}
```

## 👨‍💻 Desenvolvimento

### Configuração do Ambiente

#### Arquivo .env
O arquivo `.env` permite configurar a aplicação para diferentes ambientes:

- **Desenvolvimento local:** Use `API_HOST=127.0.0.1`
- **Rede local:** Use `API_HOST=` com o IP da sua máquina na rede
- **Produção:** Use `API_HOST=0.0.0.0` para escutar em todas as interfaces

#### Encontrar seu IP na rede local:
- **Windows:** Use o comando `ipconfig` no Prompt de Comando
- **Linux:** Use `ip addr show` ou `ifconfig` no Terminal
- **macOS:** Use `ifconfig | grep inet` no Terminal

### Adicionar Novas Funcionalidades

Para adicionar novos critérios de análise:

1. Adicione os novos checkboxes no `index.html`
2. Atualize o objeto `optionsAnalise` no JavaScript
3. Modifique a função `analyze_video_with_gemini` em `app.py` para incluir os novos parâmetros no prompt do Gemini
4. Atualize o esquema JSON de saída

## 🛣️ Roadmap

Funcionalidades planejadas para futuras versões:

- [ ] Análise de progressões harmônicas complexas
- [ ] Suporte para vídeos sem legendas (análise de áudio)
- [ ] Exportação de relatório em PDF
- [ ] Comparação entre múltiplos vídeos
- [ ] Interface de usuário aprimorada
- [ ] API pública para integração com outras aplicações

## 📝 Limitações Conhecidas

- Depende da disponibilidade de legendas/transcrições no vídeo do YouTube
- A qualidade da análise depende da clareza da transcrição
- A API Gemini tem limites de tokens que podem afetar vídeos muito longos
- Algumas legendas automáticas podem conter erros que afetam a análise

## 🔒 Segurança

- Mantenha sua chave API Gemini segura no arquivo `.env`
- Adicione `.env` ao seu arquivo `.gitignore` para não compartilhar suas credenciais
- Em ambientes de produção, restrinja o CORS para domínios específicos
- Para maior segurança, considere usar variáveis de ambiente do sistema em vez do arquivo `.env`

## 🧪 Testes

Para executar os testes automatizados:

```bash
# Ainda não implementado
# pytest tests/
```

## 📚 Como Citar

Se você utilizar este projeto em pesquisas ou trabalhos acadêmicos, por favor cite como:

```
Seixas, L. (2025). VideoAnalyzer: Uma ferramenta de análise de tutoriais de música em vídeo. 
GitHub: https://github.com/LSeixas98/VideoAnalyzer
```

## 👏 Créditos

Este projeto utiliza as seguintes tecnologias e bibliotecas:

- [Flask](https://flask.palletsprojects.com/)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [Google Gemini API](https://ai.google.dev/gemini-api)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

---

Desenvolvido com ❤️ para a comunidade musical

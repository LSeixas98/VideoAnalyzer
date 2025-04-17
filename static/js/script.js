const statusDiv = document.getElementById("status");
const resultSection = document.getElementById("result-section");
const urlInput = document.getElementById("videoUrl");
const resultTableContainer = document.getElementById("resultTableContainer");
const collapsibleJsonContainer = document.getElementById("collapsibleJson");

urlInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    analyzeVideo();
  }
});

function openTab(evt, tabName) {
  const tabContents = document.getElementsByClassName("tab-content");
  for (let i = 0; i < tabContents.length; i++) {
    tabContents[i].classList.remove("active");
  }

  const tabButtons = document.getElementsByClassName("tab-button");
  for (let i = 0; i < tabButtons.length; i++) {
    tabButtons[i].classList.remove("active");
  }

  document.getElementById(tabName).classList.add("active");
  evt.currentTarget.classList.add("active");
}

async function analyzeVideo() {
  const videoUrl = urlInput.value;
  if (!videoUrl) {
    showStatus("Por favor, insira um link do YouTube válido.", "error");
    hideResultSection();
    return;
  }

  if (!isValidYouTubeUrl(videoUrl)) {
    showStatus(
      "O URL inserido não parece ser um link válido do YouTube.",
      "error"
    );
    hideResultSection();
    return;
  }

  showStatus(
    "Analisando vídeo... Por favor, aguarde. Este processo pode levar alguns minutos.",
    "loading"
  );
  hideResultSection();

  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: videoUrl,
        optionsAnalise: {
          extrairAcordes: document.getElementById("extractChords").checked,
          detectarInstrumentos:
            document.getElementById("detectInstruments").checked,
          analisarEstrutura:
            document.getElementById("analyzeStructure").checked,
          extrairTablatura: document.getElementById("extractTab").checked,
        },
      }),
    });

    const data = await response.json();

    if (response.ok) {
      showStatus("Análise concluída com sucesso!", "success");
      renderTable(data);
      renderCollapsibleJson(data);
      showResultSection();
    } else {
      showStatus(
        `Erro na análise: ${data.erro || "Erro desconhecido"}`,
        "error"
      );
      hideResultSection();
    }
  } catch (error) {
    console.error("Erro na requisição:", error);
    showStatus(
      `Erro ao conectar com a API. Verifique se ela está rodando e o IP está correto. Detalhe: ${error.message}`,
      "error"
    );
    hideResultSection();
  }
}

function renderTable(data) {
  let tableHtml = '<table class="results-table">';

  // Informações básicas
  tableHtml += `
        <tr>
            <th colspan="2">Informações Gerais</th>
        </tr>
        <tr>
            <td>Vídeo</td>
            <td>${data.avaliacaoVideo || "N/A"}</td>
        </tr>
        <tr>
            <td>URL</td>
            <td><a href="${data.urlVideo}" target="_blank">${
    data.urlVideo
  }</a></td>
        </tr>
        <tr>
            <td>Data</td>
            <td>${data.dataAvaliacao || "N/A"}</td>
        </tr>
        <tr>
            <td>Pontuação Geral</td>
            <td><strong>${data.pontuacaoGeral || "N/A"}</strong>/5</td>
        </tr>
        <tr>
            <td>Comentário Geral</td>
            <td>${data.comentariosGerais || "N/A"}</td>
        </tr>
    `;

  // Pontos de Avaliação - Didática
  if (data.pontosAvaliacao && data.pontosAvaliacao.didaticaExplicacao) {
    const didatica = data.pontosAvaliacao.didaticaExplicacao;
    tableHtml += `
            <tr class="section-title">
                <td colspan="2">Didática da Explicação</td>
            </tr>
            <tr>
                <td>Pontuação</td>
                <td><strong>${didatica.pontuacao || "N/A"}</strong>/5</td>
            </tr>
            <tr>
                <td>Observações</td>
                <td>${didatica.observacoes || "N/A"}</td>
            </tr>
        `;
  }

  // Pontos de Avaliação - Linguagem
  if (data.pontosAvaliacao && data.pontosAvaliacao.linguagemUtilizada) {
    const linguagem = data.pontosAvaliacao.linguagemUtilizada;
    tableHtml += `
            <tr class="section-title">
                <td colspan="2">Linguagem Utilizada</td>
            </tr>
            <tr>
                <td>Pontuação</td>
                <td><strong>${linguagem.pontuacao || "N/A"}</strong>/5</td>
            </tr>
            <tr>
                <td>Observações</td>
                <td>${linguagem.observacoes || "N/A"}</td>
            </tr>
        `;
  }

  // Pontos de Avaliação - Adequação de Nível
  if (data.pontosAvaliacao && data.pontosAvaliacao.adequacaoNivel) {
    const adequacao = data.pontosAvaliacao.adequacaoNivel;
    tableHtml += `
            <tr class="section-title">
                <td colspan="2">Adequação de Nível</td>
            </tr>
            <tr>
                <td>Nível Estimado</td>
                <td>${adequacao.nivelEstimadoVideo || "N/A"}</td>
            </tr>
            <tr>
                <td>Pontuação</td>
                <td><strong>${adequacao.pontuacao || "N/A"}</strong>/5</td>
            </tr>
            <tr>
                <td>Observações</td>
                <td>${adequacao.observacoes || "N/A"}</td>
            </tr>
        `;

    // Complexidade dos Acordes
    if (adequacao.complexidadeAcordes) {
      tableHtml += `
                <tr>
                    <td class="subsection">Tipos de Acordes</td>
                    <td>${adequacao.complexidadeAcordes.tipos || "N/A"}</td>
                </tr>
                <tr>
                    <td class="subsection">Quantidade</td>
                    <td>${
                      adequacao.complexidadeAcordes.contagemAproximada || "N/A"
                    }</td>
                </tr>
            `;
    }

    // Complexidade Técnica
    tableHtml += `
            <tr>
                <td class="subsection">Técnicas Ensinadas</td>
                <td>${adequacao.complexidadeTecnica || "N/A"}</td>
            </tr>
        `;
  }

  // Acordes Identificados
  if (data.acordesIdentificados && data.acordesIdentificados.length > 0) {
    tableHtml += `
            <tr class="section-title">
                <td colspan="2">Acordes Identificados</td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="list-display">
                        ${data.acordesIdentificados
                          .map(
                            (acorde) =>
                              `<span class="tag-item">${acorde}</span>`
                          )
                          .join("")}
                    </div>
                </td>
            </tr>
        `;
  }

  // Instrumentos Identificados
  if (
    data.instrumentosIdentificados &&
    data.instrumentosIdentificados.length > 0
  ) {
    tableHtml += `
            <tr class="section-title">
                <td colspan="2">Instrumentos Identificados</td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="list-display">
                        ${data.instrumentosIdentificados
                          .map(
                            (instrumento) =>
                              `<span class="tag-item">${instrumento}</span>`
                          )
                          .join("")}
                    </div>
                </td>
            </tr>
        `;
  }

  // Estrutura Musical
  if (data.estruturaMusical) {
    tableHtml += `
            <tr class="section-title">
                <td colspan="2">Estrutura Musical</td>
            </tr>
        `;

    if (
      data.estruturaMusical.partes &&
      data.estruturaMusical.partes.length > 0
    ) {
      tableHtml += `
                <tr>
                    <td>Partes</td>
                    <td>
                        <div class="list-display">
                            ${data.estruturaMusical.partes
                              .map(
                                (parte) =>
                                  `<span class="tag-item">${parte}</span>`
                              )
                              .join("")}
                        </div>
                    </td>
                </tr>
            `;
    }

    if (data.estruturaMusical.progressao) {
      tableHtml += `
                <tr>
                    <td>Progressão</td>
                    <td>${data.estruturaMusical.progressao}</td>
                </tr>
            `;
    }

    if (data.estruturaMusical.tonalidade) {
      tableHtml += `
                <tr>
                    <td>Tonalidade</td>
                    <td>${data.estruturaMusical.tonalidade}</td>
                </tr>
            `;
    }
  }

  // Tablatura
  if (data.tablatura) {
    tableHtml += `
            <tr class="section-title">
                <td colspan="2">Tablatura</td>
            </tr>
            <tr>
                <td>Presente</td>
                <td>${data.tablatura.presente ? "Sim" : "Não"}</td>
            </tr>
        `;

    if (data.tablatura.observacoes) {
      tableHtml += `
                <tr>
                    <td>Observações</td>
                    <td>${data.tablatura.observacoes}</td>
                </tr>
            `;
    }
  }

  tableHtml += "</table>";
  resultTableContainer.innerHTML = tableHtml;
}

function renderCollapsibleJson(data) {
  let sections = [];

  sections.push({
    title: "Informações Gerais",
    content: {
      avaliacaoVideo: data.avaliacaoVideo,
      urlVideo: data.urlVideo,
      dataAvaliacao: data.dataAvaliacao,
      avaliador: data.avaliador,
      pontuacaoGeral: data.pontuacaoGeral,
      comentariosGerais: data.comentariosGerais,
    },
  });

  if (data.pontosAvaliacao) {
    sections.push({
      title: "Pontos de Avaliação",
      content: data.pontosAvaliacao,
    });
  }

  if (data.acordesIdentificados) {
    sections.push({
      title: "Acordes Identificados",
      content: {
        acordes: data.acordesIdentificados,
      },
    });
  }

  if (data.instrumentosIdentificados) {
    sections.push({
      title: "Instrumentos Identificados",
      content: {
        instrumentos: data.instrumentosIdentificados,
      },
    });
  }

  if (data.estruturaMusical) {
    sections.push({
      title: "Estrutura Musical",
      content: data.estruturaMusical,
    });
  }

  if (data.tablatura) {
    sections.push({
      title: "Tablatura",
      content: data.tablatura,
    });
  }

  let collapsibleHtml = "";
  sections.forEach((section) => {
    collapsibleHtml += `
            <button class="collapsible">${section.title}</button>
            <div class="content-panel">
                <pre>${JSON.stringify(section.content, null, 2)}</pre>
            </div>
        `;
  });

  collapsibleHtml += `
        <div class="json-full-container">
            <h3>JSON Completo</h3>
            <button id="btnCopyJson" onclick="copyJsonToClipboard()" class="copy-button">Copiar JSON</button>
            <pre id="fullJsonDisplay" class="full-json">${JSON.stringify(
              data,
              null,
              2
            )}</pre>
        </div>
    `;

  window.completeJsonData = JSON.stringify(data, null, 2);
  collapsibleJsonContainer.innerHTML = collapsibleHtml;

  const collapsibles = document.getElementsByClassName("collapsible");
  for (let i = 0; i < collapsibles.length; i++) {
    collapsibles[i].addEventListener("click", function () {
      this.classList.toggle("active");
      const contentPanel = this.nextElementSibling;
      if (contentPanel.style.maxHeight) {
        contentPanel.style.maxHeight = null;
      } else {
        contentPanel.style.maxHeight = contentPanel.scrollHeight + "px";
      }
    });
  }
}

function copyJsonToClipboard() {
  navigator.clipboard
    .writeText(window.completeJsonData)
    .then(() => {
      const copyButton = document.getElementById("btnCopyJson");
      const originalText = copyButton.textContent;
      copyButton.textContent = "Copiado!";
      copyButton.classList.add("copied");

      setTimeout(() => {
        copyButton.textContent = originalText;
        copyButton.classList.remove("copied");
      }, 2000);
    })
    .catch((err) => {
      console.error("Erro ao copiar: ", err);
      alert(
        "Não foi possível copiar o texto. Por favor, tente selecionar e copiar manualmente."
      );
    });
}

function toggleAllSections(expand) {
  const collapsibles = document.getElementsByClassName("collapsible");
  const contentPanels = document.getElementsByClassName("content-panel");

  for (let i = 0; i < collapsibles.length; i++) {
    if (expand) {
      collapsibles[i].classList.add("active");
      contentPanels[i].style.maxHeight = contentPanels[i].scrollHeight + "px";
    } else {
      collapsibles[i].classList.remove("active");
      contentPanels[i].style.maxHeight = null;
    }
  }
}

function showStatus(message, type) {
  statusDiv.textContent = message;
  statusDiv.className = type;
  statusDiv.style.display = "block";
}

function hideResultSection() {
  resultSection.style.display = "none";
}

function showResultSection() {
  resultSection.style.display = "block";
}

function isValidYouTubeUrl(url) {
  const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
  return pattern.test(url);
}

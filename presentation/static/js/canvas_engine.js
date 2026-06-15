"use strict";

// ═══════════════════════════════════════════════════════════════════
//  grapy-wiki — Canvas Engine
//  Fase 1 — Motor de Física Force-Directed
//  - Repulsão: Lei de Coulomb
//  - Atração:  Lei de Hooke (molas)
//  - Atrito:   fator de dissipação de energia por frame
//  - Dormência: zera velocidades abaixo do threshold de energia
//  Zero dependências externas. Vanilla JS puro.
// ═══════════════════════════════════════════════════════════════════

(function () {

  // ── Captura de elementos ──────────────────────────────────────────
  const canvas = document.getElementById("mapa");
  const ctx    = canvas.getContext("2d");
  const header = document.getElementById("app-header");

  // ── Paleta — alinhada ao design system ───────────────────────────
  const COLOR = {
    background  : "#0a0a0a",
    link        : "rgba(240,147,13,0.45)",  // brand-orange
    node        : "rgb(8,70,121)",           // brand-blue
    nodeStroke  : "rgba(8,70,121,0.5)",
    nodeGlow    : "rgba(8,70,121,0.25)",
    label       : "#ededed",
  };

  // ── Constantes de física ──────────────────────────────────────────
  const PHYSICS = {
    repulsionStrength : 4000,   // Força de repulsão entre nós (Coulomb)
    springLength      : 150,    // Comprimento ideal de repouso da mola (px)
    springStrength    : 0.03,   // Rigidez da mola (Hooke)
    friction          : 0.85,   // Fator de dissipação de energia por frame
    sleepThreshold    : 0.05,   // Velocidade mínima — abaixo disso, nó dorme
    minDistance       : 1,      // Distância mínima para evitar divisão por zero
  };

  // ── Constantes de renderização ────────────────────────────────────
  const RENDER = {
    nodeRadius   : 14,
    linkWidth    : 1.5,
    labelFont    : "500 12px system-ui, sans-serif",
    labelOffsetY : 6,   // px acima do topo do nó
  };

  // ── Controle de IDs ───────────────────────────────────────────────
  let nextNodeId = 3;  // Começa em 3 porque os nós iniciais são 1 e 2

  // ── Estrutura de dados mutável ────────────────────────────────────
  //  Cada nó: { id, label, group, url, x, y, vx, vy, isGrabbed }
  //  Cada link: { source: id, target: id }
  let nodes = [];
  let links = [];

  // ── Controle de Interação ─────────────────────────────────────────
  let selectedNode = null;
  let clickTimer   = null;
  let draggedNetwork = []; // Otimização de Grau 1 (BFS) para arrastar

  // ── Dimensões lógicas (atualizadas no resize) ─────────────────────
  let logicalWidth  = 0;
  let logicalHeight = 0;

  // ─────────────────────────────────────────────────────────────────
  //  CARREGAMENTO DINÂMICO
  // ─────────────────────────────────────────────────────────────────

  async function loadGraphData() {
    try {
      const response = await fetch("/api/graph");
      const data = await response.json();
      
      const cx = logicalWidth  / 2;
      const cy = logicalHeight / 2;

      // Inicializa os nós com posições próximas ao centro
      nodes = data.nodes.map(function(n) {
        return {
          id: n.id,
          label: n.label || n.id, // Suporte para o novo atributo
          group: n.group,
          url: n.url,
          x: cx + (Math.random() * 100 - 50),
          y: cy + (Math.random() * 100 - 50),
          vx: 0,
          vy: 0
        };
      });

      links = data.links;
      
    } catch (err) {
      console.error("Erro ao carregar o grafo:", err);
    }
  }

  // ─────────────────────────────────────────────────────────────────
  //  AJUSTE DE ESCALA HiDPI
  // ─────────────────────────────────────────────────────────────────

  function resizeCanvas() {
    const ratio        = window.devicePixelRatio || 1;
    const headerHeight = header.offsetHeight;

    logicalWidth  = window.innerWidth;
    logicalHeight = window.innerHeight - headerHeight;

    // Resolução interna (pixels físicos)
    canvas.width  = logicalWidth  * ratio;
    canvas.height = logicalHeight * ratio;

    // Tamanho visual preservado em pixels lógicos via CSS
    canvas.style.width    = logicalWidth  + "px";
    canvas.style.height   = logicalHeight + "px";
    canvas.style.marginTop = headerHeight + "px";

    // Escala o contexto: coordenadas de desenho permanecem lógicas
    ctx.scale(ratio, ratio);
  }


  // ─────────────────────────────────────────────────────────────────
  //  INTERAÇÃO COM MOUSE
  // ─────────────────────────────────────────────────────────────────

  canvas.addEventListener("mousedown", function(e) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    // Busca de trás para frente para pegar o nó que está "por cima"
    for (let i = nodes.length - 1; i >= 0; i--) {
      const node = nodes[i];
      if (Math.hypot(node.x - mouseX, node.y - mouseY) <= RENDER.nodeRadius) {
        selectedNode = node;
        
        // Inicia o timer para "pegar" o nó
        clickTimer = setTimeout(function() {
          if (selectedNode) {
            selectedNode.isGrabbed = true;

            // Busca de Grau 1: Encontra todas as conexões diretas
            draggedNetwork = [];
            for (let j = 0; j < links.length; j++) {
              const link = links[j];
              let neighborId = null;

              if (link.source === selectedNode.id) neighborId = link.target;
              else if (link.target === selectedNode.id) neighborId = link.source;

              if (neighborId) {
                // Encontra e acorda o vizinho caso ele esteja dormindo
                const neighborNode = nodes.find(n => n.id === neighborId);
                if (neighborNode) {
                  draggedNetwork.push(neighborNode);
                  neighborNode.vx = 0.1;
                  neighborNode.vy = 0.1;
                }
              }
            }
          }
        }, 200);
        
        break; // Achou o nó, para a busca
      }
    }
  });

  canvas.addEventListener("mousemove", function(e) {
    if (selectedNode && selectedNode.isGrabbed) {
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      // Força a posição do nó principal para o ponteiro do mouse
      selectedNode.x = mouseX;
      selectedNode.y = mouseY;

      // Zera a inércia do nó arrastado para ele não tremer/lutar contra as molas
      selectedNode.vx = 0;
      selectedNode.vy = 0;
      
      // A física global (Lei de Hooke) cuidará de puxar a 'draggedNetwork'
    }
  });

  canvas.addEventListener("mouseup", function(e) {
    if (selectedNode) {
      clearTimeout(clickTimer);

      if (!selectedNode.isGrabbed) {
        // Soltou antes dos 200ms -> Clique rápido -> Navegação
        window.location.href = selectedNode.url;
      } else {
        // Soltou depois de levantar a bolinha -> Apenas solta
        selectedNode.isGrabbed = false;
      }
      
      selectedNode = null;
      draggedNetwork = [];
    }
  });

  // ─────────────────────────────────────────────────────────────────
  //  MOTOR DE FÍSICA
  // ─────────────────────────────────────────────────────────────────

  // Mapa de acesso rápido por id para o loop de links
  function buildNodeMap() {
    const map = {};
    for (let i = 0; i < nodes.length; i++) {
      map[nodes[i].id] = nodes[i];
    }
    return map;
  }

  function applyPhysics() {
    const nodeCount = nodes.length;

    // ── 1. REPULSÃO (Coulomb) ─────────────────────────────────────
    //  Para cada par único (i, j), calcula o vetor distância
    //  e aplica forças iguais e opostas nos dois nós.
    for (let i = 0; i < nodeCount; i++) {
      for (let j = i + 1; j < nodeCount; j++) {
        const nodeA = nodes[i];
        const nodeB = nodes[j];

        const dx = nodeB.x - nodeA.x;
        const dy = nodeB.y - nodeA.y;
        const distanceSq = dx * dx + dy * dy;
        const distance   = Math.sqrt(distanceSq) || PHYSICS.minDistance;

        // Força inversamente proporcional ao quadrado da distância
        const forceMagnitude = PHYSICS.repulsionStrength / distanceSq;

        // Vetor unitário da direção A → B
        const forceX = (dx / distance) * forceMagnitude;
        const forceY = (dy / distance) * forceMagnitude;

        // A repulsa B (força positiva em B, negativa em A)
        nodeA.vx -= forceX;
        nodeA.vy -= forceY;
        nodeB.vx += forceX;
        nodeB.vy += forceY;
      }
    }

    // ── 2. ATRAÇÃO (Hooke) ────────────────────────────────────────
    //  Para cada link, aplica força de mola entre source e target.
    const nodeMap = buildNodeMap();

    for (let k = 0; k < links.length; k++) {
      const link    = links[k];
      const nodeA   = nodeMap[link.source];
      const nodeB   = nodeMap[link.target];

      if (!nodeA || !nodeB) continue;

      const dx       = nodeB.x - nodeA.x;
      const dy       = nodeB.y - nodeA.y;
      const distance = Math.sqrt(dx * dx + dy * dy) || PHYSICS.minDistance;

      // Só atrai se a distância atual for maior que o comprimento ideal
      const displacement = distance - PHYSICS.springLength;

      if (displacement > 0) {
        const forceX = (dx / distance) * displacement * PHYSICS.springStrength;
        const forceY = (dy / distance) * displacement * PHYSICS.springStrength;

        nodeA.vx += forceX;
        nodeA.vy += forceY;
        nodeB.vx -= forceX;
        nodeB.vy -= forceY;
      }
    }

    // ── 3. GRAVIDADE CENTRAL ──────────────────────────────────────
    const cx = logicalWidth / 2;
    const cy = logicalHeight / 2;
    
    for (let i = 0; i < nodeCount; i++) {
      const node = nodes[i];
      const dx = cx - node.x;
      const dy = cy - node.y;
      
      node.vx += dx * 0.002;
      node.vy += dy * 0.002;
    }

    // ── 4. ATRITO & ATUALIZAÇÃO DE POSIÇÃO ────────────────────────
    for (let i = 0; i < nodeCount; i++) {
      const node = nodes[i];

      // Dissipa energia (simula resistência do meio)
      node.vx *= PHYSICS.friction;
      node.vy *= PHYSICS.friction;

      // Estado de dormência: micro-velocidades são zeradas
      if (Math.abs(node.vx) + Math.abs(node.vy) < PHYSICS.sleepThreshold) {
        node.vx = 0;
        node.vy = 0;
      }

      // Integração de Euler: atualiza posição
      node.x += node.vx;
      node.y += node.vy;
    }
  }

  // ─────────────────────────────────────────────────────────────────
  //  RENDERIZAÇÃO
  // ─────────────────────────────────────────────────────────────────

  function drawBackground() {
    ctx.fillStyle = COLOR.background;
    ctx.fillRect(0, 0, logicalWidth, logicalHeight);
  }

  function drawLink(nodeA, nodeB) {
    ctx.beginPath();
    ctx.moveTo(nodeA.x, nodeA.y);
    ctx.lineTo(nodeB.x, nodeB.y);
    ctx.strokeStyle = COLOR.link;
    ctx.lineWidth   = RENDER.linkWidth;
    ctx.stroke();
  }

  const groupColors = {};
  let currentHue = Math.random() * 360; // Semente inicial aleatória

  function drawNode(node) {
    // Se o nó estiver levantado (grabbed), o raio aumenta visualmente
    const r = node.isGrabbed ? RENDER.nodeRadius + 5 : RENDER.nodeRadius;

    // Resolve a cor do nó baseado no grupo (pasta pai)
    if (node.group && !groupColors[node.group]) {
      // Usa o Ângulo de Ouro (~137.5 graus) para garantir cores sempre distintas
      groupColors[node.group] = `hsl(${currentHue}, 70%, 60%)`;
      currentHue = (currentHue + 137.5) % 360;
    }
    const nodeColor = node.group ? groupColors[node.group] : COLOR.node;

    // Aplica sombra se estiver levantado
    if (node.isGrabbed) {
      ctx.shadowBlur = 15;
      ctx.shadowColor = "rgba(0,0,0,0.5)";
    } else {
      ctx.shadowBlur = 0;
    }

    // Glow externo
    ctx.beginPath();
    ctx.arc(node.x, node.y, r + 4, 0, Math.PI * 2);
    ctx.fillStyle = COLOR.nodeGlow;
    ctx.fill();

    // Preenchimento principal
    ctx.beginPath();
    ctx.arc(node.x, node.y, r, 0, Math.PI * 2);
    ctx.fillStyle = nodeColor;
    ctx.fill();

    // Borda
    ctx.strokeStyle = COLOR.nodeStroke;
    ctx.lineWidth   = 2;
    ctx.stroke();

    // Limpa a sombra para não afetar os textos e os outros nós
    ctx.shadowBlur = 0;

    // Rótulo acima do nó (usa label ao invés do id interno)
    ctx.font         = RENDER.labelFont;
    ctx.fillStyle    = COLOR.label;
    ctx.textAlign    = "center";
    ctx.textBaseline = "bottom";
    ctx.fillText(node.label || node.id, node.x, node.y - r - RENDER.labelOffsetY);
  }

  function render() {
    const nodeMap = buildNodeMap();

    drawBackground();

    // Links (camada inferior)
    for (let k = 0; k < links.length; k++) {
      const nodeA = nodeMap[links[k].source];
      const nodeB = nodeMap[links[k].target];
      if (nodeA && nodeB) drawLink(nodeA, nodeB);
    }

    // Nós (camada superior)
    for (let i = 0; i < nodes.length; i++) {
      drawNode(nodes[i]);
    }
  }

  // ─────────────────────────────────────────────────────────────────
  //  LOOP PRINCIPAL
  // ─────────────────────────────────────────────────────────────────

  function loop() {
    applyPhysics();
    render();
    requestAnimationFrame(loop);
  }

  // ─────────────────────────────────────────────────────────────────
  //  INICIALIZAÇÃO
  // ─────────────────────────────────────────────────────────────────

  resizeCanvas();
  loadGraphData().then(() => {
    window.addEventListener("resize", resizeCanvas);
    requestAnimationFrame(loop);
  });

})();

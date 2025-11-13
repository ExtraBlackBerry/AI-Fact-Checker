document.addEventListener("contextmenu", (e) => {
  window._factcheckerMouseX = e.clientX;
  window._factcheckerMouseY = e.clientY;
});

chrome.runtime.onMessage.addListener((message) => {

  console.log("FACT CHECKER UI SCRIPT LOADED");
  console.log("Received message:", message);

  if (!message || !message.result) return;

  const result = message.result;
  if (typeof result !== "object" || !("score" in result) || !Array.isArray(result.results)) return;

  const existing = document.getElementById("factchecker-popup");
  if (existing) existing.remove();

  const { score, results } = result;

  const x = window._factcheckerMouseX || 50;
  const y = window._factcheckerMouseY || 50;

  // === POPUP CONTAINER ===
  const popup = document.createElement("div");
  popup.id = "factchecker-popup";
  popup.style.position = "fixed";
  popup.style.left = x + "px";
  popup.style.top = y + "px";
  popup.style.width = "320px";
  popup.style.background = "white";
  popup.style.borderRadius = "12px";
  popup.style.boxShadow = "0 0 12px rgba(0,0,0,0.2)";
  popup.style.zIndex = "999999";
  popup.style.padding = "20px";
  popup.style.fontFamily = "Arial, sans-serif";
  popup.style.userSelect = "none";
  popup.style.cursor = "move";

  // === CLOSE BUTTON ===
  const closeBtn = document.createElement("div");
  closeBtn.textContent = "×";
  closeBtn.style.position = "absolute";
  closeBtn.style.top = "10px";
  closeBtn.style.right = "14px";
  closeBtn.style.fontSize = "20px";
  closeBtn.style.cursor = "pointer";
  closeBtn.addEventListener("click", () => popup.remove());
  popup.appendChild(closeBtn);

  // === TITLE ===
  const title = document.createElement("div");
  title.textContent = "FAVS";
  title.style.textAlign = "center";
  title.style.fontSize = "18px";
  title.style.fontWeight = "600";
  title.style.marginBottom = "10px";
  popup.appendChild(title);

  // === CANVAS GAUGE ===
  const canvas = document.createElement("canvas");
  canvas.width = 250;
  canvas.height = 140;
  canvas.style.display = "block";
  canvas.style.margin = "0 auto";
  popup.appendChild(canvas);

  const ctx = canvas.getContext("2d");

  const radius = 110;
  const cx = canvas.width / 2;
  const cy = canvas.height * 1.2;

  // Background arc
  ctx.beginPath();
  ctx.lineWidth = 18;
  ctx.strokeStyle = "#d3d3d3";
  ctx.arc(cx, cy, radius, Math.PI, 0, false);
  ctx.stroke();

  // Score arc
  ctx.beginPath();
  ctx.strokeStyle = "#222";
  ctx.arc(cx, cy, radius, Math.PI, Math.PI + (Math.PI * score), false);
  ctx.stroke();

  // === SCORE LABEL ===
  const label = document.createElement("div");
  label.textContent = "Verification Score";
  label.style.textAlign = "center";
  label.style.marginTop = "5px";
  label.style.color = "#555";
  label.style.fontSize = "12px";
  popup.appendChild(label);

  const percent = document.createElement("div");
  percent.textContent = Math.round(score * 100) + "%";
  percent.style.textAlign = "center";
  percent.style.fontSize = "28px";
  percent.style.fontWeight = "700";
  percent.style.marginTop = "2px";
  popup.appendChild(percent);

  // === SCALE LABELS ===
  const left = document.createElement("div");
  left.textContent = "0";
  left.style.position = "absolute";
  left.style.left = "20px";
  left.style.bottom = "90px";
  left.style.fontSize = "12px";
  left.style.color = "#777";
  popup.appendChild(left);

  const right = document.createElement("div");
  right.textContent = "100";
  right.style.position = "absolute";
  right.style.right = "20px";
  right.style.bottom = "90px";
  right.style.fontSize = "12px";
  right.style.color = "#777";
  popup.appendChild(right);

  // === DETAILS LINK ===
  const more = document.createElement("div");
  more.textContent = "More details";
  more.style.textAlign = "center";
  more.style.marginTop = "12px";
  more.style.textDecoration = "underline";
  more.style.cursor = "pointer";
  popup.appendChild(more);

  // === HIDDEN LINKS ===
  const linksContainer = document.createElement("div");
  linksContainer.style.display = "none";
  linksContainer.style.marginTop = "10px";
  linksContainer.style.maxHeight = "150px";
  linksContainer.style.overflowY = "auto";

  results.forEach(text => {
  const p = document.createElement("div");
  p.textContent = text;
  p.style.whiteSpace = "pre-wrap";   // keeps line breaks
  p.style.fontSize = "12px";
  p.style.marginTop = "6px";
  p.style.padding = "6px 4px";
  p.style.background = "#f7f7f7";
  p.style.borderRadius = "6px";
  linksContainer.appendChild(p);
});

  popup.appendChild(linksContainer);

  more.addEventListener("click", () => {
    linksContainer.style.display = linksContainer.style.display === "none" ? "block" : "none";
  });

  // === DRAGGING ===
  let dragging = false;
  let offsetX = 0, offsetY = 0;

  popup.addEventListener("mousedown", e => {
    dragging = true;
    offsetX = e.clientX - popup.offsetLeft;
    offsetY = e.clientY - popup.offsetTop;
  });

  document.addEventListener("mousemove", e => {
    if (!dragging) return;
    popup.style.left = e.clientX - offsetX + "px";
    popup.style.top = e.clientY - offsetY + "px";
  });

  document.addEventListener("mouseup", () => dragging = false);

  document.body.appendChild(popup);
});

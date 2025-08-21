document.addEventListener("contextmenu", (e) => {
  window._factcheckerMouseX = e.clientX;
  window._factcheckerMouseY = e.clientY;
});

chrome.runtime.onMessage.addListener((message) => {
  if (!message || !message.result) return;
  const result = message.result;
  if (typeof result !== "object" || !("score" in result) || !Array.isArray(result.results)) return;

  const existing = document.getElementById("factchecker-popup");
  if (existing) existing.remove();

  const { score, results } = result;
  let x = window._factcheckerMouseX || 0;
  let y = window._factcheckerMouseY || 0;

  const popup = document.createElement("div");
  popup.id = "factchecker-popup";
  popup.style.position = "fixed";
  popup.style.left = x + "px";
  popup.style.top = y + "px";
  popup.style.width = "250px";
  popup.style.background = "#fff";
  popup.style.borderRadius = "8px";
  popup.style.boxShadow = "0 0 8px rgba(0,0,0,0.3)";
  popup.style.zIndex = "99999";
  popup.style.padding = "12px";
  popup.style.fontFamily = "Arial, sans-serif";
  popup.style.cursor = "move";

  const closeBtn = document.createElement("span");
  closeBtn.textContent = "×";
  closeBtn.style.cursor = "pointer";
  closeBtn.style.float = "right";
  closeBtn.style.fontSize = "18px";
  closeBtn.addEventListener("click", () => popup.remove());
  popup.appendChild(closeBtn);

  if (typeof score === "number") {
    const circle = document.createElement("div");
    circle.textContent = score.toFixed(2);
    circle.style.width = "70px";
    circle.style.height = "70px";
    circle.style.borderRadius = "50%";
    circle.style.margin = "20px auto";
    circle.style.display = "flex";
    circle.style.alignItems = "center";
    circle.style.justifyContent = "center";
    circle.style.fontSize = "24px";
    circle.style.fontWeight = "600";
    circle.style.border = "3px solid #000";
    popup.appendChild(circle);
  } else {
    const msg = document.createElement("div");
    msg.textContent = score;
    msg.style.textAlign = "center";
    msg.style.fontWeight = "600";
    msg.style.margin = "20px auto";
    popup.appendChild(msg);
  }

  const toggle = document.createElement("div");
  toggle.textContent = "Links ▼";
  toggle.style.cursor = "pointer";
  toggle.style.fontWeight = "600";
  popup.appendChild(toggle);

  const linksContainer = document.createElement("div");
  linksContainer.style.display = "none";
  linksContainer.style.maxHeight = "150px";
  linksContainer.style.overflowY = "auto";

  results.forEach((url) => {
    const a = document.createElement("a");
    a.href = url;
    a.textContent = url;
    a.target = "_blank";
    a.style.display = "block";
    a.style.wordBreak = "break-all";
    linksContainer.appendChild(a);
  });
  popup.appendChild(linksContainer);

  toggle.addEventListener("click", () => {
    const open = linksContainer.style.display === "none";
    linksContainer.style.display = open ? "block" : "none";
    toggle.textContent = open ? "Links ▲" : "Links ▼";
  });

  let isDragging = false;
  let offsetX = 0;
  let offsetY = 0;

  popup.addEventListener("mousedown", (e) => {
    isDragging = true;
    offsetX = e.clientX - popup.getBoundingClientRect().left;
    offsetY = e.clientY - popup.getBoundingClientRect().top;
  });

  document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    popup.style.left = e.clientX - offsetX + "px";
    popup.style.top = e.clientY - offsetY + "px";
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
  });

  document.body.appendChild(popup);
});

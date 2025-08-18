chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.result) {

    const existing = document.getElementById("factchecker-sidebar");
    if (existing) existing.remove();

    const sidebar = document.createElement("div");
    sidebar.id = "factchecker-sidebar";
    sidebar.style.position = "fixed";
    sidebar.style.top = "0";
    sidebar.style.right = "0";
    sidebar.style.width = "300px";
    sidebar.style.height = "100%";
    sidebar.style.overflow = "auto";
    sidebar.style.background = "white";
    sidebar.style.boxShadow = "0 0 8px rgba(0,0,0,0.3)";
    sidebar.style.zIndex = "9999";
    sidebar.style.padding = "10px";
    sidebar.innerText = JSON.stringify(message.result, null, 2);

    document.body.appendChild(sidebar);
  }
});

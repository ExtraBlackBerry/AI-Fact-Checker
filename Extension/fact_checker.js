chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "send-to-pipeline",
    title: "FACT CHECK",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "send-to-pipeline") {
    const selectedText = info.selectionText;

    fetch('http://localhost:5000/fact_check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: selectedText })
    })
    .then(response => response.json())
    .then(data => {
      chrome.tabs.sendMessage(tab.id, { result: data });
    });
  }
});

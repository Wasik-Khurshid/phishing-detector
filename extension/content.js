// content.js
// Runs inside every webpage — shows warning banner if phishing detected

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === "PHISHING_DETECTED") {
    showWarningBanner(message.score, message.flags)
  }
})

function showWarningBanner(score, flags) {
  // Don't show twice
  if (document.getElementById("phishing-detector-banner")) return

  const banner = document.createElement("div")
  banner.id = "phishing-detector-banner"
  banner.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
    background: #1a0000;
    border-bottom: 3px solid #ef4444;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 4px 20px rgba(239,68,68,0.4);
  `

  const topFlags = flags.slice(0, 2).join(" • ")

  banner.innerHTML = `
    <div style="display:flex;align-items:center;gap:12px">
      <span style="font-size:24px">🚨</span>
      <div>
        <div style="color:#ef4444;font-weight:700;font-size:14px">
          PHISHING WARNING — Risk Score: ${score}/100
        </div>
        <div style="color:#94a3b8;font-size:11px;margin-top:2px">
          ${topFlags}
        </div>
      </div>
    </div>
    <button id="phishing-close-btn" style="
      background: #ef4444;
      color: white;
      border: none;
      border-radius: 6px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    ">Dismiss</button>
  `

  document.body.prepend(banner)

  document.getElementById("phishing-close-btn").onclick = () => {
    banner.remove()
  }
}
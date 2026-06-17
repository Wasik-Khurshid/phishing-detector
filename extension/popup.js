// popup.js — Shows stored result (no need to re-fetch)

let currentUrl = ""
let tabId = null

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  currentUrl = tabs[0].url
  tabId = tabs[0].id
  document.getElementById("urlBox").textContent = currentUrl

  // Load stored result
  chrome.storage.local.get([`result_${tabId}`], (data) => {
    const result = data[`result_${tabId}`]
    if (result) {
      showResult(result)
    } else {
      document.getElementById("loading").style.display = "block"
    }
  })
})

// Manual re-analyze button
function analyze() {
  document.getElementById("loading").style.display = "block"
  document.getElementById("result").innerHTML = ""
  document.getElementById("analyzeBtn").disabled = true

  fetch("https://phishing-detector-z2s5.onrender.com/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: currentUrl })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("loading").style.display = "none"
      document.getElementById("analyzeBtn").disabled = false
      showResult(data)
    })
    .catch(() => {
      document.getElementById("loading").style.display = "none"
      document.getElementById("analyzeBtn").disabled = false
      document.getElementById("result").innerHTML = `
        <div class="error">❌ API Error — Wait 50s (Render wakeup)</div>
      `
    })
}

function showResult(data) {
  const verdict = data.verdict
  const finalScore = data.final_score
  const mlScore = data.ml_score
  const heuristicScore = data.heuristic_score
  const flags = data.flags || []

  const cls = verdict === "PHISHING" ? "phishing"
             : verdict === "SUSPICIOUS" ? "suspicious"
             : "safe"

  const barColor = finalScore > 60 ? "red"
                 : finalScore > 30 ? "yellow"
                 : "green"

  const emoji = verdict === "PHISHING" ? "🚨"
               : verdict === "SUSPICIOUS" ? "⚠️"
               : "✅"

  const flagsHtml = flags.length > 0 ? `
    <div class="flags">
      <h3>⚠ Red Flags:</h3>
      ${flags.map(f => `
        <div class="flag-item"><span>•</span> ${f}</div>
      `).join("")}
    </div>
  ` : `<div style="text-align:center;color:#22c55e;font-size:12px;margin-top:8px">No red flags found ✓</div>`

  document.getElementById("loading").style.display = "none"
  document.getElementById("result").innerHTML = `
    <div class="result ${cls}">
      <div class="verdict">${emoji} ${verdict}</div>
      <div class="scores-grid">
        <div class="score-card">
          <div class="val">${mlScore}%</div>
          <div class="label">ML Score</div>
        </div>
        <div class="score-card">
          <div class="val purple">${heuristicScore}/100</div>
          <div class="label">Heuristic Score</div>
        </div>
      </div>
      <div class="score-row">
        <span>Final Risk Score</span>
        <span>${finalScore}/100</span>
      </div>
      <div class="score-bar">
        <div class="score-fill ${barColor}" style="width:${finalScore}%"></div>
      </div>
      ${flagsHtml}
    </div>
  `
}
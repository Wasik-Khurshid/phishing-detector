// background.js
// Runs in background — auto checks every tab when URL changes

const API_URL = "https://phishing-detector-z2s5.onrender.com/api/analyze"

// Check URL and update badge color
async function checkUrl(tabId, url) {
  // Skip chrome:// and extension pages
  if (!url || url.startsWith("chrome") || url.startsWith("edge") || url.startsWith("about")) {
    return
  }

  try {
    // Show loading — grey badge
    chrome.action.setBadgeText({ tabId, text: "..." })
    chrome.action.setBadgeBackgroundColor({ tabId, color: "#64748b" })

    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    })

    const data = await response.json()

    // Store result for popup to use
    chrome.storage.local.set({ [`result_${tabId}`]: data })

    // Update badge based on verdict
    if (data.verdict === "PHISHING") {
      chrome.action.setBadgeText({ tabId, text: "⚠" })
      chrome.action.setBadgeBackgroundColor({ tabId, color: "#ef4444" })

      // Send message to content script to show warning banner
      chrome.tabs.sendMessage(tabId, {
        type: "PHISHING_DETECTED",
        score: data.final_score,
        flags: data.flags
      })

    } else if (data.verdict === "SUSPICIOUS") {
      chrome.action.setBadgeText({ tabId, text: "??" })
      chrome.action.setBadgeBackgroundColor({ tabId, color: "#f59e0b" })

    } else {
      chrome.action.setBadgeText({ tabId, text: "✓" })
      chrome.action.setBadgeBackgroundColor({ tabId, color: "#22c55e" })
    }

  } catch (err) {
    chrome.action.setBadgeText({ tabId, text: "!" })
    chrome.action.setBadgeBackgroundColor({ tabId, color: "#64748b" })
  }
}

// Auto-trigger on every tab update
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    checkUrl(tabId, tab.url)
  }
})
import { useState } from "react"

function App() {
  const [url, setUrl] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyzeUrl = async () => {
    if (!url.trim()) return
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch("https://phishing-detector-z2s5.onrender.com/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url }),
      })
      if (!response.ok) throw new Error("API error")
      const data = await response.json()
      setResult(data)
    } catch (error) {
      alert("Error: Flask server chal raha hai? http://127.0.0.1:5000")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-cyan-400 mb-2">
          🛡️ Phishing Detector
        </h1>
        <p className="text-center text-gray-400 mb-8">
          Enter a URL to check if it's safe or a phishing attempt
        </p>

        <div className="flex gap-3 mb-8">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && analyzeUrl()}
            placeholder="Enter URL e.g. http://paypa1-login.ru/secure"
            className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400"
          />
          <button
            onClick={analyzeUrl}
            disabled={loading}
            className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 text-black font-bold px-6 py-3 rounded-lg transition-colors"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {loading && (
          <div className="text-center text-cyan-400 animate-pulse text-lg">
            🔍 Analyzing URL...
          </div>
        )}

        {result && (
          <div className={`rounded-xl border p-6 mb-6 ${
            result.verdict === "PHISHING"
              ? "border-red-500 bg-red-950"
              : result.verdict === "SUSPICIOUS"
              ? "border-yellow-500 bg-yellow-950"
              : "border-green-500 bg-green-950"
          }`}>

            <div className="text-center mb-6">
              <div className={`text-5xl font-black mb-2 ${
                result.verdict === "PHISHING" ? "text-red-400" :
                result.verdict === "SUSPICIOUS" ? "text-yellow-400" :
                "text-green-400"
              }`}>
                {result.verdict === "PHISHING" ? "🚨 PHISHING" :
                 result.verdict === "SUSPICIOUS" ? "⚠️ SUSPICIOUS" :
                 "✅ SAFE"}
              </div>
              <p className="text-gray-300 text-sm break-all">{result.url}</p>
            </div>

            <div className="mb-6">
              <div className="flex justify-between mb-1">
                <span className="text-sm text-gray-400">Final Risk Score</span>
                <span className="text-sm font-bold text-white">{result.final_score}/100</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-4">
                <div
                  className={`h-4 rounded-full transition-all ${
                    result.final_score > 60 ? "bg-red-500" :
                    result.final_score > 30 ? "bg-yellow-500" :
                    "bg-green-500"
                  }`}
                  style={{ width: `${result.final_score}%` }}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-cyan-400">{result.ml_score}%</div>
                <div className="text-xs text-gray-400">ML Model Score</div>
              </div>
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-purple-400">{result.heuristic_score}/100</div>
                <div className="text-xs text-gray-400">Heuristic Score</div>
              </div>
            </div>

            {result.flags && result.flags.length > 0 && (
              <div className="mb-6">
                <h3 className="text-sm font-bold text-red-400 mb-2">⚠ Red Flags Triggered:</h3>
                <ul className="space-y-1">
                  {result.flags.map((flag, i) => (
                    <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                      <span className="text-red-400 mt-0.5">•</span>
                      {flag}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.features && (
              <div>
                <h3 className="text-sm font-bold text-gray-400 mb-2">📊 URL Features:</h3>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(result.features).map(([key, value]) => (
                    <div key={key} className="bg-gray-800 rounded px-3 py-2 flex justify-between">
                      <span className="text-xs text-gray-400">{key}</span>
                      <span className="text-xs font-bold text-white">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
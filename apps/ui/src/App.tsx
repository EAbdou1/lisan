import { useEffect } from "react"
import { useLisanEvents } from "./hooks/useLisanEvents"
import { usePywebview } from "./hooks/usePywebview"
import { useLisanStore } from "./store"

export default function App() {
  const { api, ready } = usePywebview()
  const { status, lastTranscript, error } = useLisanStore()
  useLisanEvents()

  // Load initial data once pywebview is ready
  useEffect(() => {
    if (!ready || !api) return

    const loadData = async () => {
      const [history, snippets, settings] = await Promise.all([
        api.get_history(),
        api.get_snippets(),
        api.get_settings(),
      ])

      useLisanStore.getState().setHistory(history)
      useLisanStore.getState().setSnippets(snippets)
      useLisanStore.getState().setSettings(settings)
    }

    loadData()
  }, [ready, api])

  // Temporary UI to verify everything works
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-[#0A0A0F] text-white">
      <h1 className="text-2xl font-bold mb-4">لسان</h1>

      <div className="text-sm text-gray-400 mb-6">
        Status: <span className="text-indigo-400">{status}</span>
      </div>

      {error && (
        <div className="text-red-400 text-sm mb-4">
          Error: {error}
        </div>
      )}

      {lastTranscript && (
        <div className="bg-[#111118] rounded-lg p-4 max-w-xs w-full">
          <p className="text-xs text-gray-500 mb-1">Last transcript</p>
          <p className="text-sm">{lastTranscript.cleaned}</p>
          <p className="text-xs text-gray-500 mt-2">
            {lastTranscript.wordCount} words · {lastTranscript.duration}s
          </p>
        </div>
      )}

      {!ready && (
        <p className="text-xs text-gray-600 mt-4">
          Waiting for pywebview...
        </p>
      )}
    </div>
  )
}
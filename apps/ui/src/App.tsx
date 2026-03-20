import { useEffect } from "react"
import { useLisanEvents } from "./hooks/useLisanEvents"
import { usePywebview } from "./hooks/usePywebview"
import { useLisanStore } from "./store"
import { SettingsTab } from "./components/SettingsTab"
import type { Tab } from "./store"

const NAV_TABS: { id: Tab; label: string }[] = [
  { id: "main", label: "Lisan" },
  { id: "history", label: "History" },
  { id: "snippets", label: "Snippets" },
  { id: "settings", label: "Settings" },
]

export default function App() {
  const { api, ready } = usePywebview()
  const { status, lastTranscript, error, activeTab, setActiveTab } = useLisanStore()
  useLisanEvents()

  // Load initial data once pywebview is ready
  useEffect(() => {
    if (!ready || !api) return
    const load = async () => {
      const [history, snippets, settings] = await Promise.all([
        api.get_history(),
        api.get_snippets(),
        api.get_settings(),
      ])
      useLisanStore.getState().setHistory(history)
      useLisanStore.getState().setSnippets(snippets)
      useLisanStore.getState().setSettings(settings)
    }
    load()
  }, [ready, api])

  // Handle navigate events from tray
  useEffect(() => {
    const original = window.lisanEvent
    window.lisanEvent = (event, data) => {
      if (event === "navigate") {
        setActiveTab(data as Tab)
        return
      }
      original?.(event, data)
    }
  }, [setActiveTab])

  return (
    <div className="flex flex-col h-screen bg-[#0A0A0F] text-white select-none">

      {/* Tab bar */}
      <div className="flex border-b border-white/5 px-2 pt-2 gap-1 flex-shrink-0">
        {NAV_TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-1.5 text-xs rounded-t-md transition-colors
                        ${activeTab === tab.id
                          ? "text-white bg-[#111118] border border-white/10 border-b-[#111118]"
                          : "text-[#888899] hover:text-white"
                        }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === "main" && (
          <div className="flex flex-col items-center justify-center h-full gap-4 px-4">
            <h1 className="text-2xl font-bold">LISAN</h1>
            <div className="text-sm text-[#888899]">
              Status: <span className="text-indigo-400">{status}</span>
            </div>
            {error && (
              <p className="text-red-400 text-sm">Error: {error}</p>
            )}
            {lastTranscript && (
              <div className="bg-[#111118] rounded-lg p-4 w-full border border-white/5">
                <p className="text-xs text-[#888899] mb-1">Last transcript</p>
                <p className="text-sm">{lastTranscript.cleaned}</p>
                <p className="text-xs text-[#888899] mt-2">
                  {lastTranscript.wordCount} words · {lastTranscript.duration}s
                </p>
              </div>
            )}
            {!ready && (
              <p className="text-xs text-[#444455]">Waiting for pywebview...</p>
            )}
          </div>
        )}

        {activeTab === "history" && (
          <div className="flex items-center justify-center h-full">
            <p className="text-sm text-[#888899]">History — coming soon</p>
          </div>
        )}

        {activeTab === "snippets" && (
          <div className="flex items-center justify-center h-full">
            <p className="text-sm text-[#888899]">Snippets — coming soon</p>
          </div>
        )}

        {activeTab === "settings" && <SettingsTab />}
      </div>
    </div>
  )
}

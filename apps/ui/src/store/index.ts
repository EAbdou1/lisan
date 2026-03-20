import { create } from "zustand";
import type {
  AppStatus,
  Transcript,
  HistoryItem,
  Snippet,
  AppSettings,
} from "../types/bridge";

export type Tab = "main" | "history" | "snippets" | "settings";

interface LisanStore {
  // State
  status: AppStatus;
  lastTranscript: Transcript | null;
  history: HistoryItem[];
  snippets: Snippet[];
  settings: AppSettings | null;
  error: string | null;
  activeTab: Tab;

  // Actions
  setStatus: (status: AppStatus) => void;
  setTranscript: (t: Transcript) => void;
  setHistory: (h: HistoryItem[]) => void;
  setSnippets: (s: Snippet[]) => void;
  setSettings: (s: AppSettings) => void;
  setError: (e: string | null) => void;
  setActiveTab: (tab: Tab) => void;
}

export const useLisanStore = create<LisanStore>((set) => ({
  status: "idle",
  lastTranscript: null,
  history: [],
  snippets: [],
  settings: null,
  error: null,
  activeTab: "main",

  setStatus: (status) => set({ status }),
  setTranscript: (lastTranscript) => set({ lastTranscript }),
  setHistory: (history) => set({ history }),
  setSnippets: (snippets) => set({ snippets }),
  setSettings: (settings) => set({ settings }),
  setError: (error) => set({ error }),
  setActiveTab: (activeTab) => set({ activeTab }),
}));

export type AppStatus =
  | "idle"
  | "recording"
  | "transcribing"
  | "cleaning"
  | "error";

export interface Transcript {
  raw: string;
  cleaned: string;
  wordCount: number;
  duration: number;
}

export interface HistoryItem {
  id: number;
  raw_transcript: string;
  cleaned_transcript: string;
  app_name: string | null;
  word_count: number | null;
  duration_seconds: number | null;
  language: string | null;
  created_at: string;
}

export interface Snippet {
  id: number;
  trigger: string;
  expansion: string;
  created_at: string;
}

export interface AppSettings {
  hotkey: string;
  language: string;
  cleanupMode: string;
}

// The pywebview bridge — all methods return Promises
export interface PyWebviewAPI {
  start_recording: () => Promise<void>;
  stop_recording: () => Promise<void>;
  get_history: () => Promise<HistoryItem[]>;
  get_snippets: () => Promise<Snippet[]>;
  save_snippet: (trigger: string, expansion: string) => Promise<void>;
  delete_snippet: (id: number) => Promise<void>;
  get_settings: () => Promise<AppSettings>;
}

// Augment the global window object
declare global {
  interface Window {
    pywebview: { api: PyWebviewAPI };
    lisanEvent: (event: string, data: unknown) => void;
  }
}

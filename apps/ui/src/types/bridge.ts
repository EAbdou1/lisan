export type AppStatus =
  | "idle"
  | "recording"
  | "transcribing"
  | "cleaning"
  | "error";

export type Language = "auto" | "ar" | "en";
export type CleanupMode = "light" | "aggressive" | "off";

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

export interface Microphone {
  index: number;
  name: string;
  channels: number;
}

export interface AppSettings {
  hotkey: string;
  language: Language;
  cleanupMode: CleanupMode;
  micDevice: number | null;
  microphones: Microphone[];
}

export interface SaveSettingsPayload {
  hotkey?: string;
  language?: Language;
  cleanup_mode?: CleanupMode;
  mic_device?: number | null;
}

export interface PyWebviewAPI {
  start_recording: () => Promise<void>;
  stop_recording: () => Promise<void>;
  get_history: () => Promise<HistoryItem[]>;
  get_snippets: () => Promise<Snippet[]>;
  save_snippet: (trigger: string, expansion: string) => Promise<void>;
  delete_snippet: (id: number) => Promise<void>;
  get_settings: () => Promise<AppSettings>;
  save_settings: (payload: SaveSettingsPayload) => Promise<void>;
}

declare global {
  interface Window {
    pywebview: { api: PyWebviewAPI };
    lisanEvent: (event: string, data: unknown) => void;
  }
}

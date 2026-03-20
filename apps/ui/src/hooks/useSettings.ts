import { useState, useEffect } from "react";
import { useLisanStore } from "../store";
import { usePywebview } from "./usePywebview";
import type { Language, CleanupMode } from "../types/bridge";

export interface SettingsDraft {
  hotkey: string;
  language: Language;
  cleanupMode: CleanupMode;
  micDevice: number | null;
}

export function useSettings() {
  const { api, ready } = usePywebview();
  const { settings, setSettings } = useLisanStore();

  const [draft, setDraft] = useState<SettingsDraft>({
    hotkey: "alt+space",
    language: "auto",
    cleanupMode: "light",
    micDevice: null,
  });

  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [recordingHotkey, setRecordingHotkey] = useState(false);

  // Sync draft when settings load
  useEffect(() => {
    if (!settings) return;
    setDraft({
      hotkey: settings.hotkey,
      language: settings.language,
      cleanupMode: settings.cleanupMode,
      micDevice: settings.micDevice,
    });
  }, [settings]);

  // Hotkey recorder — listen for key combos
  useEffect(() => {
    if (!recordingHotkey) return;

    const held = new Set<string>();

    const onKeyDown = (e: KeyboardEvent) => {
      e.preventDefault();
      held.add(e.key.toLowerCase());

      const modifiers = ["alt", "control", "shift", "meta"];
      const mod = modifiers.find((m) => held.has(m));
      const key = [...held].find((k) => !modifiers.includes(k));

      if (mod && key) {
        const modLabel = mod === "control" ? "ctrl" : mod;
        const keyLabel = key === " " ? "space" : key;
        setDraft((d) => ({ ...d, hotkey: `${modLabel}+${keyLabel}` }));
        setRecordingHotkey(false);
      }
    };

    const onKeyUp = (e: KeyboardEvent) => {
      held.delete(e.key.toLowerCase());
    };

    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("keyup", onKeyUp);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
    };
  }, [recordingHotkey]);

  const save = async () => {
    if (!api || !ready) return;
    setSaving(true);
    try {
      await api.save_settings({
        hotkey: draft.hotkey,
        language: draft.language,
        cleanup_mode: draft.cleanupMode,
        mic_device: draft.micDevice,
      });
      const updated = await api.get_settings();
      setSettings(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } finally {
      setSaving(false);
    }
  };

  return {
    draft,
    setDraft,
    saving,
    saved,
    recordingHotkey,
    setRecordingHotkey,
    save,
    microphones: settings?.microphones ?? [],
  };
}

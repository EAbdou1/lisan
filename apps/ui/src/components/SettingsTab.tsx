import { useSettings } from "../hooks/useSettings";
import type { Language, CleanupMode } from "../types/bridge";

const LANGUAGES: { value: Language; label: string }[] = [
  { value: "auto", label: "Auto detect" },
  { value: "ar", label: "Arabic — العربية" },
  { value: "en", label: "English" },
];

const CLEANUP_MODES: {
  value: CleanupMode;
  label: string;
  description: string;
}[] = [
  { value: "light", label: "Light", description: "Remove fillers only" },
  { value: "aggressive", label: "Aggressive", description: "Full grammar fix" },
  { value: "off", label: "Off", description: "Raw transcript" },
];

export function SettingsTab() {
  const {
    draft,
    setDraft,
    saving,
    saved,
    recordingHotkey,
    setRecordingHotkey,
    save,
    microphones,
  } = useSettings();

  return (
    <div className="flex flex-col h-full overflow-y-auto px-4 py-5 gap-6">
      {/* Microphone */}
      <Section title="Microphone">
        <select
          value={draft.micDevice ?? ""}
          onChange={(e) =>
            setDraft((d) => ({
              ...d,
              micDevice: e.target.value === "" ? null : Number(e.target.value),
            }))
          }
          className="w-full bg-[#1A1A24] border border-white/10 text-white text-sm
                     rounded-lg px-3 py-2.5 outline-none focus:border-indigo-500
                     transition-colors"
        >
          <option value="">System default</option>
          {microphones.map((mic) => (
            <option key={mic.index} value={mic.index}>
              {mic.name}
            </option>
          ))}
        </select>
      </Section>

      {/* Hotkey */}
      <Section title="Hotkey">
        <button
          onClick={() => setRecordingHotkey(true)}
          className={`w-full rounded-lg px-3 py-2.5 text-sm font-mono text-left
                      border transition-all outline-none
                      ${
                        recordingHotkey
                          ? "border-indigo-500 bg-indigo-500/10 text-indigo-300 animate-pulse"
                          : "border-white/10 bg-[#1A1A24] text-white hover:border-white/20"
                      }`}
        >
          {recordingHotkey ? "Press your combo..." : draft.hotkey}
        </button>
        <p className="text-xs text-[#888899] mt-1.5">
          Hold a modifier (Alt, Ctrl, Shift) then press a key.
        </p>
      </Section>

      {/* Language */}
      <Section title="Language">
        <div className="flex flex-col gap-2">
          {LANGUAGES.map((lang) => (
            <RadioOption
              key={lang.value}
              label={lang.label}
              checked={draft.language === lang.value}
              onChange={() => setDraft((d) => ({ ...d, language: lang.value }))}
            />
          ))}
        </div>
      </Section>

      {/* Cleanup mode */}
      <Section title="Cleanup mode">
        <div className="flex flex-col gap-2">
          {CLEANUP_MODES.map((mode) => (
            <RadioOption
              key={mode.value}
              label={mode.label}
              description={mode.description}
              checked={draft.cleanupMode === mode.value}
              onChange={() =>
                setDraft((d) => ({ ...d, cleanupMode: mode.value }))
              }
            />
          ))}
        </div>
      </Section>

      {/* Save button */}
      <button
        onClick={save}
        disabled={saving}
        className={`w-full py-2.5 rounded-lg text-sm font-medium transition-all
                    ${
                      saved
                        ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                        : "bg-indigo-600 hover:bg-indigo-500 text-white border border-transparent"
                    }
                    disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {saving ? "Saving..." : saved ? "Saved ✓" : "Save settings"}
      </button>
    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col gap-2">
      <p className="text-xs font-medium text-[#888899] uppercase tracking-widest">
        {title}
      </p>
      {children}
    </div>
  );
}

function RadioOption({
  label,
  description,
  checked,
  onChange,
}: {
  label: string;
  description?: string;
  checked: boolean;
  onChange: () => void;
}) {
  return (
    <button
      onClick={onChange}
      className={`flex items-center gap-3 w-full px-3 py-2.5 rounded-lg border
                  text-left transition-all
                  ${
                    checked
                      ? "border-indigo-500/50 bg-indigo-500/10"
                      : "border-white/10 bg-[#1A1A24] hover:border-white/20"
                  }`}
    >
      <span
        className={`w-4 h-4 rounded-full border-2 flex-shrink-0 flex items-center
                    justify-center transition-colors
                    ${checked ? "border-indigo-500" : "border-white/20"}`}
      >
        {checked && (
          <span className="w-2 h-2 rounded-full bg-indigo-500 block" />
        )}
      </span>
      <span className="flex flex-col">
        <span className="text-sm text-white">{label}</span>
        {description && (
          <span className="text-xs text-[#888899]">{description}</span>
        )}
      </span>
    </button>
  );
}

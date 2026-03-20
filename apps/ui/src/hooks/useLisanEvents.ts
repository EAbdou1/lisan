import { useEffect } from "react";
import { useLisanStore } from "../store";
import type { AppStatus, Transcript } from "../types/bridge";

export function useLisanEvents() {
  const { setStatus, setTranscript, setError } = useLisanStore();

  useEffect(() => {
    // Global handler Python calls via window.lisanEvent()
    window.lisanEvent = (event: string, data: unknown) => {
      switch (event) {
        case "status":
          setStatus(data as AppStatus);
          break;

        case "transcript":
          setTranscript(data as Transcript);
          break;

        case "error":
          setError(data as string);
          break;

        default:
          console.warn("Unknown lisan event:", event, data);
      }
    };

    return () => {
      // Cleanup — replace with no-op on unmount
      window.lisanEvent = () => {};
    };
  }, [setStatus, setTranscript, setError]);
}

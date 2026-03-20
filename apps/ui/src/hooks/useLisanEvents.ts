import { useEffect } from "react";
import { useLisanStore } from "../store";
import type { AppStatus, Transcript } from "../types/bridge";
import type { Tab } from "../store";

export function useLisanEvents() {
  const { setStatus, setTranscript, setError } = useLisanStore();

  useEffect(() => {
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

        case "navigate":
          useLisanStore.getState().setActiveTab(data as Tab);
          break;

        default:
          console.warn("Unknown lisan event:", event, data);
      }
    };

    return () => {
      window.lisanEvent = () => {};
    };
  }, [setStatus, setTranscript, setError]);
}

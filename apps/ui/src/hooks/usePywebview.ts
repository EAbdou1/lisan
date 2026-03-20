import { useEffect, useState } from "react";
import type { PyWebviewAPI } from "../types/bridge";

export function usePywebview() {
  const [ready, setReady] = useState(false);
  const [api, setApi] = useState<PyWebviewAPI | null>(null);

  useEffect(() => {
    const init = () => {
      setApi(window.pywebview.api);
      setReady(true);
    };

    // Already loaded
    if (window.pywebview) {
      init();
      return;
    }

    // Wait for pywebview to fire ready event
    window.addEventListener("pywebviewready", init);
    return () => window.removeEventListener("pywebviewready", init);
  }, []);

  return { api, ready };
}

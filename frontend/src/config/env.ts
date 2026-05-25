const DEFAULT_API_BASE_URL = "http://localhost:8000";
const DEFAULT_API_VERSION = "v1";
const DEFAULT_APP_NAME = "NeSy Diagnostic Client";

function trimTrailingSlash(value: string): string {
  return value.replace(/\/+$/, "");
}

export const env = {
  appName: import.meta.env.VITE_APP_NAME || DEFAULT_APP_NAME,
  apiBaseUrl: trimTrailingSlash(
    import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
  ),
  apiVersion: import.meta.env.VITE_API_VERSION || DEFAULT_API_VERSION,
} as const;

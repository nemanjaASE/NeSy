import { env } from "./env";

export const apiConfig = {
  baseUrl: env.apiBaseUrl,
  version: env.apiVersion,
  routes: {
    health: "/health",
    diagnose: `/api/${env.apiVersion}/diagnostics/diagnose`,
  },
} as const;

export function buildApiUrl(path: string): string {
  return `${apiConfig.baseUrl}${path}`;
}

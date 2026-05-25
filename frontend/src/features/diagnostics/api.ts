import { apiConfig } from "@/config";
import { apiRequest } from "@/lib";
import type { DiagnosticRequest, DiagnosticResponse } from "./types";

export function runDiagnosis(
  payload: DiagnosticRequest
): Promise<DiagnosticResponse> {
  return apiRequest<DiagnosticResponse>(apiConfig.routes.diagnose, {
    method: "POST",
    body: payload,
  });
}

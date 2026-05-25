import { buildApiUrl } from "@/config";

type RequestOptions = Omit<RequestInit, "body"> & {
  body?: unknown;
};

async function parseResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    return (await response.text()) as T;
  }

  return (await response.json()) as T;
}

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {}
): Promise<T> {
  const headers = new Headers(options.headers);

  if (options.body !== undefined && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(buildApiUrl(path), {
    ...options,
    headers,
    body:
      options.body === undefined ? undefined : JSON.stringify(options.body),
  });

  if (!response.ok) {
    const errorBody = await parseResponse<unknown>(response);
    throw new Error(
      typeof errorBody === "string"
        ? errorBody
        : `Request failed with status ${response.status}`
    );
  }

  return parseResponse<T>(response);
}

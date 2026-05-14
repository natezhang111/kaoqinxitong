import http from "./http";

export async function fetchSystemHealth() {
  const { data } = await http.get("/system/health");
  return data;
}

export async function fetchSystemSummary() {
  const { data } = await http.get("/system/summary");
  return data;
}

export async function fetchModelStatus() {
  const { data } = await http.get("/system/model-status");
  return data;
}

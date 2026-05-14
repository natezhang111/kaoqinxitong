import http from "./http";

export async function fetchStatisticsReport() {
  const { data } = await http.get("/statistics/report");
  return data;
}

export async function fetchStatisticsDashboard() {
  const { data } = await http.get("/statistics/dashboard");
  return data;
}

export async function fetchActivityFrequency() {
  const { data } = await http.get("/statistics/activity-frequency");
  return data;
}

export async function fetchActivityAccuracy() {
  const { data } = await http.get("/statistics/activity-accuracy");
  return data;
}

export async function exportStatisticsReport() {
  return await http.get("/statistics/report/export", {
    responseType: "blob",
  });
}

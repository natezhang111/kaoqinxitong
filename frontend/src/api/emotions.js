import http from "./http";

export async function fetchEmotionReport() {
  const { data } = await http.get("/emotions/report");
  return data;
}

export async function fetchEmotionRecords(params) {
  const { data } = await http.get("/emotions/records", { params });
  return data;
}

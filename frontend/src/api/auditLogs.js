import http from "./http";

export async function fetchAuditLogRecords(params) {
  const { data } = await http.get("/audit-logs/records", { params });
  return data;
}

export async function fetchAuditLogSummary(params) {
  const { data } = await http.get("/audit-logs/summary", { params });
  return data;
}
<<<<<<< HEAD
=======

export async function exportAuditLogRecords(params) {
  return await http.get("/audit-logs/records/export", {
    params,
    responseType: "blob",
  });
}
>>>>>>> 98bf8e49 (update)

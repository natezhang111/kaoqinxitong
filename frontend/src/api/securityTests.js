import http from "./http";

<<<<<<< HEAD
export async function runSecurityLivenessTest({ blobs, testType, remark }) {
=======
export async function runSecurityLivenessTest({ blobs, testType, remark, challengeId }) {
>>>>>>> 98bf8e49 (update)
  const formData = new FormData();
  blobs.forEach((blob, index) => {
    formData.append("files", blob, `security_${Date.now()}_${index + 1}.png`);
  });
  formData.append("test_type", testType);
  if (remark) {
    formData.append("remark", remark);
  }
<<<<<<< HEAD
=======
  if (challengeId) {
    formData.append("challenge_id", challengeId);
  }
>>>>>>> 98bf8e49 (update)
  const { data } = await http.post("/security-tests/liveness", formData);
  return data;
}

export async function fetchSecurityTestRecords(params) {
  const { data } = await http.get("/security-tests/records", { params });
  return data;
}

export async function fetchSecurityTestSummary(params) {
  const { data } = await http.get("/security-tests/summary", { params });
  return data;
}

export async function exportSecurityTestRecords(params) {
  const response = await http.get("/security-tests/export", {
    params,
    responseType: "blob",
  });
  return response;
}

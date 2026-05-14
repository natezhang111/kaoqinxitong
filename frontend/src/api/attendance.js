import http from "./http";

<<<<<<< HEAD
export async function checkinAttendance({ blobs, captureMode }) {
=======
export async function checkinAttendance({ blobs, captureMode, challengeId }) {
>>>>>>> 98bf8e49 (update)
  const formData = new FormData();
  blobs.forEach((blob, index) => {
    formData.append("files", blob, `capture_${Date.now()}_${index + 1}.png`);
  });
  formData.append("capture_mode", captureMode);
<<<<<<< HEAD
=======
  if (challengeId) {
    formData.append("challenge_id", challengeId);
  }
>>>>>>> 98bf8e49 (update)
  const { data } = await http.post("/attendance/checkin", formData);
  return data;
}

export async function fetchAttendanceRecords(params) {
  const { data } = await http.get("/attendance/records", { params });
  return data;
}

export async function exportAttendanceRecords(params) {
  const response = await http.get("/attendance/export", {
    params,
    responseType: "blob",
  });
  return response;
}

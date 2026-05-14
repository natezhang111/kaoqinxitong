import http from "./http";

export async function fetchStudents(params) {
  const { data } = await http.get("/students", { params });
  return data;
}

export async function createStudent(payload) {
  const { data } = await http.post("/students", payload);
  return data;
}

export async function updateStudent(studentId, payload) {
  const { data } = await http.put(`/students/${studentId}`, payload);
  return data;
}

export async function deleteStudent(studentId) {
  const { data } = await http.delete(`/students/${studentId}`);
  return data;
}

<<<<<<< HEAD
export async function importStudentsCsv(file) {
  const formData = new FormData();
  formData.append("file", file, file.name);
=======
export async function importStudentsCsv(file, photosZipFile = null) {
  const formData = new FormData();
  formData.append("file", file, file.name);
  if (photosZipFile) {
    formData.append("photos_zip", photosZipFile, photosZipFile.name);
  }
>>>>>>> 98bf8e49 (update)
  const { data } = await http.post("/students/import", formData);
  return data;
}

export async function uploadStudentFace(studentId, file) {
  const formData = new FormData();
  formData.append("file", file, file.name);
  const { data } = await http.post(`/students/${studentId}/face`, formData);
  return data;
}

export async function bindStudentAccount(studentId, payload = {}) {
  const { data } = await http.post(`/students/${studentId}/account/bind`, payload);
  return data;
}

export async function resetStudentAccountPassword(studentId, payload = {}) {
  const { data } = await http.post(
    `/students/${studentId}/account/reset-password`,
    payload
  );
  return data;
}

export async function fetchMyStudentProfile() {
  const { data } = await http.get("/students/me/profile");
  return data;
}

export async function fetchMyStudentActivities() {
  const { data } = await http.get("/students/me/activities");
  return data;
}

export async function fetchMyStudentEmotions() {
  const { data } = await http.get("/students/me/emotions");
  return data;
}

export async function fetchMyStudentGroupPhotoRecords() {
  const { data } = await http.get("/students/me/group-photo-records");
  return data;
}

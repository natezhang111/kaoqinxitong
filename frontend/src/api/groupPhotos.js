import http from "./http";

export async function recognizeGroupPhoto({
  file,
  title,
  activityType,
  activityDate,
}) {
  const formData = new FormData();
  formData.append("file", file, file.name);
  formData.append("title", title);
  formData.append("activity_type", activityType);
  if (activityDate) {
    formData.append("activity_date", activityDate);
  }
  const { data } = await http.post("/group-photos/recognize", formData);
  return data;
}

export async function fetchActivities(params) {
  const { data } = await http.get("/group-photos/activities", { params });
  return data;
}

export async function fetchActivityDetail(activityId) {
  const { data } = await http.get(`/group-photos/activities/${activityId}`);
  return data;
}

export async function fetchActivityParticipants(activityId, params) {
  const { data } = await http.get(
    `/group-photos/activities/${activityId}/participants`,
    { params }
  );
  return data;
}

export async function evaluateActivity(activityId, payload) {
  const { data } = await http.post(
    `/group-photos/activities/${activityId}/evaluate`,
    payload
  );
  return data;
}

export async function correctGroupPhotoFaceResult(activityId, faceResultId, payload) {
  const { data } = await http.patch(
    `/group-photos/activities/${activityId}/faces/${faceResultId}`,
    payload
  );
  return data;
}

export async function exportGroupPhotoActivity(activityId) {
  const response = await http.get(`/group-photos/activities/${activityId}/export`, {
    responseType: "blob",
  });
  return response;
}

import http from "./http";

export async function fetchUsers(params) {
  const { data } = await http.get("/users", { params });
  return data;
}

export async function fetchPermissionMatrix() {
  const { data } = await http.get("/users/permission-matrix");
  return data;
}

export async function fetchUser(userId) {
  const { data } = await http.get(`/users/${userId}`);
  return data;
}

export async function createUser(payload) {
  const { data } = await http.post("/users", payload);
  return data;
}

export async function updateUser(userId, payload) {
  const { data } = await http.put(`/users/${userId}`, payload);
  return data;
}

export async function resetUserPassword(userId, payload) {
  const { data } = await http.post(`/users/${userId}/reset-password`, payload);
  return data;
}

export async function deleteUser(userId) {
  const { data } = await http.delete(`/users/${userId}`);
  return data;
}

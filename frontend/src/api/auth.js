import http from "./http";

export async function login(payload) {
  const { data } = await http.post("/auth/login", payload);
  return data;
}

export async function fetchCurrentUser() {
  const { data } = await http.get("/auth/me");
  return data;
}

export async function changePassword(payload) {
  const { data } = await http.post("/auth/change-password", payload);
  return data;
}

export async function logout() {
  const { data } = await http.post("/auth/logout");
  return data;
}

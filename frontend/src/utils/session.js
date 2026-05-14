import { logout } from "../api/auth";

export function parseSavedUser() {
  const raw = localStorage.getItem("attendance_user");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function clearSession() {
  localStorage.removeItem("attendance_token");
  localStorage.removeItem("attendance_user");
}

export async function performLogout(router) {
  try {
    await logout();
  } catch (error) {
    if (error?.response?.status !== 401) {
      console.warn("Remote logout failed, clearing local session.", error);
    }
  } finally {
    clearSession();
    if (router?.currentRoute?.value?.name !== "login") {
      await router.push({ name: "login" });
    }
  }
}

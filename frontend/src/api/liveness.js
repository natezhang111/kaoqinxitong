import http from "./http";

export async function createLivenessChallenge({ purpose }) {
  const { data } = await http.post("/liveness/challenge", { purpose });
  return data;
}

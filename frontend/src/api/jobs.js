
import api from "./client";

export async function getJobs() {
  const response = await api.get("/jobs/");
  return response.data;
}

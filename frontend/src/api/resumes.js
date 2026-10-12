
import api from "./client";

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/resumes/", formData);
  return response.data;
}

export async function getResumes() {
  const response = await api.get("/resumes/");
  return response.data;
}


export async function analyzeResume(resumeId) {
  const response = await api.post(`/resumes/${resumeId}/analyze/`);
  return response.data;
}


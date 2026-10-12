
import { useCallback, useEffect, useState } from "react";
import Login from "./pages/Login";
import { getJobs } from "./api/jobs";
import { getResumes, analyzeResume } from "./api/resumes";
import ResumeUpload from "./components/ResumeUpload";
import api from "./api/client";

function getSkillName(skill) {
  if (typeof skill === "string") return skill;

  if (skill && typeof skill === "object") {
    return (
      skill.name ||
      skill.normalized_name ||
      skill.skill_name ||
      skill.title ||
      ""
    );
  }

  return "";
}

function App() {
  const [jobs, setJobs] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [analysisError, setAnalysisError] = useState("");
  const [analyzingId, setAnalyzingId] = useState(null);
  const [aiLoadingId, setAiLoadingId] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState({});

  const token = localStorage.getItem("access_token");

  const loadResumes = useCallback(async () => {
    const data = await getResumes();
    console.log("Resume API response:", data);

    const resumeList = Array.isArray(data) ? data : [];
    setResumes(resumeList);
    return resumeList;
  }, []);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    async function loadDashboard() {
      try {
        const [jobData, resumeData] = await Promise.all([
          getJobs(),
          getResumes(),
        ]);

        console.log("Jobs API response:", jobData);
        console.log("Resume API response:", resumeData);
        console.log("First resume object:", resumeData[0]);
        console.log("First resume skills:", resumeData[0]?.skills);
        console.log("First skill object:", resumeData[0]?.skills?.[0]);   
        setJobs(Array.isArray(jobData) ? jobData : []);
        setResumes(Array.isArray(resumeData) ? resumeData : []);
        setError("");
      } catch (err) {
        console.error("Dashboard loading error:", err);

        if (err.response?.status === 401) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          setError("Your session expired. Please sign in again.");
        } else {
          setError(
            err.response?.data?.detail ||
              "Could not load dashboard data."
          );
        }
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [token]);

  async function handleAnalyze(resumeId) {
    setAnalyzingId(resumeId);
    setAnalysisError("");

    try {
      const result = await analyzeResume(resumeId);
      console.log("Skill extraction result:", result);
      await loadResumes();
    } catch (err) {
      console.error("Skill extraction error:", err);
      setAnalysisError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Could not extract skills from this resume."
      );
    } finally {
      setAnalyzingId(null);
    }
  }

  async function handleAIAnalysis(resumeId) {
    setAiLoadingId(resumeId);
    setAnalysisError("");

    try {
      const response = await api.post(
        `/resumes/${resumeId}/llm-analysis/`
      );

      setAiAnalysis((previous) => ({
        ...previous,
        [resumeId]: response.data.analysis,
      }));
    } catch (err) {
      console.error("AI analysis error:", err);
      setAnalysisError(
        err.response?.data?.error ||
          err.response?.data?.detail ||
          "Could not generate AI analysis."
      );
    } finally {
      setAiLoadingId(null);
    }
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.reload();
  }

  if (!token) return <Login />;

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        Loading dashboard...
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 p-5 text-white md:p-10">
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-cyan-300">
            JobIntel AI
          </h1>
          <p className="mt-2 text-slate-400">
            Your AI-powered career assistant
          </p>
        </div>

        <button
          onClick={handleLogout}
          className="rounded-lg border border-slate-700 px-4 py-2 hover:border-cyan-400"
        >
          Log out
        </button>
      </header>

      {error && (
        <p role="alert" className="mb-5 rounded-lg bg-red-950 p-4 text-red-300">
          {error}
        </p>
      )}

      <ResumeUpload
        onUploaded={async () => {
          try {
            await loadResumes();
          } catch (err) {
            console.error(err);
            setError("Resume uploaded, but the list could not refresh.");
          }
        }}
      />

      <section className="mt-10">
        <h2 className="text-2xl font-semibold">My Resumes</h2>

        {analysisError && (
          <p role="alert" className="mt-3 rounded-lg bg-red-950 p-3 text-red-300">
            {analysisError}
          </p>
        )}

        {resumes.length === 0 ? (
          <p className="mt-4 text-slate-400">
            No resumes uploaded yet. Upload a PDF to get started.
          </p>
        ) : (
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            {resumes.map((resume) => {
              const skills = Array.isArray(resume.skills)
                ? resume.skills
                : [];

              const skillNames = skills
                .map(getSkillName)
                .filter(Boolean);

              return (
                <article
                  key={resume.id}
                  className="rounded-xl border border-slate-800 bg-slate-900 p-5"
                >
                  <h3 className="break-words text-lg font-semibold">
                    {resume.original_filename}
                  </h3>

                  <p className="mt-2 text-sm text-slate-400">
                    Uploaded:{" "}
                    {resume.uploaded_at
                      ? new Date(resume.uploaded_at).toLocaleDateString()
                      : "Date unavailable"}
                  </p>

                  <div className="mt-4">
                    <p className="text-sm text-slate-300">
                      Detected skills: {skills.length}
                    </p>

                    {skillNames.length > 0 ? (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {skillNames.map((name, index) => (
                          <span
                            key={`${name}-${index}`}
                            className="rounded-full bg-slate-800 px-3 py-1 text-xs text-cyan-300"
                          >
                            {name}
                          </span>
                        ))}
                      </div>
                    ) : skills.length > 0 ? (
                      <p className="mt-2 text-sm text-amber-300">
                        Skills were returned, but their names are missing.
                        Check the browser console for the API response.
                      </p>
                    ) : (
                      <p className="mt-2 text-sm text-slate-500">
                        No skills displayed yet. Click Extract Skills.
                      </p>
                    )}
                  </div>

                  <div className="mt-5 flex flex-wrap gap-3">
                    <button
                      onClick={() => handleAnalyze(resume.id)}
                      disabled={analyzingId === resume.id}
                      className="rounded-lg bg-cyan-400 px-4 py-2 font-semibold text-slate-950 disabled:opacity-50"
                    >
                      {analyzingId === resume.id
                        ? "Extracting..."
                        : "Extract Skills"}
                    </button>

                    <button
                      onClick={() => handleAIAnalysis(resume.id)}
                      disabled={aiLoadingId === resume.id}
                      className="rounded-lg border border-cyan-400 px-4 py-2 font-semibold text-cyan-300 disabled:opacity-50"
                    >
                      {aiLoadingId === resume.id
                        ? "Generating..."
                        : "AI Resume Analysis"}
                    </button>
                  </div>

                  {aiAnalysis[resume.id] && (
                    <div className="mt-6 space-y-4 border-t border-slate-700 pt-5">
                      <div>
                        <h4 className="font-semibold text-cyan-300">
                          Professional Summary
                        </h4>
                        <p className="mt-2 text-sm leading-6 text-slate-300">
                          {aiAnalysis[resume.id].summary}
                        </p>
                      </div>

                      {[
                        { title: "Strengths", key: "strengths" },
                        { title: "Areas to Improve", key: "weaknesses" },
                        { title: "Suggested Skills", key: "suggested_skills" },
                        { title: "Improvement Tips", key: "improvement_tips" },
                      ].map((section) => (
                        <div key={section.key}>
                          <h4 className="font-semibold">{section.title}</h4>
                          <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-slate-300">
                            {(aiAnalysis[resume.id][section.key] || []).map(
                              (item, index) => (
                                <li key={`${section.key}-${index}`}>{item}</li>
                              )
                            )}
                          </ul>
                        </div>
                      ))}
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        )}
      </section>

      <section className="mt-12">
        <h2 className="text-2xl font-semibold">Available Jobs</h2>

        {jobs.length === 0 ? (
          <p className="mt-4 text-slate-400">No jobs available yet.</p>
        ) : (
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            {jobs.map((job) => (
              <article
                key={job.id}
                className="rounded-xl border border-slate-800 bg-slate-900 p-5"
              >
                <h3 className="text-xl font-semibold">{job.title}</h3>
                <p className="mt-1 text-slate-400">{job.company}</p>
                <p className="mt-3 text-sm text-slate-300">
                  {job.location || "Location not specified"}
                </p>
                <p className="mt-3 text-sm text-slate-400">
                  Required skills:{" "}
                  {job.required_skills?.join(", ") || "Not specified"}
                </p>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;

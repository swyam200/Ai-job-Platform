
import { useState } from "react";
import { uploadResume } from "../api/resumes";

function ResumeUpload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setMessage("Please select a PDF resume.");
      return;
    }

    if (file.type !== "application/pdf" &&
        !file.name.toLowerCase().endsWith(".pdf")) {
      setMessage("Only PDF files are allowed.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setMessage("File must be 5 MB or smaller.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const resume = await uploadResume(file);
      setMessage("Resume uploaded successfully!");
      setFile(null);
      event.target.reset();
      onUploaded?.(resume);
    } catch (error) {
      setMessage(
        error.response?.data?.file?.[0] ||
        error.response?.data?.detail ||
        "Upload failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border border-slate-800 bg-slate-900 p-5"
    >
      <h2 className="text-xl font-semibold">Upload Resume</h2>
      <p className="mt-1 text-sm text-slate-400">
        PDF only, up to 5 MB
      </p>

      <input
        type="file"
        accept=".pdf,application/pdf"
        onChange={(event) => setFile(event.target.files?.[0] || null)}
        className="mt-4 block w-full text-sm text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-4 file:py-2 file:font-semibold file:text-slate-950"
      />

      <button
        type="submit"
        disabled={loading}
        className="mt-4 rounded-lg bg-cyan-400 px-5 py-2 font-semibold text-slate-950 disabled:opacity-50"
      >
        {loading ? "Uploading..." : "Upload PDF"}
      </button>

      {message && (
        <p role="status" className="mt-3 text-sm text-cyan-300">
          {message}
        </p>
      )}
    </form>
  );
}

export default ResumeUpload;

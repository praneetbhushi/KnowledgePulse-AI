import {
  useState,
} from "react";

import {
  Upload,
  FileText,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

import api from "../api/axios";


export default function UploadDocument() {

  const [
    file,
    setFile,
  ] = useState<File | null>(null);

  const [
    uploading,
    setUploading,
  ] = useState(false);

  const [
    message,
    setMessage,
  ] = useState("");

  const [
    error,
    setError,
  ] = useState("");


  function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {

    const selectedFile =
      event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setMessage("");
    setError("");
  }


  async function handleUpload() {

    if (!file) {
      setError(
        "Please select a document first."
      );
      return;
    }

    try {

      setUploading(true);
      setMessage("");
      setError("");

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      await api.post(
        "/api/v1/documents/upload",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      setMessage(
        "Document uploaded successfully."
      );

      setFile(null);

    } catch (err) {

      console.error(
        "Upload error:",
        err
      );

      setError(
        "Document upload failed."
      );

    } finally {

      setUploading(false);

    }
  }


  return (

    <div style={styles.page}>

      <div style={styles.header}>

        <h1 style={styles.title}>
          Upload Document
        </h1>

        <p style={styles.subtitle}>
          Upload organizational documents
          for AI-powered analysis.
        </p>

      </div>


      <div style={styles.card}>

        <div style={styles.iconCircle}>
          <Upload size={30} />
        </div>

        <h2 style={styles.heading}>
          Upload your knowledge document
        </h2>

        <p style={styles.description}>
          Supported formats:
          PDF, DOCX, PPTX and TXT.
        </p>


        <label style={styles.dropZone}>

          <FileText
            size={42}
            style={{
              marginBottom: "15px",
            }}
          />

          <strong>
            {file
              ? file.name
              : "Choose a document"}
          </strong>

          <span style={styles.fileHint}>
            {file
              ? `${(
                  file.size / 1024
                ).toFixed(1)} KB`
              : "Click here to select a file"}
          </span>

          <input
            type="file"
            accept=".pdf,.docx,.pptx,.txt"
            onChange={handleFileChange}
            style={{
              display: "none",
            }}
          />

        </label>


        {file && (

          <div style={styles.selectedFile}>

            <FileText size={20} />

            <span>
              Selected: {file.name}
            </span>

          </div>

        )}


        <button
          onClick={handleUpload}
          disabled={
            !file || uploading
          }
          style={{
            ...styles.uploadButton,
            opacity:
              !file || uploading
                ? 0.6
                : 1,
          }}
        >

          <Upload size={19} />

          {uploading
            ? "Uploading..."
            : "Upload Document"}

        </button>


        {message && (

          <div style={styles.success}>

            <CheckCircle size={20} />

            {message}

          </div>

        )}


        {error && (

          <div style={styles.error}>

            <AlertCircle size={20} />

            {error}

          </div>

        )}

      </div>

    </div>
  );
}


const styles: Record<
  string,
  React.CSSProperties
> = {

  page: {
    minHeight: "100vh",
    padding: "40px",
    background: "#f5f7fb",
    fontFamily:
      "Inter, Arial, sans-serif",
  },

  header: {
    marginBottom: "30px",
  },

  title: {
    margin: 0,
    fontSize: "32px",
    fontWeight: 700,
  },

  subtitle: {
    marginTop: "8px",
    color: "#64748b",
  },

  card: {
    maxWidth: "800px",
    margin: "0 auto",
    background: "#ffffff",
    borderRadius: "20px",
    border: "1px solid #e2e8f0",
    padding: "45px",
    textAlign: "center",
    boxShadow:
      "0 8px 25px rgba(0,0,0,0.05)",
  },

  iconCircle: {
    width: "65px",
    height: "65px",
    margin: "0 auto 20px",
    borderRadius: "50%",
    background: "#eff6ff",
    color: "#2563eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },

  heading: {
    margin: 0,
    fontSize: "24px",
  },

  description: {
    color: "#64748b",
    marginBottom: "30px",
  },

  dropZone: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "220px",
    border:
      "2px dashed #93c5fd",
    borderRadius: "16px",
    background: "#eff6ff",
    color: "#2563eb",
    cursor: "pointer",
    padding: "30px",
  },

  fileHint: {
    marginTop: "8px",
    color: "#64748b",
    fontSize: "14px",
  },

  selectedFile: {
    marginTop: "18px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    color: "#475569",
  },

  uploadButton: {
    marginTop: "25px",
    display: "inline-flex",
    alignItems: "center",
    gap: "9px",
    background: "#2563eb",
    color: "#ffffff",
    border: "none",
    padding: "13px 25px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: "15px",
  },

  success: {
    marginTop: "20px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "8px",
    color: "#166534",
    background: "#dcfce7",
    padding: "12px",
    borderRadius: "10px",
  },

  error: {
    marginTop: "20px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "8px",
    color: "#991b1b",
    background: "#fee2e2",
    padding: "12px",
    borderRadius: "10px",
  },
};
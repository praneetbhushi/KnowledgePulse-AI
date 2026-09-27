import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  getDocumentIntelligence,
  type DocumentIntelligence as DocumentIntelligenceType,
} from "../api/documents";

export default function DocumentIntelligence() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [document, setDocument] =
    useState<DocumentIntelligenceType | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) {
      setError("Document ID is missing.");
      setLoading(false);
      return;
    }

    async function loadDocument() {
      try {
        setLoading(true);
        setError("");

        const data = await getDocumentIntelligence(Number(id));

        setDocument(data);
      } catch (err) {
        console.error("Document intelligence error:", err);
        setError("Failed to load document intelligence.");
      } finally {
        setLoading(false);
      }
    }

    loadDocument();
  }, [id]);

  if (loading) {
    return (
      <div style={{ padding: "40px" }}>
        <h1>Document Intelligence</h1>
        <p>Loading document intelligence...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "40px" }}>
        <h1>Document Intelligence</h1>

        <p style={{ color: "red" }}>{error}</p>

        <button
          onClick={() => navigate("/documents")}
          style={{
            marginTop: "15px",
            padding: "10px 20px",
            cursor: "pointer",
          }}
        >
          Back to Documents
        </button>
      </div>
    );
  }

  if (!document) {
    return (
      <div style={{ padding: "40px" }}>
        <h1>Document Intelligence</h1>
        <p>Document not found.</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "40px" }}>
      <button
        onClick={() => navigate("/documents")}
        style={{
          marginBottom: "25px",
          padding: "10px 18px",
          cursor: "pointer",
        }}
      >
        ← Back to Documents
      </button>

      <h1>Document Intelligence</h1>

      <p style={{ color: "#666" }}>
        AI-powered analysis of the uploaded document.
      </p>

      {/* Document Information */}
      <section
        style={{
          marginTop: "25px",
          padding: "25px",
          border: "1px solid #ddd",
          borderRadius: "10px",
        }}
      >
        <h2>Document Information</h2>

        <p>
          <strong>Document ID:</strong> #{document.document_id}
        </p>

        <p>
          <strong>Filename:</strong> {document.filename}
        </p>

        <p>
          <strong>File Type:</strong> {document.file_type}
        </p>

        <p>
          <strong>File Size:</strong>{" "}
          {(document.file_size / (1024 * 1024)).toFixed(2)} MB
        </p>

        <p>
          <strong>Status:</strong> {document.status}
        </p>

        <p>
          <strong>Uploaded By:</strong> User #{document.uploaded_by}
        </p>

        <p>
          <strong>Uploaded At:</strong>{" "}
          {new Date(document.uploaded_at).toLocaleString("en-IN")}
        </p>
      </section>

      {/* Classification */}
      <section
        style={{
          marginTop: "25px",
          padding: "25px",
          border: "1px solid #ddd",
          borderRadius: "10px",
        }}
      >
        <h2>Classification</h2>

        <p>
          <strong>Category:</strong>{" "}
          {document.category ?? "Not Classified"}
        </p>

        <p>
          <strong>Confidence:</strong>{" "}
          {document.classification_confidence !== null
            ? `${(
                document.classification_confidence * 100
              ).toFixed(1)}%`
            : "N/A"}
        </p>
      </section>

      {/* Quality */}
      <section
        style={{
          marginTop: "25px",
          padding: "25px",
          border: "1px solid #ddd",
          borderRadius: "10px",
        }}
      >
        <h2>Knowledge Quality</h2>

        <p>
          <strong>Quality Score:</strong>{" "}
          {document.quality.score !== null
            ? `${document.quality.score}/100`
            : "N/A"}
        </p>

        <p>
          <strong>Quality Level:</strong>{" "}
          {document.quality.level ?? "Not Available"}
        </p>
      </section>

      {/* Duplicate Detection */}
      <section
        style={{
          marginTop: "25px",
          padding: "25px",
          border: "1px solid #ddd",
          borderRadius: "10px",
        }}
      >
        <h2>Duplicate Detection</h2>

        <p>
          <strong>Duplicate:</strong>{" "}
          {document.duplicate.is_duplicate ? "Yes" : "No"}
        </p>

        {document.duplicate.is_duplicate && (
          <>
            <p>
              <strong>Duplicate Of:</strong>{" "}
              {document.duplicate.duplicate_of_document_id !== null
                ? `#${document.duplicate.duplicate_of_document_id}`
                : "N/A"}
            </p>

            <p>
              <strong>Similarity:</strong>{" "}
              {document.duplicate.similarity !== null
                ? `${(
                    document.duplicate.similarity * 100
                  ).toFixed(1)}%`
                : "N/A"}
            </p>
          </>
        )}
      </section>
    </div>
  );
}
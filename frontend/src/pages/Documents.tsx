import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  getDocuments,
  type Document,
} from "../api/documentApi";

export default function Documents() {

  const [documents, setDocuments] =
    useState<Document[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  async function loadDocuments() {

    try {

      setLoading(true);
      setError("");

      const data =
        await getDocuments();

      setDocuments(data);

    } catch (err) {

      console.error(err);

      setError(
        "Failed to load documents."
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {

    loadDocuments();

  }, []);


  function formatFileSize(
    bytes: number
  ) {

    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {

      return `${(
        bytes / 1024
      ).toFixed(1)} KB`;

    }

    return `${(
      bytes /
      (1024 * 1024)
    ).toFixed(1)} MB`;
  }


  return (

    <div
      style={{
        padding: "40px",
        minHeight: "100vh",
        background: "#f5f7fb",
      }}
    >

      <h1
        style={{
          marginBottom: "10px",
        }}
      >
        Documents
      </h1>

      <p
        style={{
          color: "#64748b",
          marginBottom: "30px",
        }}
      >
        View and manage your
        organizational knowledge documents.
      </p>


      {/* ========================= */}
      {/* Error Message */}
      {/* ========================= */}

      {error && (

        <div
          style={{
            padding: "15px",
            marginBottom: "20px",
            background: "#fee2e2",
            color: "#991b1b",
            borderRadius: "8px",
          }}
        >
          {error}
        </div>

      )}


      {/* ========================= */}
      {/* Documents Section */}
      {/* ========================= */}

      <div
        style={{
          background: "white",
          border: "1px solid #e2e8f0",
          borderRadius: "12px",
          padding: "25px",
          overflowX: "auto",
        }}
      >

        <h2
          style={{
            marginTop: 0,
            marginBottom: "20px",
          }}
        >
          Uploaded Documents
        </h2>


        {loading ? (

          <p>
            Loading documents...
          </p>

        ) : documents.length === 0 ? (

          <div
            style={{
              padding: "40px",
              textAlign: "center",
              color: "#64748b",
            }}
          >

            <h3>
              No documents uploaded yet.
            </h3>

            <p>
              Go to the Upload Document
              page to add a document.
            </p>

            <Link
              to="/upload"
              style={{
                display: "inline-block",
                marginTop: "15px",
                padding: "10px 18px",
                background: "#2563eb",
                color: "white",
                textDecoration: "none",
                borderRadius: "7px",
              }}
            >
              Upload Document
            </Link>

          </div>

        ) : (

          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
            }}
          >

            <thead>

              <tr>

                <th style={styles.th}>
                  ID
                </th>

                <th style={styles.th}>
                  Filename
                </th>

                <th style={styles.th}>
                  Category
                </th>

                <th style={styles.th}>
                  Status
                </th>

                <th style={styles.th}>
                  Size
                </th>

                <th style={styles.th}>
                  Action
                </th>

              </tr>

            </thead>


            <tbody>

              {documents.map(
                (doc) => (

                  <tr
                    key={doc.id}
                    style={{
                      borderTop:
                        "1px solid #e2e8f0",
                    }}
                  >

                    <td style={styles.td}>
                      {doc.id}
                    </td>


                    <td style={styles.td}>

                      <strong>
                        {doc.original_filename ||
                          doc.filename}
                      </strong>

                    </td>


                    <td
                      style={{
                        ...styles.td,
                        textAlign: "center",
                      }}
                    >
                      {doc.category ||
                        "Unclassified"}
                    </td>


                    <td
                      style={{
                        ...styles.td,
                        textAlign: "center",
                      }}
                    >

                      <span
                        style={{
                          display:
                            "inline-block",
                          padding:
                            "5px 10px",
                          borderRadius:
                            "20px",
                          background:
                            "#eff6ff",
                          color:
                            "#1d4ed8",
                          fontSize:
                            "13px",
                        }}
                      >
                        {doc.status}
                      </span>

                    </td>


                    <td
                      style={{
                        ...styles.td,
                        textAlign: "center",
                      }}
                    >
                      {formatFileSize(
                        doc.file_size
                      )}
                    </td>


                    <td
                      style={{
                        ...styles.td,
                        textAlign: "center",
                      }}
                    >

                      <Link
                        to={`/documents/intelligence/${doc.id}`}
                        style={{
                          display:
                            "inline-block",
                          padding:
                            "8px 15px",
                          background:
                            "#2563eb",
                          color:
                            "white",
                          textDecoration:
                            "none",
                          borderRadius:
                            "6px",
                          fontWeight:
                            500,
                        }}
                      >
                        AI Intelligence
                      </Link>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        )}

      </div>

    </div>
  );
}


const styles: Record<
  string,
  React.CSSProperties
> = {

  th: {
    padding: "14px",
    textAlign: "left",
    background: "#f8fafc",
    color: "#475569",
    fontWeight: 600,
  },

  td: {
    padding: "14px",
  },

};
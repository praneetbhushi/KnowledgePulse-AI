import { useState } from "react";
import api from "../api/axios";

export default function SemanticSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);

      const response = await api.post(
        "/api/v1/search/search",
        {
          query,
          top_k: 5,
        }
      );

      setResults(
        response.data.results || []
      );
    } catch (error) {
      console.error(
        "Semantic search failed:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">

      <h1 className="text-3xl font-bold mb-2">
        Semantic Search
      </h1>

      <p className="text-gray-600 mb-8">
        Search organizational knowledge using
        AI-powered semantic retrieval.
      </p>

      <div className="bg-white rounded-xl shadow p-6">

        <div className="flex gap-3">

          <input
            type="text"
            value={query}
            onChange={(e) =>
              setQuery(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSearch();
              }
            }}
            placeholder="Search your organizational knowledge..."
            className="flex-1 border rounded-lg px-4 py-3"
          />

          <button
            onClick={handleSearch}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg"
          >
            {loading
              ? "Searching..."
              : "Search"}
          </button>

        </div>

        <div className="mt-8 space-y-4">

          {results.map(
            (result, index) => (
              <div
                key={index}
                className="border rounded-lg p-5"
              >
                <h3 className="font-semibold">
                  {result.document_name ||
                    `Result ${index + 1}`}
                </h3>

                <p className="text-gray-600 mt-2">
                  {result.content ||
                    result.text ||
                    "No content available"}
                </p>
              </div>
            )
          )}

          {!loading &&
            results.length === 0 && (
              <p className="text-gray-500">
                Enter a query to search your
                organizational knowledge.
              </p>
            )}

        </div>

      </div>

    </div>
  );
}
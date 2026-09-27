import { useEffect, useState } from "react";
import type { CSSProperties } from "react";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import {
  getAnalyticsDashboard,
  getRecentSearches,
  getAnalyticsTrends,
  type AnalyticsDashboard,
  type RecentSearch,
  type AnalyticsTrend,
} from "../api/analytics";

import {
  Search,
  CheckCircle,
  Target,
  Zap,
} from "lucide-react";

export default function Analytics() {

  const [data, setData] =
    useState<AnalyticsDashboard | null>(null);

  const [recentSearches, setRecentSearches] =
    useState<RecentSearch[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [trends, setTrends] =
    useState<AnalyticsTrend[]>([]);

  useEffect(() => {
    loadAnalytics();
  }, []);

  async function loadAnalytics() {

    try {

      setLoading(true);
      setError("");

      const [
        dashboard,
        searches,
        trendData,
      ] = await Promise.all([
        getAnalyticsDashboard(),
        getRecentSearches(),
        getAnalyticsTrends(),
      ]);

      setData(dashboard);
      setRecentSearches(searches);
      setTrends(trendData);

    } catch (error) {

      console.error(
        "Analytics error:",
        error
      );

      setError(
        "Unable to load analytics data."
      );

    } finally {

      setLoading(false);

    }
  }

  if (loading) {

    return (
      <div style={styles.loading}>
        Loading analytics...
      </div>
    );

  }

  if (error) {

    return (
      <div style={styles.error}>

        <h2>Analytics Error</h2>

        <p>{error}</p>

        <button
          style={styles.refreshButton}
          onClick={loadAnalytics}
        >
          Retry
        </button>

      </div>
    );

  }

  if (!data) {
    return null;
  }

  const performanceData = [
    {
      name: "Search",
      time: data.average_search_time,
    },
    {
      name: "LLM",
      time: data.average_llm_time,
    },
    {
      name: "RAG",
      time: data.average_rag_time,
    },
  ];

  const answerData = [
    {
      name: "Answered",
      value: data.answered_searches,
    },
    {
      name: "Unanswered",
      value: data.unanswered_searches,
    },
  ];

  const activityData = (() => {

    const result = [];

    for (let i = 6; i >= 0; i--) {

      const date = new Date();

      date.setHours(0, 0, 0, 0);
      date.setDate(
        date.getDate() - i
      );

      const year =
        date.getFullYear();

      const month =
        String(
          date.getMonth() + 1
        ).padStart(2, "0");

      const day =
        String(
          date.getDate()
        ).padStart(2, "0");

      const dateKey =
        `${year}-${month}-${day}`;

      const existing =
        trends.find(
          (item) =>
            item.date === dateKey
        );

      result.push({

        date:
          date.toLocaleDateString(
            "en-IN",
            {
              day: "2-digit",
              month: "short",
            }
          ),

        searches:
          existing?.searches ?? 0,

        answered:
          existing?.answered ?? 0,

        unanswered:
          existing?.unanswered ?? 0,
      });
    }

    return result;

  })();

  return (
    <div style={styles.page}>

      {/* HEADER */}

      <div style={styles.header}>

        <div>

          <h1 style={styles.title}>
            KnowledgePulse AI
          </h1>

          <p style={styles.subtitle}>
            Knowledge Search & RAG Analytics
          </p>

        </div>

        <button
          style={styles.refreshButton}
          onClick={loadAnalytics}
        >
          ↻ Refresh
        </button>

      </div>

      {/* SEARCH ACTIVITY */}

      <div style={styles.fullChartCard}>

        <h2 style={styles.sectionTitle}>
          Search Activity
        </h2>

        <p style={styles.sectionSubtitle}>
          Search volume and answered queries
          over the last 7 days
        </p>

        <ResponsiveContainer
          width="100%"
          height={320}
        >

          <LineChart
            data={activityData}
          >

            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis
              dataKey="date"
            />

            <YAxis
              allowDecimals={false}
            />

            <Tooltip />

            <Legend />

            <Line
              type="monotone"
              dataKey="searches"
              stroke="#2563eb"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
              name="Total Searches"
            />

            <Line
              type="monotone"
              dataKey="answered"
              stroke="#16a34a"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
              name="Answered"
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

      {/* STAT CARDS */}

      <div style={styles.cardGrid}>

        <StatCard
          title="Total Searches"
          value={data.total_searches}
          icon={<Search size={22} />}
          description="Total knowledge queries"
        />

        <StatCard
          title="Answered Searches"
          value={data.answered_searches}
          icon={<CheckCircle size={22} />}
          description="Queries successfully answered"
        />

        <StatCard
          title="Answer Rate"
          value={`${data.answer_rate}%`}
          icon={<Target size={22} />}
          description="Percentage of queries answered"
        />

        <StatCard
          title="Average RAG Time"
          value={`${data.average_rag_time.toFixed(2)}s`}
          icon={<Zap size={22} />}
          description="Retrieval + AI generation"
        />

      </div>

      {/* PERFORMANCE CARDS */}

      <div style={styles.performanceGrid}>

        <PerformanceCard
          title="Average Search Time"
          value={data.average_search_time}
          unit="seconds"
        />

        <PerformanceCard
          title="Average LLM Time"
          value={data.average_llm_time}
          unit="seconds"
        />

        <PerformanceCard
          title="Average RAG Time"
          value={data.average_rag_time}
          unit="seconds"
        />

        <PerformanceCard
          title="Average Distance"
          value={data.average_distance}
          unit="semantic distance"
        />

      </div>

      {/* CHARTS */}

      <div style={styles.chartGrid}>

        {/* PERFORMANCE CHART */}

        <div style={styles.chartCard}>

          <h2 style={styles.sectionTitle}>
            Response Performance
          </h2>

          <p style={styles.sectionSubtitle}>
            Average processing time
          </p>

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <BarChart
              data={performanceData}
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="name"
              />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="time"
                fill="#2563eb"
                radius={[
                  6,
                  6,
                  0,
                  0,
                ]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

        {/* ANSWER QUALITY */}

        <div style={styles.chartCard}>

          <h2 style={styles.sectionTitle}>
            Answer Quality
          </h2>

          <p style={styles.sectionSubtitle}>
            Answered vs unanswered searches
          </p>

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <PieChart>

              <Pie
                data={answerData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >

                <Cell fill="#16a34a" />

                <Cell fill="#dc2626" />

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* RECENT SEARCHES */}

      <div style={styles.tableCard}>

        <div style={styles.tableHeader}>

          <div>

            <h2 style={styles.sectionTitle}>
              Recent Searches
            </h2>

            <p style={styles.sectionSubtitle}>
              Latest knowledge queries
            </p>

          </div>

          <span style={styles.countBadge}>
            {recentSearches.length} records
          </span>

        </div>

        <div style={styles.tableWrapper}>

          <table style={styles.table}>

            <thead>

              <tr>

                <th style={styles.th}>
                  Query
                </th>

                <th style={styles.th}>
                  Results
                </th>

                <th style={styles.th}>
                  Distance
                </th>

                <th style={styles.th}>
                  Search
                </th>

                <th style={styles.th}>
                  LLM
                </th>

                <th style={styles.th}>
                  RAG
                </th>

                <th style={styles.th}>
                  Status
                </th>

                <th style={styles.th}>
                  Date
                </th>

              </tr>

            </thead>

            <tbody>

              {recentSearches.length === 0 ? (

                <tr>

                  <td
                    colSpan={8}
                    style={{
                      padding: "40px",
                      textAlign: "center",
                      color: "#64748b",
                    }}
                  >
                    No searches found.
                  </td>

                </tr>

              ) : (

                recentSearches.map(
                  (search) => (

                    <tr
                      key={search.id}
                    >

                      <td
                        style={
                          styles.tdQuery
                        }
                      >
                        {search.query}
                      </td>

                      <td
                        style={
                          styles.td
                        }
                      >
                        {search.result_count}
                      </td>

                      <td
                        style={
                          styles.td
                        }
                      >
                        {search.best_distance !==
                        null
                          ? search.best_distance.toFixed(
                              3
                            )
                          : "—"}
                      </td>

                      <td
                        style={
                          styles.td
                        }
                      >
                        {formatTime(
                          search.search_time
                        )}
                      </td>

                      <td
                        style={
                          styles.td
                        }
                      >
                        {formatTime(
                          search.llm_time
                        )}
                      </td>

                      <td
                        style={
                          styles.td
                        }
                      >
                        {formatTime(
                          search.total_rag_time
                        )}
                      </td>

                      <td
                        style={
                          styles.td
                        }
                      >

                        {search.was_answered ===
                        true ? (

                          <span
                            style={
                              styles.successBadge
                            }
                          >
                            Answered
                          </span>

                        ) : search.was_answered ===
                          false ? (

                          <span
                            style={
                              styles.failedBadge
                            }
                          >
                            Unanswered
                          </span>

                        ) : (

                          <span
                            style={
                              styles.pendingBadge
                            }
                          >
                            Pending
                          </span>

                        )}

                      </td>

                      <td
                        style={
                          styles.td
                        }
                      >
                        {new Date(
                          search.searched_at
                        ).toLocaleString()}
                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}


/* ================================================= */
/* STAT CARD */
/* ================================================= */

function StatCard({
  title,
  value,
  icon,
  description,
}: {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  description: string;
}) {

  return (

    <div style={styles.statCard}>

      <div style={styles.statTop}>

        <div style={styles.statIcon}>
          {icon}
        </div>

        <span style={styles.statTitle}>
          {title}
        </span>

      </div>

      <div style={styles.statValue}>
        {value}
      </div>

      <div style={styles.statDescription}>
        {description}
      </div>

    </div>

  );
}


/* ================================================= */
/* PERFORMANCE CARD */
/* ================================================= */

function PerformanceCard({
  title,
  value,
  unit,
}: {
  title: string;
  value: number;
  unit: string;
}) {

  return (

    <div
      style={
        styles.performanceCard
      }
    >

      <p
        style={
          styles.performanceTitle
        }
      >
        {title}
      </p>

      <h3
        style={
          styles.performanceValue
        }
      >
        {value.toFixed(2)}
      </h3>

      <span
        style={
          styles.performanceUnit
        }
      >
        {unit}
      </span>

    </div>

  );
}


/* ================================================= */
/* HELPERS */
/* ================================================= */

const formatTime = (
  value: number | null | undefined
) => {

  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return `${value.toFixed(2)}s`;
};


/* ================================================= */
/* STYLES */
/* ================================================= */

const styles: Record<
  string,
  CSSProperties
> = {

  page: {
    minHeight: "100vh",
    padding: "32px",
    background: "#f8fafc",
    fontFamily:
      "Inter, Arial, sans-serif",
  },

  fullChartCard: {
    background: "white",
    padding: "25px",
    borderRadius: "14px",
    boxShadow:
      "0 4px 15px rgba(0,0,0,0.05)",
    marginBottom: "30px",
  },

  loading: {
    padding: "50px",
    fontSize: "20px",
  },

  error: {
    padding: "50px",
  },

  header: {
    display: "flex",
    justifyContent:
      "space-between",
    alignItems: "center",
    marginBottom: "32px",
    gap: "20px",
  },

  title: {
    margin: 0,
    fontSize: "30px",
    fontWeight: 700,
    color: "#0f172a",
  },

  subtitle: {
    marginTop: "8px",
    color: "#64748b",
    fontSize: "16px",
  },

  refreshButton: {
    border: "none",
    background: "#2563eb",
    color: "white",
    padding: "11px 18px",
    borderRadius: "9px",
    cursor: "pointer",
    fontSize: "14px",
    fontWeight: 600,
    boxShadow:
      "0 4px 10px rgba(37, 99, 235, 0.25)",
  },

  cardGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px",
    marginBottom: "25px",
  },

  statCard: {
    background: "white",
    padding: "24px",
    borderRadius: "16px",
    border:
      "1px solid #e2e8f0",
    boxShadow:
      "0 4px 18px rgba(15, 23, 42, 0.06)",
    transition:
      "transform 0.2s ease, box-shadow 0.2s ease",
  },

  statTop: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },

  statIcon: {
    width: "42px",
    height: "42px",
    borderRadius: "10px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#eff6ff",
    color: "#2563eb",
  },

  statTitle: {
    color: "#64748b",
    fontSize: "14px",
    fontWeight: 500,
  },

  statValue: {
    marginTop: "18px",
    fontSize: "30px",
    fontWeight: 700,
    color: "#0f172a",
  },

  statDescription: {
    marginTop: "6px",
    fontSize: "13px",
    color: "#94a3b8",
  },

  performanceGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px",
    marginBottom: "30px",
  },

  performanceCard: {
    background: "white",
    padding: "20px",
    borderRadius: "12px",
    border:
      "1px solid #e2e8f0",
  },

  performanceTitle: {
    margin: 0,
    color: "#64748b",
  },

  performanceValue: {
    margin: "10px 0 5px",
    fontSize: "24px",
  },

  performanceUnit: {
    fontSize: "13px",
    color: "#94a3b8",
  },

  chartGrid: {
    display: "grid",
    gridTemplateColumns:
      "minmax(0, 2fr) minmax(320px, 1fr)",
    gap: "25px",
    marginBottom: "30px",
  },

  chartCard: {
    background: "white",
    padding: "25px",
    borderRadius: "14px",
    boxShadow:
      "0 4px 15px rgba(0,0,0,0.05)",
  },

  sectionTitle: {
    margin: 0,
    fontSize: "20px",
    fontWeight: 600,
  },

  sectionSubtitle: {
    marginTop: "6px",
    color: "#64748b",
    fontSize: "14px",
  },

  tableCard: {
    background: "white",
    borderRadius: "14px",
    padding: "25px",
    boxShadow:
      "0 4px 15px rgba(0,0,0,0.05)",
  },

  tableHeader: {
    display: "flex",
    justifyContent:
      "space-between",
    alignItems: "center",
    marginBottom: "20px",
  },

  countBadge: {
    background: "#eff6ff",
    color: "#2563eb",
    padding: "7px 12px",
    borderRadius: "20px",
    fontSize: "13px",
  },

  tableWrapper: {
    overflowX: "auto",
  },

  table: {
    width: "100%",
    borderCollapse: "collapse",
  },

  /* UPDATED — TABLE HEADER */

  th: {
    textAlign: "left",
    padding: "14px 15px",
    background: "#f8fafc",
    color: "#475569",
    fontSize: "12px",
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: "0.04em",
    borderBottom:
      "1px solid #e2e8f0",
    whiteSpace: "nowrap",
  },

  /* UPDATED — TABLE CELLS */

  td: {
    padding: "15px",
    borderBottom:
      "1px solid #f1f5f9",
    fontSize: "14px",
    color: "#334155",
    whiteSpace: "nowrap",
  },

  /* UPDATED — QUERY CELL */

  tdQuery: {
    padding: "15px",
    borderBottom:
      "1px solid #f1f5f9",
    fontSize: "14px",
    fontWeight: 500,
    maxWidth: "350px",
    minWidth: "250px",
    wordBreak: "break-word",
    lineHeight: 1.5,
  },

  /* UPDATED — ANSWERED BADGE */

  successBadge: {
    display: "inline-block",
    background: "#dcfce7",
    color: "#15803d",
    padding: "5px 10px",
    borderRadius: "15px",
    fontSize: "12px",
    fontWeight: 600,
    whiteSpace: "nowrap",
  },

  /* UPDATED — UNANSWERED BADGE */

  failedBadge: {
    display: "inline-block",
    background: "#fee2e2",
    color: "#dc2626",
    padding: "5px 10px",
    borderRadius: "15px",
    fontSize: "12px",
    fontWeight: 600,
    whiteSpace: "nowrap",
  },

  /* UPDATED — PENDING BADGE */

  pendingBadge: {
    display: "inline-block",
    background: "#f1f5f9",
    color: "#64748b",
    padding: "5px 10px",
    borderRadius: "15px",
    fontSize: "12px",
    fontWeight: 600,
    whiteSpace: "nowrap",
  },

};
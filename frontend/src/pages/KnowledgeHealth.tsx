import {
  useEffect,
  useState,
} from "react";

import {
  Activity,
  FileText,
  Copy,
  CheckCircle,
  AlertTriangle,
} from "lucide-react";

import api from "../api/axios";


interface HealthData {
  total_documents: number;
  processed_documents: number;
  uploaded_documents: number;
  duplicate_documents: number;
  classified_documents: number;
  unclassified_documents: number;
  scored_documents: number;
  average_quality_score: number;
  high_quality_documents: number;
  medium_quality_documents: number;
  low_quality_documents: number;
}


export default function KnowledgeHealth() {

  const [
    data,
    setData,
  ] = useState<HealthData | null>(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");


  async function loadHealth() {

    try {

      setLoading(true);
      setError("");

      const response =
        await api.get(
          "/api/v1/knowledge-health/summary"
        );

      setData(response.data);

    } catch (err) {

      console.error(
        "Knowledge health error:",
        err
      );

      setError(
        "Unable to load knowledge health."
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {
    loadHealth();
  }, []);


  if (loading) {

    return (
      <div style={styles.loading}>
        Loading knowledge health...
      </div>
    );
  }


  if (error) {

    return (
      <div style={styles.page}>

        <h1>
          Knowledge Health
        </h1>

        <div style={styles.error}>
          {error}
        </div>

      </div>
    );
  }


  if (!data) {
    return null;
  }


  return (

    <div style={styles.page}>

      <div style={styles.header}>

        <div>

          <h1 style={styles.title}>
            Knowledge Health
          </h1>

          <p style={styles.subtitle}>
            Monitor the overall health,
            quality and completeness of
            organizational knowledge.
          </p>

        </div>

        <div style={styles.scoreCircle}>

          <Activity size={25} />

          <strong>
            {data.average_quality_score.toFixed(1)}
          </strong>

          <span>
            Health Score
          </span>

        </div>

      </div>


      <div style={styles.grid}>

        <HealthCard
          title="Total Documents"
          value={data.total_documents}
          icon={<FileText size={22} />}
        />

        <HealthCard
          title="Processed"
          value={data.processed_documents}
          icon={<CheckCircle size={22} />}
        />

        <HealthCard
          title="Duplicates"
          value={data.duplicate_documents}
          icon={<Copy size={22} />}
        />

        <HealthCard
          title="Classified"
          value={data.classified_documents}
          icon={<Activity size={22} />}
        />

      </div>


      <div style={styles.section}>

        <h2>
          Document Quality
        </h2>

        <div style={styles.qualityGrid}>

          <QualityCard
            title="High Quality"
            value={
              data.high_quality_documents
            }
            icon={
              <CheckCircle size={22} />
            }
          />

          <QualityCard
            title="Medium Quality"
            value={
              data.medium_quality_documents
            }
            icon={
              <Activity size={22} />
            }
          />

          <QualityCard
            title="Low Quality"
            value={
              data.low_quality_documents
            }
            icon={
              <AlertTriangle size={22} />
            }
          />

        </div>

      </div>


      <div style={styles.section}>

        <h2>
          Knowledge Coverage
        </h2>

        <div style={styles.coverage}>

          <CoverageRow
            label="Processed Documents"
            value={
              data.processed_documents
            }
            total={
              data.total_documents
            }
          />

          <CoverageRow
            label="Classified Documents"
            value={
              data.classified_documents
            }
            total={
              data.total_documents
            }
          />

          <CoverageRow
            label="Quality Scored"
            value={
              data.scored_documents
            }
            total={
              data.total_documents
            }
          />

        </div>

      </div>

    </div>
  );
}


function HealthCard({
  title,
  value,
  icon,
}: {
  title: string;
  value: number;
  icon: React.ReactNode;
}) {

  return (

    <div style={styles.card}>

      <div style={styles.cardTop}>

        <span>
          {title}
        </span>

        <div style={styles.iconBox}>
          {icon}
        </div>

      </div>

      <strong style={styles.cardValue}>
        {value}
      </strong>

    </div>
  );
}


function QualityCard({
  title,
  value,
  icon,
}: {
  title: string;
  value: number;
  icon: React.ReactNode;
}) {

  return (

    <div style={styles.qualityCard}>

      {icon}

      <div>

        <strong>
          {value}
        </strong>

        <span>
          {title}
        </span>

      </div>

    </div>
  );
}


function CoverageRow({
  label,
  value,
  total,
}: {
  label: string;
  value: number;
  total: number;
}) {

  const percentage =
    total > 0
      ? (value / total) * 100
      : 0;

  return (

    <div style={styles.coverageRow}>

      <div style={styles.coverageHeader}>

        <span>
          {label}
        </span>

        <strong>
          {value} / {total}
        </strong>

      </div>

      <div style={styles.progressBackground}>

        <div
          style={{
            ...styles.progress,
            width: `${percentage}%`,
          }}
        />

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

  loading: {
    padding: "50px",
    fontSize: "20px",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "35px",
  },

  title: {
    margin: 0,
    fontSize: "32px",
  },

  subtitle: {
    color: "#64748b",
    maxWidth: "700px",
  },

  scoreCircle: {
    width: "130px",
    height: "130px",
    borderRadius: "50%",
    background: "#ffffff",
    border: "8px solid #dbeafe",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    color: "#2563eb",
  },

  grid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(4, 1fr)",
    gap: "20px",
  },

  card: {
    background: "#ffffff",
    border: "1px solid #e2e8f0",
    borderRadius: "16px",
    padding: "22px",
  },

  cardTop: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    color: "#64748b",
  },

  iconBox: {
    width: "42px",
    height: "42px",
    borderRadius: "10px",
    background: "#eff6ff",
    color: "#2563eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },

  cardValue: {
    display: "block",
    marginTop: "18px",
    fontSize: "28px",
  },

  section: {
    background: "#ffffff",
    borderRadius: "16px",
    border: "1px solid #e2e8f0",
    padding: "25px",
    marginTop: "25px",
  },

  qualityGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(3, 1fr)",
    gap: "20px",
  },

  qualityCard: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    padding: "20px",
    background: "#f8fafc",
    borderRadius: "12px",
  },

  coverage: {
    marginTop: "20px",
  },

  coverageRow: {
    marginBottom: "22px",
  },

  coverageHeader: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "8px",
  },

  progressBackground: {
    height: "10px",
    background: "#e2e8f0",
    borderRadius: "10px",
    overflow: "hidden",
  },

  progress: {
    height: "100%",
    background: "#2563eb",
    borderRadius: "10px",
  },

  error: {
    background: "#fee2e2",
    color: "#991b1b",
    padding: "20px",
    borderRadius: "10px",
  },
};
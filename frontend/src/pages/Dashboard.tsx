import {
  useEffect,
  useState,
} from "react";

import type {
  CSSProperties,
  ReactNode,
} from "react";

import {
  Activity,
  BarChart3,
  Brain,
  CheckCircle2,
  FileText,
  MessageSquare,
  Search,
  Upload,
  Users,
  AlertTriangle,
  TrendingUp,
  Database,
} from "lucide-react";

import {
  useNavigate,
} from "react-router-dom";

import {
  getDashboardSummary,
} from "../api/dashboardApi";

import type {
  DashboardSummary,
} from "../types/dashboard";

import {
  useAuth,
} from "../context/AuthContext";


/* =========================================================
   PLATFORM SERVICES
========================================================= */

const services = [
  {
    title: "Documents",
    description:
      "Explore and manage organizational knowledge.",
    icon: FileText,
    path: "/documents",
    roles: [1, 2, 3],
  },

  {
    title: "Upload",
    description:
      "Add new knowledge documents to the platform.",
    icon: Upload,
    path: "/upload",
    roles: [1, 2, 3],
  },

  {
    title: "AI Chat",
    description:
      "Ask questions using your organization's knowledge.",
    icon: MessageSquare,
    path: "/chat",
    roles: [1, 2, 3],
  },

  {
    title: "Semantic Search",
    description:
      "Find knowledge using intelligent semantic retrieval.",
    icon: Search,
    path: "/semantic-search",
    roles: [1, 2, 3],
  },

  {
    title: "Analytics",
    description:
      "Understand knowledge usage and search behavior.",
    icon: BarChart3,
    path: "/analytics",
    roles: [1, 2],
  },

  {
    title: "Document Intelligence",
    description:
      "Inspect classification, quality and document insights.",
    icon: Brain,
    path: "/documents/intelligence/11",
    roles: [1, 2],
  },

  {
    title: "Knowledge Health",
    description:
      "Monitor knowledge quality and organizational gaps.",
    icon: Activity,
    path: "/knowledge-health",
    roles: [1, 2],
  },

  {
    title: "User Management",
    description:
      "Manage organizational users and access.",
    icon: Users,
    path: "/user-management",
    roles: [1],
  },
];


/* =========================================================
   MAIN DASHBOARD
========================================================= */

export default function Dashboard() {

  const {
    user,
    loading,
    logout,
  } = useAuth();

  const navigate = useNavigate();

  const [
    data,
    setData,
  ] = useState<DashboardSummary | null>(null);

  const [
    dashboardLoading,
    setDashboardLoading,
  ] = useState(true);

  const [
    profileOpen,
    setProfileOpen,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");


  /* =======================================================
     LOAD DASHBOARD
  ======================================================= */

  useEffect(() => {

    async function loadDashboard() {

      try {

        setDashboardLoading(true);
        setError("");

        const result =
          await getDashboardSummary();

        setData(result);

      } catch (err) {

        console.error(
          "Dashboard error:",
          err
        );

        setError(
          "Unable to load dashboard data."
        );

      } finally {

        setDashboardLoading(false);

      }
    }

    loadDashboard();

  }, []);


  /* =======================================================
     AUTH LOADING
  ======================================================= */

  if (loading || !user) {

    return (
      <div style={styles.loadingPage}>
        <div style={styles.loadingOrb}>
          <Activity size={28} />
        </div>

        <h2>
          Loading KnowledgePulse AI
        </h2>

        <p>
          Preparing your knowledge intelligence dashboard...
        </p>
      </div>
    );
  }


  /* =======================================================
     ERROR
  ======================================================= */

  if (error) {

    return (
      <div style={styles.loadingPage}>

        <AlertTriangle
          size={42}
        />

        <h2>
          Dashboard unavailable
        </h2>

        <p>
          {error}
        </p>

      </div>
    );
  }


  /* =======================================================
     DATA
  ======================================================= */

  const totalDocuments =
    data?.documents.total_documents ?? 0;

  const processedDocuments =
    data?.documents.processed_documents ?? 0;

  const failedDocuments =
    data?.documents.failed_documents ?? 0;

  const processingDocuments =
    data?.documents.processing_documents ?? 0;

  const duplicateDocuments =
    data?.documents.duplicate_documents ?? 0;

  const qualityScore =
    data?.quality.average_quality_score ?? 0;

  const totalSearches =
    data?.search_analytics.total_searches ?? 0;

  const successfulSearches =
    data?.search_analytics.successful_searches ?? 0;

  const weakSearches =
    data?.search_analytics.weak_searches ?? 0;

  const searchSuccessRate =
    data?.search_analytics.success_rate ?? 0;

  const totalGaps =
    data?.knowledge_gaps.total_gaps ?? 0;

  const highPriorityGaps =
    data?.knowledge_gaps.high_priority_gaps ?? 0;

  const mediumPriorityGaps =
    data?.knowledge_gaps.medium_priority_gaps ?? 0;

  const lowPriorityGaps =
    data?.knowledge_gaps.low_priority_gaps ?? 0;


  const visibleServices =
    services.filter(
      (service) =>
        service.roles.includes(
          user.role_id
        )
    );


  /* =======================================================
     HEALTH LEVEL
  ======================================================= */

  const healthLevel =
    getHealthLevel(
      qualityScore
    );


  return (

    <div style={styles.page}>

      {/* ===================================================
          TOP NAVIGATION
      =================================================== */}

      <header style={styles.header}>

        <div style={styles.brandArea}>

          <div style={styles.logoBox}>
            <Brain size={25} />
          </div>

          <div>

            <h1 style={styles.brandTitle}>
              KnowledgePulse AI
            </h1>

            <p style={styles.brandSubtitle}>
              Knowledge Intelligence Command Center
            </p>

          </div>

        </div>


        {/* PROFILE */}

        <div style={styles.profileContainer}>

          <button
            onClick={() =>
              setProfileOpen(
                !profileOpen
              )
            }
            style={styles.profileButton}
          >

            <div style={styles.avatar}>
              {user.name
                ?.charAt(0)
                .toUpperCase()}
            </div>

            <div style={styles.profileText}>

              <strong>
                {user.name}
              </strong>

              <span>
                {getRoleName(
                  user.role_id
                )}
              </span>

            </div>

          </button>


          {profileOpen && (

            <div style={styles.profileMenu}>

              <div style={styles.profileMenuHeader}>

                <strong>
                  {user.name}
                </strong>

                <span>
                  {user.email}
                </span>

              </div>

              <div style={styles.divider} />

              <button
                onClick={() => {
                  logout();
                  navigate("/login");
                }}
                style={styles.logoutButton}
              >
                Logout
              </button>

            </div>

          )}

        </div>

      </header>


      {/* ===================================================
          HERO
      =================================================== */}

      <section style={styles.hero}>

        <div>

          <span style={styles.eyebrow}>
            ORGANIZATIONAL KNOWLEDGE
          </span>

          <h2 style={styles.heroTitle}>
            Knowledge Intelligence
            <br />
            at a Glance
          </h2>

          <p style={styles.heroDescription}>
            Monitor document quality, search
            intelligence, knowledge gaps and
            organizational health from one place.
          </p>

        </div>


        <div style={styles.heroStats}>

          <MiniMetric
            label="Documents"
            value={totalDocuments}
            icon={<Database size={18} />}
          />

          <MiniMetric
            label="Processed"
            value={processedDocuments}
            icon={<CheckCircle2 size={18} />}
          />

          <MiniMetric
            label="Searches"
            value={totalSearches}
            icon={<Search size={18} />}
          />

        </div>

      </section>


      {/* ===================================================
          MAIN VISUALIZATION GRID
      =================================================== */}

      <section style={styles.mainGrid}>

        {/* KNOWLEDGE HEALTH */}

        <div style={styles.healthCard}>

          <div style={styles.cardHeader}>

            <div>

              <span style={styles.cardEyebrow}>
                KNOWLEDGE HEALTH
              </span>

              <h3 style={styles.cardTitle}>
                Organizational Health
              </h3>

            </div>

            <Activity
              size={22}
            />

          </div>


          <div style={styles.healthContent}>

            <div
              style={{
                ...styles.healthGauge,
                background:
                  `conic-gradient(
                    #6366f1 ${Math.min(
                      qualityScore,
                      100
                    ) * 3.6}deg,
                    #e2e8f0 0deg
                  )`,
              }}
            >

              <div style={styles.gaugeInner}>

                <strong>
                  {dashboardLoading
                    ? "..."
                    : `${qualityScore.toFixed(
                        1
                      )}%`}
                </strong>

                <span>
                  Health Score
                </span>

              </div>

            </div>


            <div style={styles.healthDetails}>

              <div style={styles.healthStatus}>

                <span
                  style={{
                    ...styles.statusDot,
                    background:
                      healthLevel.dot,
                  }}
                />

                <strong>
                  {healthLevel.label}
                </strong>

              </div>

              <p>
                Based on document quality,
                completeness and organizational
                knowledge coverage.
              </p>

              <div style={styles.healthMetric}>

                <span>
                  Quality Score
                </span>

                <strong>
                  {qualityScore.toFixed(1)}%
                </strong>

              </div>

            </div>

          </div>

        </div>


        {/* DOCUMENT STATUS */}

        <div style={styles.card}>

          <div style={styles.cardHeader}>

            <div>

              <span style={styles.cardEyebrow}>
                DOCUMENT PIPELINE
              </span>

              <h3 style={styles.cardTitle}>
                Document Status
              </h3>

            </div>

            <FileText size={22} />

          </div>


          <div style={styles.statusList}>

            <StatusBar
              label="Processed"
              value={processedDocuments}
              total={totalDocuments}
            />

            <StatusBar
              label="Processing"
              value={processingDocuments}
              total={totalDocuments}
            />

            <StatusBar
              label="Failed"
              value={failedDocuments}
              total={totalDocuments}
            />

            <StatusBar
              label="Duplicates"
              value={duplicateDocuments}
              total={totalDocuments}
            />

          </div>

        </div>

      </section>


      {/* ===================================================
          SECOND VISUALIZATION ROW
      =================================================== */}

      <section style={styles.threeGrid}>

        {/* QUALITY */}

        <div style={styles.card}>

          <div style={styles.cardHeader}>

            <div>

              <span style={styles.cardEyebrow}>
                QUALITY
              </span>

              <h3 style={styles.cardTitle}>
                Knowledge Quality
              </h3>

            </div>

            <Brain size={22} />

          </div>


          <QualityRow
            label="Excellent"
            value={
              data?.quality.excellent_documents ?? 0
            }
            total={totalDocuments}
          />

          <QualityRow
            label="Good"
            value={
              data?.quality.good_documents ?? 0
            }
            total={totalDocuments}
          />

          <QualityRow
            label="Fair"
            value={
              data?.quality.fair_documents ?? 0
            }
            total={totalDocuments}
          />

          <QualityRow
            label="Poor"
            value={
              data?.quality.poor_documents ?? 0
            }
            total={totalDocuments}
          />

        </div>


        {/* SEARCH INTELLIGENCE */}

        <div style={styles.card}>

          <div style={styles.cardHeader}>

            <div>

              <span style={styles.cardEyebrow}>
                SEARCH INTELLIGENCE
              </span>

              <h3 style={styles.cardTitle}>
                Search Performance
              </h3>

            </div>

            <TrendingUp size={22} />

          </div>


          <div style={styles.bigNumber}>
            {searchSuccessRate.toFixed(1)}%
          </div>

          <span style={styles.muted}>
            Search success rate
          </span>


          <div style={styles.searchStats}>

            <SearchStat
              label="Total"
              value={totalSearches}
            />

            <SearchStat
              label="Successful"
              value={successfulSearches}
            />

            <SearchStat
              label="Weak"
              value={weakSearches}
            />

          </div>

        </div>


        {/* KNOWLEDGE GAPS */}

        <div style={styles.card}>

          <div style={styles.cardHeader}>

            <div>

              <span style={styles.cardEyebrow}>
                KNOWLEDGE GAPS
              </span>

              <h3 style={styles.cardTitle}>
                Missing Knowledge
              </h3>

            </div>

            <AlertTriangle size={22} />

          </div>


          <div style={styles.gapNumber}>
            {totalGaps}
          </div>

          <span style={styles.muted}>
            Identified knowledge gaps
          </span>


          <div style={styles.gapList}>

            <GapRow
              label="High Priority"
              value={highPriorityGaps}
              type="high"
            />

            <GapRow
              label="Medium Priority"
              value={mediumPriorityGaps}
              type="medium"
            />

            <GapRow
              label="Low Priority"
              value={lowPriorityGaps}
              type="low"
            />

          </div>

        </div>

      </section>


      {/* ===================================================
          DEPARTMENT HEALTH
      =================================================== */}

      {data &&
        data.department_health.departments
          .length > 0 && (

        <section style={styles.card}>

          <div style={styles.cardHeader}>

            <div>

              <span style={styles.cardEyebrow}>
                ORGANIZATIONAL INTELLIGENCE
              </span>

              <h3 style={styles.cardTitle}>
                Department Knowledge Health
              </h3>

            </div>

            <BarChart3 size={22} />

          </div>


          <div style={styles.departmentList}>

            {data.department_health.departments.map(
              (department) => (

                <div
                  key={
                    department.department_id
                  }
                  style={
                    styles.departmentRow
                  }
                >

                  <div
                    style={
                      styles.departmentInfo
                    }
                  >

                    <strong>
                      {department.department_name}
                    </strong>

                    <span>
                      {
                        department.total_documents
                      } documents
                    </span>

                  </div>


                  <div
                    style={
                      styles.departmentBarArea
                    }
                  >

                    <div
                      style={
                        styles.departmentBarBackground
                      }
                    >

                      <div
                        style={{
                          ...styles.departmentBar,
                          width: `${Math.min(
                            department.knowledge_health_score,
                            100
                          )}%`,
                        }}
                      />

                    </div>

                  </div>


                  <strong
                    style={
                      styles.departmentScore
                    }
                  >
                    {department.knowledge_health_score.toFixed(
                      1
                    )}
                    %
                  </strong>

                </div>

              )
            )}

          </div>

        </section>

      )}


      {/* ===================================================
          PLATFORM SERVICES
      =================================================== */}

      <section>

        <div style={styles.servicesHeader}>

          <div>

            <span style={styles.cardEyebrow}>
              PLATFORM
            </span>

            <h2 style={styles.servicesTitle}>
              Intelligence Services
            </h2>

            <p style={styles.servicesSubtitle}>
              Access the capabilities available
              for your role.
            </p>

          </div>

        </div>


        <div style={styles.servicesGrid}>

          {visibleServices.map(
            (service) => {

              const Icon =
                service.icon;

              return (

                <button
                  key={service.title}
                  onClick={() =>
                    navigate(
                      service.path
                    )
                  }
                  style={styles.serviceCard}
                >

                  <div style={styles.serviceIcon}>
                    <Icon size={22} />
                  </div>

                  <div
                    style={
                      styles.serviceContent
                    }
                  >

                    <strong>
                      {service.title}
                    </strong>

                    <span>
                      {service.description}
                    </span>

                  </div>

                  <span
                    style={
                      styles.serviceArrow
                    }
                  >
                    →
                  </span>

                </button>

              );
            }
          )}

        </div>

      </section>

    </div>
  );
}


/* =========================================================
   COMPONENTS
========================================================= */

function MiniMetric({
  label,
  value,
  icon,
}: {
  label: string;
  value: number;
  icon: ReactNode;
}) {

  return (

    <div style={styles.miniMetric}>

      <div style={styles.miniIcon}>
        {icon}
      </div>

      <div>

        <strong>
          {value}
        </strong>

        <span>
          {label}
        </span>

      </div>

    </div>
  );
}


function StatusBar({
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
      ? Math.min(
          (value / total) * 100,
          100
        )
      : 0;

  return (

    <div style={styles.statusItem}>

      <div style={styles.statusHeader}>

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

      </div>

      <div style={styles.barBackground}>

        <div
          style={{
            ...styles.barFill,
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  );
}


function QualityRow({
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
      ? Math.min(
          (value / total) * 100,
          100
        )
      : 0;

  return (

    <div style={styles.qualityRow}>

      <div style={styles.qualityHeader}>

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

      </div>

      <div style={styles.qualityBackground}>

        <div
          style={{
            ...styles.qualityFill,
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  );
}


function SearchStat({
  label,
  value,
}: {
  label: string;
  value: number;
}) {

  return (

    <div style={styles.searchStat}>

      <strong>
        {value}
      </strong>

      <span>
        {label}
      </span>

    </div>
  );
}


function GapRow({
  label,
  value,
  type,
}: {
  label: string;
  value: number;
  type: "high" | "medium" | "low";
}) {

  const dotColor =
    type === "high"
      ? "#ef4444"
      : type === "medium"
        ? "#f59e0b"
        : "#22c55e";

  return (

    <div style={styles.gapRow}>

      <div style={styles.gapLabel}>

        <span
          style={{
            ...styles.gapDot,
            background: dotColor,
          }}
        />

        {label}

      </div>

      <strong>
        {value}
      </strong>

    </div>
  );
}


function getRoleName(
  roleId: number
) {

  if (roleId === 1) {
    return "Admin";
  }

  if (roleId === 2) {
    return "Manager";
  }

  return "Employee";
}


function getHealthLevel(
  score: number
) {

  if (score >= 80) {

    return {
      label: "Healthy",
      dot: "#22c55e",
    };
  }

  if (score >= 60) {

    return {
      label: "Moderate",
      dot: "#f59e0b",
    };
  }

  return {
    label: "Needs Attention",
    dot: "#ef4444",
  };
}


/* =========================================================
   STYLES
========================================================= */

const styles: Record<
  string,
  CSSProperties
> = {

  page: {
    minHeight: "100vh",
    padding: "28px 38px 60px",
    background:
      "linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f8fafc 100%)",
    fontFamily:
      "Inter, Arial, sans-serif",
    color: "#0f172a",
  },


  /* HEADER */

  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "30px",
  },

  brandArea: {
    display: "flex",
    alignItems: "center",
    gap: "13px",
  },

  logoBox: {
    width: "48px",
    height: "48px",
    borderRadius: "14px",
    background:
      "linear-gradient(135deg, #4f46e5, #7c3aed)",
    color: "#ffffff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow:
      "0 8px 20px rgba(79,70,229,0.25)",
  },

  brandTitle: {
    margin: 0,
    fontSize: "22px",
    fontWeight: 800,
    letterSpacing: "-0.5px",
  },

  brandSubtitle: {
    margin: "3px 0 0",
    color: "#64748b",
    fontSize: "13px",
  },


  /* PROFILE */

  profileContainer: {
    position: "relative",
  },

  profileButton: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    background: "#ffffff",
    border: "1px solid #e2e8f0",
    borderRadius: "14px",
    padding: "8px 13px",
    cursor: "pointer",
    boxShadow:
      "0 4px 15px rgba(15,23,42,0.04)",
  },

  avatar: {
    width: "38px",
    height: "38px",
    borderRadius: "11px",
    background:
      "linear-gradient(135deg, #4f46e5, #7c3aed)",
    color: "#ffffff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 700,
  },

  profileText: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    gap: "2px",
  },

  profileMenu: {
    position: "absolute",
    top: "calc(100% + 8px)",
    right: 0,
    width: "240px",
    background: "#ffffff",
    border:
      "1px solid #e2e8f0",
    borderRadius: "14px",
    padding: "10px",
    boxShadow:
      "0 18px 40px rgba(15,23,42,0.14)",
    zIndex: 100,
  },

  profileMenuHeader: {
    display: "flex",
    flexDirection: "column",
    gap: "4px",
    padding: "10px",
  },

  divider: {
    height: "1px",
    background: "#e2e8f0",
    margin: "4px 0",
  },

  logoutButton: {
    width: "100%",
    textAlign: "left",
    border: "none",
    background: "transparent",
    color: "#dc2626",
    padding: "11px",
    borderRadius: "9px",
    cursor: "pointer",
    fontWeight: 600,
  },


  /* HERO */

  hero: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "30px",
    padding: "32px",
    borderRadius: "24px",
    background:
      "linear-gradient(135deg, #111827, #312e81 60%, #4f46e5)",
    color: "#ffffff",
    marginBottom: "25px",
    boxShadow:
      "0 20px 45px rgba(49,46,129,0.18)",
  },

  eyebrow: {
    fontSize: "11px",
    letterSpacing: "1.8px",
    fontWeight: 700,
    opacity: 0.7,
  },

  heroTitle: {
    fontSize: "34px",
    lineHeight: 1.15,
    margin: "10px 0",
    letterSpacing: "-1px",
  },

  heroDescription: {
    maxWidth: "620px",
    margin: 0,
    color: "#cbd5e1",
    lineHeight: 1.6,
  },

  heroStats: {
    display: "flex",
    gap: "12px",
    flexWrap: "wrap",
  },

  miniMetric: {
    minWidth: "125px",
    display: "flex",
    alignItems: "center",
    gap: "10px",
    padding: "14px",
    border:
      "1px solid rgba(255,255,255,0.12)",
    background:
      "rgba(255,255,255,0.08)",
    borderRadius: "14px",
  },

  miniIcon: {
    width: "35px",
    height: "35px",
    borderRadius: "9px",
    background:
      "rgba(255,255,255,0.12)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },


  /* CARDS */

  mainGrid: {
    display: "grid",
    gridTemplateColumns:
      "1.25fr 1fr",
    gap: "20px",
    marginBottom: "20px",
  },

  threeGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(3, 1fr)",
    gap: "20px",
    marginBottom: "20px",
  },

  card: {
    background:
      "rgba(255,255,255,0.92)",
    border:
      "1px solid rgba(226,232,240,0.9)",
    borderRadius: "20px",
    padding: "24px",
    boxShadow:
      "0 8px 25px rgba(15,23,42,0.05)",
  },

  healthCard: {
    background:
      "linear-gradient(135deg, #ffffff, #f5f3ff)",
    border:
      "1px solid #e2e8f0",
    borderRadius: "20px",
    padding: "24px",
    boxShadow:
      "0 8px 25px rgba(15,23,42,0.05)",
  },

  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: "22px",
  },

  cardEyebrow: {
    display: "block",
    fontSize: "10px",
    letterSpacing: "1.5px",
    fontWeight: 800,
    color: "#6366f1",
  },

  cardTitle: {
    margin: "5px 0 0",
    fontSize: "19px",
    fontWeight: 700,
  },


  /* HEALTH */

  healthContent: {
    display: "flex",
    alignItems: "center",
    gap: "35px",
  },

  healthGauge: {
    width: "180px",
    height: "180px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },

  gaugeInner: {
    width: "140px",
    height: "140px",
    borderRadius: "50%",
    background: "#ffffff",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    boxShadow:
      "inset 0 0 20px rgba(99,102,241,0.06)",
  },

  healthDetails: {
    flex: 1,
  },

  healthStatus: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "18px",
  },

  statusDot: {
    width: "9px",
    height: "9px",
    borderRadius: "50%",
  },

  healthMetric: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "20px",
    paddingTop: "15px",
    borderTop:
      "1px solid #e2e8f0",
  },


  /* DOCUMENT STATUS */

  statusList: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },

  statusItem: {
    width: "100%",
  },

  statusHeader: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "8px",
    fontSize: "14px",
  },

  barBackground: {
    height: "9px",
    background: "#e2e8f0",
    borderRadius: "10px",
    overflow: "hidden",
  },

  barFill: {
    height: "100%",
    background:
      "linear-gradient(90deg, #6366f1, #8b5cf6)",
    borderRadius: "10px",
  },


  /* QUALITY */

  qualityRow: {
    marginBottom: "18px",
  },

  qualityHeader: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "7px",
    fontSize: "13px",
  },

  qualityBackground: {
    height: "8px",
    background: "#e2e8f0",
    borderRadius: "8px",
    overflow: "hidden",
  },

  qualityFill: {
    height: "100%",
    background:
      "linear-gradient(90deg, #4f46e5, #a855f7)",
    borderRadius: "8px",
  },


  /* SEARCH */

  bigNumber: {
    fontSize: "42px",
    fontWeight: 800,
    letterSpacing: "-2px",
    marginTop: "5px",
  },

  muted: {
    color: "#64748b",
    fontSize: "13px",
  },

  searchStats: {
    display: "grid",
    gridTemplateColumns:
      "repeat(3, 1fr)",
    gap: "10px",
    marginTop: "25px",
  },

  searchStat: {
    background: "#f8fafc",
    borderRadius: "12px",
    padding: "14px",
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },


  /* GAPS */

  gapNumber: {
    fontSize: "42px",
    fontWeight: 800,
    letterSpacing: "-2px",
  },

  gapList: {
    marginTop: "18px",
    display: "flex",
    flexDirection: "column",
    gap: "11px",
  },

  gapRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  gapLabel: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    color: "#475569",
    fontSize: "13px",
  },

  gapDot: {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
  },


  /* DEPARTMENTS */

  departmentList: {
    display: "flex",
    flexDirection: "column",
    gap: "18px",
  },

  departmentRow: {
    display: "grid",
    gridTemplateColumns:
      "190px 1fr 70px",
    alignItems: "center",
    gap: "20px",
  },

  departmentInfo: {
    display: "flex",
    flexDirection: "column",
    gap: "3px",
  },

  departmentBarArea: {
    width: "100%",
  },

  departmentBarBackground: {
    height: "11px",
    background: "#e2e8f0",
    borderRadius: "20px",
    overflow: "hidden",
  },

  departmentBar: {
    height: "100%",
    background:
      "linear-gradient(90deg, #6366f1, #8b5cf6)",
    borderRadius: "20px",
  },

  departmentScore: {
    textAlign: "right",
  },


  /* SERVICES */

  servicesHeader: {
    marginTop: "35px",
    marginBottom: "18px",
  },

  servicesTitle: {
    margin: "5px 0",
    fontSize: "26px",
  },

  servicesSubtitle: {
    margin: 0,
    color: "#64748b",
  },

  servicesGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(4, 1fr)",
    gap: "15px",
  },

  serviceCard: {
    display: "flex",
    alignItems: "center",
    gap: "13px",
    textAlign: "left",
    background: "#ffffff",
    border:
      "1px solid #e2e8f0",
    borderRadius: "16px",
    padding: "18px",
    cursor: "pointer",
    transition:
      "all 0.2s ease",
    boxShadow:
      "0 5px 18px rgba(15,23,42,0.04)",
  },

  serviceIcon: {
    width: "43px",
    height: "43px",
    borderRadius: "11px",
    background:
      "linear-gradient(135deg, #eef2ff, #f5f3ff)",
    color: "#4f46e5",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },

  serviceContent: {
    display: "flex",
    flexDirection: "column",
    gap: "5px",
    flex: 1,
  },

  serviceArrow: {
    color: "#6366f1",
    fontSize: "20px",
  },


  /* LOADING */

  loadingPage: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    background:
      "linear-gradient(135deg, #f8fafc, #eef2ff)",
    color: "#475569",
  },

  loadingOrb: {
    width: "65px",
    height: "65px",
    borderRadius: "20px",
    background:
      "linear-gradient(135deg, #4f46e5, #7c3aed)",
    color: "#ffffff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: "15px",
  },
};
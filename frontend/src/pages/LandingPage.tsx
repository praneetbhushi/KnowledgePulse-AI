import { Link } from "react-router-dom";
import {
  ArrowRight,
  Brain,
  CheckCircle2,
  Database,
  FileSearch,
  BarChart3,
  MessageSquare,
  ShieldCheck,
  Sparkles,
  Upload,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div style={styles.page}>
      {/* NAVBAR */}
      <nav style={styles.navbar}>
        <div style={styles.logoSection}>
          <div style={styles.logoIcon}>
            <Brain size={25} />
          </div>

          <div>
            <div style={styles.logoText}>KnowledgePulse AI</div>
            <div style={styles.logoSubtext}>Knowledge Intelligence Platform</div>
          </div>
        </div>

        <div style={styles.navLinks}>
          <a href="#features" style={styles.navLink}>
            Features
          </a>

          <a href="#how-it-works" style={styles.navLink}>
            How It Works
          </a>

          <a href="#technology" style={styles.navLink}>
            Technology
          </a>

          <Link to="/login" style={styles.signInButton}>
            Sign In
          </Link>
        </div>
      </nav>

      {/* HERO */}
      <section style={styles.hero}>
        <div style={styles.heroContent}>
          <div style={styles.badge}>
            <Sparkles size={16} />
            AI-Powered Enterprise Knowledge
          </div>

          <h1 style={styles.heroTitle}>
            Turn Organizational Knowledge
            <span style={styles.heroHighlight}> Into Intelligence</span>
          </h1>

          <p style={styles.heroDescription}>
            KnowledgePulse AI helps organizations upload, process, classify,
            search, analyze, and interact with their knowledge using
            Artificial Intelligence and Retrieval-Augmented Generation.
          </p>

          <div style={styles.heroButtons}>
            <Link to="/login" style={styles.primaryButton}>
              Get Started
              <ArrowRight size={19} />
            </Link>

            <a href="#features" style={styles.secondaryButton}>
              Explore Features
            </a>
          </div>

          <div style={styles.heroPoints}>
            <span>
              <CheckCircle2 size={17} />
              Secure Authentication
            </span>

            <span>
              <CheckCircle2 size={17} />
              AI-Powered Search
            </span>

            <span>
              <CheckCircle2 size={17} />
              RAG-Based Chat
            </span>
          </div>
        </div>

        {/* HERO VISUAL */}
        <div style={styles.heroVisual}>
          <div style={styles.dashboardCard}>
            <div style={styles.cardHeader}>
              <div>
                <div style={styles.cardTitle}>Knowledge Intelligence</div>
                <div style={styles.cardSubtitle}>
                  Organizational knowledge overview
                </div>
              </div>

              <div style={styles.statusDot}>●</div>
            </div>

            <div style={styles.metricGrid}>
              <MetricCard
                icon={<Database size={20} />}
                value="Documents"
                label="Knowledge Repository"
              />

              <MetricCard
                icon={<FileSearch size={20} />}
                value="Semantic"
                label="Intelligent Search"
              />

              <MetricCard
                icon={<MessageSquare size={20} />}
                value="AI Chat"
                label="RAG Assistant"
              />

              <MetricCard
                icon={<BarChart3 size={20} />}
                value="Analytics"
                label="Knowledge Insights"
              />
            </div>

            <div style={styles.aiPanel}>
              <div style={styles.aiIcon}>
                <Brain size={20} />
              </div>

              <div>
                <strong>AI Knowledge Assistant</strong>
                <p>
                  Ask questions and receive answers grounded in your
                  organization's documents.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" style={styles.section}>
        <div style={styles.sectionHeading}>
          <div style={styles.sectionBadge}>PLATFORM FEATURES</div>

          <h2 style={styles.sectionTitle}>
            Everything your knowledge needs
          </h2>

          <p style={styles.sectionDescription}>
            A complete platform for managing, understanding, searching, and
            improving organizational knowledge.
          </p>
        </div>

        <div style={styles.featureGrid}>
          <FeatureCard
            icon={<Upload size={24} />}
            title="Document Management"
            description="Upload and manage PDF, DOCX, PPTX, and TXT documents in a centralized knowledge repository."
          />

          <FeatureCard
            icon={<Brain size={24} />}
            title="AI Document Processing"
            description="Automatically extract, clean, classify, chunk, and generate embeddings from uploaded documents."
          />

          <FeatureCard
            icon={<FileSearch size={24} />}
            title="Semantic Search"
            description="Find relevant information using semantic and hybrid search instead of relying only on keywords."
          />

          <FeatureCard
            icon={<MessageSquare size={24} />}
            title="RAG AI Assistant"
            description="Ask questions about organizational knowledge and receive document-grounded AI responses."
          />

          <FeatureCard
            icon={<BarChart3 size={24} />}
            title="Knowledge Analytics"
            description="Monitor search activity, answer rates, document quality, and knowledge usage."
          />

          <FeatureCard
            icon={<ShieldCheck size={24} />}
            title="Secure Access"
            description="JWT authentication and role-based access provide controlled access to the platform."
          />
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how-it-works" style={styles.workflowSection}>
        <div style={styles.sectionHeading}>
          <div style={styles.sectionBadge}>HOW IT WORKS</div>

          <h2 style={styles.sectionTitle}>From documents to intelligence</h2>

          <p style={styles.sectionDescription}>
            KnowledgePulse AI transforms raw organizational documents into
            searchable and intelligent knowledge.
          </p>
        </div>

        <div style={styles.workflow}>
          <WorkflowStep
            number="01"
            title="Upload"
            description="Upload organizational documents."
          />

          <WorkflowStep
            number="02"
            title="Process"
            description="Extract and clean document content."
          />

          <WorkflowStep
            number="03"
            title="Understand"
            description="Classify, chunk and generate embeddings."
          />

          <WorkflowStep
            number="04"
            title="Search"
            description="Retrieve relevant knowledge semantically."
          />

          <WorkflowStep
            number="05"
            title="Ask AI"
            description="Generate grounded answers using RAG."
          />
        </div>
      </section>

      {/* TECHNOLOGY */}
      <section id="technology" style={styles.section}>
        <div style={styles.sectionHeading}>
          <div style={styles.sectionBadge}>TECHNOLOGY</div>

          <h2 style={styles.sectionTitle}>Built with modern AI technology</h2>

          <p style={styles.sectionDescription}>
            KnowledgePulse AI combines modern web engineering, databases,
            vector search, machine learning, and generative AI.
          </p>
        </div>

        <div style={styles.techGrid}>
          {[
            "React + TypeScript",
            "FastAPI",
            "PostgreSQL",
            "ChromaDB",
            "RAG",
            "Sentence Transformers",
            "JWT Authentication",
            "Machine Learning",
          ].map((technology) => (
            <div key={technology} style={styles.techCard}>
              <CheckCircle2 size={18} />
              <span>{technology}</span>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section style={styles.ctaSection}>
        <div>
          <div style={styles.ctaBadge}>
            <Sparkles size={16} />
            KnowledgePulse AI
          </div>

          <h2 style={styles.ctaTitle}>
            Make your organizational knowledge intelligent.
          </h2>

          <p style={styles.ctaDescription}>
            Upload documents, search knowledge, ask AI questions, and analyze
            your organization's knowledge ecosystem.
          </p>
        </div>

        <Link to="/login" style={styles.ctaButton}>
          Launch Platform
          <ArrowRight size={19} />
        </Link>
      </section>

      {/* FOOTER */}
      <footer style={styles.footer}>
        <div>
          <strong>KnowledgePulse AI</strong>
          <span> — Enterprise Knowledge Health & Intelligence Platform</span>
        </div>

        <div>AI • RAG • Knowledge Intelligence</div>
      </footer>
    </div>
  );
}

/* ---------- COMPONENTS ---------- */

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div style={styles.featureCard}>
      <div style={styles.featureIcon}>{icon}</div>

      <h3 style={styles.featureTitle}>{title}</h3>

      <p style={styles.featureDescription}>{description}</p>
    </div>
  );
}

function MetricCard({
  icon,
  value,
  label,
}: {
  icon: React.ReactNode;
  value: string;
  label: string;
}) {
  return (
    <div style={styles.metricCard}>
      <div style={styles.metricIcon}>{icon}</div>
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function WorkflowStep({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div style={styles.workflowStep}>
      <div style={styles.workflowNumber}>{number}</div>

      <h3>{title}</h3>

      <p>{description}</p>
    </div>
  );
}

/* ---------- STYLES ---------- */

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    background:
      "linear-gradient(180deg, #07111f 0%, #0a1628 45%, #f8fafc 45%, #f8fafc 100%)",
    color: "#0f172a",
    fontFamily:
      "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
  },

  navbar: {
    height: 78,
    padding: "0 7%",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    color: "white",
    borderBottom: "1px solid rgba(255,255,255,0.08)",
  },

  logoSection: {
    display: "flex",
    alignItems: "center",
    gap: 12,
  },

  logoIcon: {
    width: 42,
    height: 42,
    borderRadius: 12,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "linear-gradient(135deg, #6366f1, #06b6d4)",
  },

  logoText: {
    fontSize: 18,
    fontWeight: 800,
  },

  logoSubtext: {
    fontSize: 10,
    opacity: 0.6,
    marginTop: 2,
  },

  navLinks: {
    display: "flex",
    alignItems: "center",
    gap: 30,
  },

  navLink: {
    color: "#cbd5e1",
    textDecoration: "none",
    fontSize: 14,
    fontWeight: 500,
  },

  signInButton: {
    textDecoration: "none",
    color: "white",
    padding: "10px 19px",
    borderRadius: 9,
    border: "1px solid rgba(255,255,255,0.2)",
    fontSize: 14,
    fontWeight: 600,
  },

  hero: {
    maxWidth: 1250,
    margin: "0 auto",
    padding: "90px 6% 110px",
    display: "grid",
    gridTemplateColumns: "1.05fr 0.95fr",
    gap: 70,
    alignItems: "center",
    color: "white",
  },

  heroContent: {
    maxWidth: 650,
  },

  badge: {
    display: "inline-flex",
    alignItems: "center",
    gap: 8,
    padding: "8px 13px",
    borderRadius: 999,
    background: "rgba(99,102,241,0.14)",
    border: "1px solid rgba(129,140,248,0.3)",
    color: "#c7d2fe",
    fontSize: 12,
    fontWeight: 700,
    marginBottom: 24,
  },

  heroTitle: {
    fontSize: "clamp(42px, 5vw, 68px)",
    lineHeight: 1.05,
    letterSpacing: "-2.5px",
    margin: 0,
    fontWeight: 850,
  },

  heroHighlight: {
    display: "block",
    background: "linear-gradient(90deg, #818cf8, #22d3ee)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },

  heroDescription: {
    color: "#94a3b8",
    fontSize: 18,
    lineHeight: 1.75,
    margin: "27px 0",
    maxWidth: 620,
  },

  heroButtons: {
    display: "flex",
    gap: 14,
    flexWrap: "wrap",
  },

  primaryButton: {
    display: "inline-flex",
    alignItems: "center",
    gap: 9,
    padding: "14px 22px",
    borderRadius: 10,
    background: "linear-gradient(135deg, #6366f1, #06b6d4)",
    color: "white",
    textDecoration: "none",
    fontWeight: 700,
    boxShadow: "0 12px 30px rgba(79,70,229,0.28)",
  },

  secondaryButton: {
    padding: "14px 22px",
    borderRadius: 10,
    border: "1px solid rgba(255,255,255,0.16)",
    color: "#e2e8f0",
    textDecoration: "none",
    fontWeight: 600,
  },

  heroPoints: {
    display: "flex",
    gap: 20,
    flexWrap: "wrap",
    marginTop: 28,
    color: "#94a3b8",
    fontSize: 12,
  },

  heroVisual: {
    display: "flex",
    justifyContent: "center",
  },

  dashboardCard: {
    width: "100%",
    maxWidth: 500,
    padding: 22,
    borderRadius: 20,
    background: "rgba(15,23,42,0.8)",
    border: "1px solid rgba(148,163,184,0.16)",
    boxShadow: "0 30px 80px rgba(0,0,0,0.35)",
    backdropFilter: "blur(20px)",
  },

  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 20,
  },

  cardTitle: {
    fontWeight: 750,
    fontSize: 16,
  },

  cardSubtitle: {
    fontSize: 11,
    color: "#64748b",
    marginTop: 5,
  },

  statusDot: {
    color: "#22c55e",
    fontSize: 14,
  },

  metricGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 12,
  },

  metricCard: {
    padding: 16,
    borderRadius: 14,
    background: "rgba(30,41,59,0.72)",
    border: "1px solid rgba(148,163,184,0.1)",
    display: "flex",
    flexDirection: "column",
    gap: 5,
    color: "#e2e8f0",
  },

  metricIcon: {
    width: 34,
    height: 34,
    borderRadius: 9,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "rgba(99,102,241,0.15)",
    color: "#a5b4fc",
    marginBottom: 5,
  },

  aiPanel: {
    marginTop: 14,
    padding: 16,
    borderRadius: 14,
    background: "linear-gradient(135deg, rgba(99,102,241,0.16), rgba(6,182,212,0.08))",
    border: "1px solid rgba(129,140,248,0.18)",
    display: "flex",
    gap: 13,
    color: "#e2e8f0",
  },

  aiIcon: {
    width: 38,
    height: 38,
    borderRadius: 10,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "rgba(99,102,241,0.18)",
    color: "#a5b4fc",
    flexShrink: 0,
  },

  section: {
    padding: "100px 7%",
    background: "#f8fafc",
  },

  sectionHeading: {
    maxWidth: 720,
    margin: "0 auto 55px",
    textAlign: "center",
  },

  sectionBadge: {
    color: "#6366f1",
    fontSize: 12,
    fontWeight: 800,
    letterSpacing: 1.5,
    marginBottom: 12,
  },

  sectionTitle: {
    fontSize: "clamp(30px, 4vw, 45px)",
    margin: 0,
    letterSpacing: "-1.5px",
  },

  sectionDescription: {
    color: "#64748b",
    lineHeight: 1.7,
    marginTop: 16,
  },

  featureGrid: {
    maxWidth: 1150,
    margin: "0 auto",
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: 20,
  },

  featureCard: {
    background: "white",
    border: "1px solid #e2e8f0",
    borderRadius: 17,
    padding: 26,
    boxShadow: "0 10px 30px rgba(15,23,42,0.04)",
  },

  featureIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#eef2ff",
    color: "#4f46e5",
    marginBottom: 18,
  },

  featureTitle: {
    margin: 0,
    fontSize: 17,
  },

  featureDescription: {
    color: "#64748b",
    lineHeight: 1.65,
    fontSize: 14,
    marginBottom: 0,
  },

  workflowSection: {
    padding: "100px 7%",
    background: "#eef2ff",
  },

  workflow: {
    maxWidth: 1150,
    margin: "0 auto",
    display: "grid",
    gridTemplateColumns: "repeat(5, 1fr)",
    gap: 16,
  },

  workflowStep: {
    background: "white",
    borderRadius: 16,
    padding: 23,
    border: "1px solid #e0e7ff",
  },

  workflowNumber: {
    fontSize: 13,
    fontWeight: 800,
    color: "#6366f1",
    marginBottom: 18,
  },

  techGrid: {
    maxWidth: 1000,
    margin: "0 auto",
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: 14,
  },

  techCard: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    background: "white",
    border: "1px solid #e2e8f0",
    borderRadius: 12,
    padding: "16px 18px",
    fontWeight: 600,
    fontSize: 14,
  },

  ctaSection: {
    margin: "0 7%",
    padding: "55px 6%",
    borderRadius: 24,
    background: "linear-gradient(135deg, #111827, #1e1b4b)",
    color: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 30,
  },

  ctaBadge: {
    display: "flex",
    alignItems: "center",
    gap: 7,
    color: "#a5b4fc",
    fontSize: 12,
    fontWeight: 700,
    marginBottom: 12,
  },

  ctaTitle: {
    fontSize: 32,
    margin: 0,
  },

  ctaDescription: {
    color: "#94a3b8",
    maxWidth: 650,
    lineHeight: 1.6,
  },

  ctaButton: {
    display: "inline-flex",
    alignItems: "center",
    gap: 8,
    background: "white",
    color: "#111827",
    padding: "14px 20px",
    borderRadius: 10,
    textDecoration: "none",
    fontWeight: 750,
    whiteSpace: "nowrap",
  },

  footer: {
    marginTop: 50,
    padding: "30px 7%",
    display: "flex",
    justifyContent: "space-between",
    gap: 20,
    flexWrap: "wrap",
    color: "#64748b",
    fontSize: 13,
    background: "#f8fafc",
  },
};
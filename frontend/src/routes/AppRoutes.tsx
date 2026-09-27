import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import LandingPage from "../pages/LandingPage";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import Documents from "../pages/Documents";
import UploadDocument from "../pages/UploadDocument";
import Chat from "../pages/Chat";
import SemanticSearch from "../pages/SemanticSearch";
import Analytics from "../pages/Analytics";
import KnowledgeHealth from "../pages/KnowledgeHealth";
import DocumentIntelligence from "../pages/DocumentIntelligence";
import UserManagement from "../pages/UserManagement";

import ProtectedRoute from "./ProtectedRoute";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* PUBLIC */}

        <Route
          path="/"
          element={<LandingPage />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        {/* PROTECTED */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/documents"
          element={
            <ProtectedRoute>
              <Documents />
            </ProtectedRoute>
          }
        />

        <Route
          path="/upload"
          element={
            <ProtectedRoute>
              <UploadDocument />
            </ProtectedRoute>
          }
        />

        {/* AI CHAT */}

        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />

        {/* SEMANTIC SEARCH */}

        <Route
          path="/semantic-search"
          element={
            <ProtectedRoute>
              <SemanticSearch />
            </ProtectedRoute>
          }
        />

        {/* ANALYTICS */}

        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <Analytics />
            </ProtectedRoute>
          }
        />

        {/* KNOWLEDGE HEALTH */}

        <Route
          path="/knowledge-health"
          element={
            <ProtectedRoute>
              <KnowledgeHealth />
            </ProtectedRoute>
          }
        />

        {/* DOCUMENT INTELLIGENCE */}

        <Route
          path="/documents/intelligence/:id"
          element={
            <ProtectedRoute>
              <DocumentIntelligence />
            </ProtectedRoute>
          }
        />

        {/* USER MANAGEMENT */}

        <Route
          path="/user-management"
          element={
            <ProtectedRoute>
              <UserManagement />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}
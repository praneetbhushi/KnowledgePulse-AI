import api from "./axios";

export interface DocumentOverview {
  total_documents: number;
  processed_documents: number;
  duplicate_documents: number;
  average_quality: number;
}

export interface QualityDistribution {
  quality_level: string;
  count: number;
}

export interface RecentDocument {
  id: number;
  filename: string;
  file_type: string;
  status: string;
  category: string | null;
  quality_score: number | null;
  quality_level: string | null;
  is_duplicate: boolean;
  uploaded_at: string;
}


export async function getDocumentOverview(): Promise<DocumentOverview> {
  const response = await api.get("/document-analytics/overview");
  return response.data;
}


export async function getQualityDistribution(): Promise<
  QualityDistribution[]
> {
  const response = await api.get("/document-analytics/quality-distribution");
  return response.data;
}


export async function getRecentDocuments(): Promise<
  RecentDocument[]
> {
  const response = await api.get("/api/v1/document-analytics/recent");
  return response.data;
}
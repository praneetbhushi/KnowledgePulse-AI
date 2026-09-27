import api from "./axios";

export interface AnalyticsDashboard {
  total_searches: number;
  answered_searches: number;
  unanswered_searches: number;
  answer_rate: number;
  average_search_time: number;
  average_llm_time: number;
  average_rag_time: number;
  average_distance: number;
}

export interface RecentSearch {
  id: number;
  query: string;
  result_count: number;
  best_distance: number | null;
  search_time: number | null;
  llm_time: number | null;
  total_rag_time: number | null;
  was_answered: boolean | null;
  searched_at: string;
}

export interface AnalyticsTrend {
  date: string;
  searches: number;
  answered: number;
  unanswered: number;
  average_search_time: number;
  average_llm_time: number;
  average_rag_time: number;
}

export async function getAnalyticsDashboard(): Promise<AnalyticsDashboard> {
  const response = await api.get("/api/v1/analytics/dashboard");

  return response.data;
}

export async function getRecentSearches(): Promise<RecentSearch[]> {
  const response = await api.get("/api/v1/analytics/recent-searches");
  return response.data;
}

export async function getAnalyticsTrends(): Promise<AnalyticsTrend[]> {
  const response = await api.get("/api/v1/analytics/trends");
  return response.data;
}
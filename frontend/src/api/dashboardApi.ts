import api from "./axios";
import type { DashboardSummary } from "../types/dashboard";

export const getDashboardSummary = async (): Promise<DashboardSummary> => {
  const response = await api.get("/api/v1/dashboard/summary");
  return response.data;
};
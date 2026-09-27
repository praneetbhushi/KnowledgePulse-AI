import { useQuery } from "@tanstack/react-query";
import { getDashboardSummary } from "../api/dashboardApi";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: getDashboardSummary,
  });
}
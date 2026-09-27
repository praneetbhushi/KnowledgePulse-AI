import { useEffect, useState } from "react";

import {
  getAnalyticsDashboard,
  getRecentSearches,
  getAnalyticsTrends,
} from "../api/analytics";

import type {
  AnalyticsDashboard,
  RecentSearch,
  AnalyticsTrend,
} from "../api/analytics";

export default function useAnalytics() {
  const [dashboard, setDashboard] =
    useState<AnalyticsDashboard | null>(null);

  const [recentSearches, setRecentSearches] =
    useState<RecentSearch[]>([]);

  const [trends, setTrends] =
    useState<AnalyticsTrend[]>([]);

  const [loading, setLoading] =
    useState<boolean>(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        setLoading(true);
        setError(null);

        const [
          dashboardData,
          recentSearchesData,
          trendsData,
        ] = await Promise.all([
          getAnalyticsDashboard(),
          getRecentSearches(),
          getAnalyticsTrends(),
        ]);

        setDashboard(dashboardData);
        setRecentSearches(recentSearchesData);
        setTrends(trendsData);
      } catch (err) {
        console.error(
          "Failed to load analytics:",
          err
        );

        setError(
          "Failed to load analytics data."
        );
      } finally {
        setLoading(false);
      }
    };

    loadAnalytics();
  }, []);

  return {
    dashboard,
    recentSearches,
    trends,
    loading,
    error,
  };
}
import { useEffect, useState } from "react";

import {
  getDocumentOverview,
  getQualityDistribution,
  getRecentDocuments,
} from "../api/documentAnalytics";

import type {
  DocumentOverview,
  QualityDistribution,
  RecentDocument,
} from "../api/documentAnalytics";


export default function useDocumentAnalytics() {

  const [overview, setOverview] =
    useState<DocumentOverview | null>(null);

  const [qualityDistribution, setQualityDistribution] =
    useState<QualityDistribution[]>([]);

  const [recentDocuments, setRecentDocuments] =
    useState<RecentDocument[]>([]);

  const [loading, setLoading] =
    useState<boolean>(true);

  const [error, setError] =
    useState<string | null>(null);


  const loadData = async () => {

    try {

      setLoading(true);
      setError(null);

      const [
        overviewData,
        qualityData,
        recentData,
      ] = await Promise.all([
        getDocumentOverview(),
        getQualityDistribution(),
        getRecentDocuments(),
      ]);

      setOverview(overviewData);
      setQualityDistribution(qualityData);
      setRecentDocuments(recentData);

    } catch (err) {

      console.error(
        "Failed to load document analytics:",
        err
      );

      setError(
        "Failed to load document analytics."
      );

    } finally {

      setLoading(false);

    }
  };


  useEffect(() => {
    loadData();
  }, []);


  return {
    overview,
    qualityDistribution,
    recentDocuments,
    loading,
    error,
    refresh: loadData,
  };
}
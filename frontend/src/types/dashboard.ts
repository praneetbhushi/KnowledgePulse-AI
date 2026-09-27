export interface DashboardSummary {
  documents: {
    total_documents: number;
    processed_documents: number;
    failed_documents: number;
    processing_documents: number;
    duplicate_documents: number;
  };

  quality: {
    average_quality_score: number;
    excellent_documents: number;
    good_documents: number;
    fair_documents: number;
    poor_documents: number;
    documents_without_quality_score: number;
  };

  classification: {
    total_classified_documents: number;
    average_classification_confidence: number;
    category_distribution: Record<string, number>;
    duplicate_rate: number;
  };

  search_analytics: {
    total_searches: number;
    unique_queries: number;
    successful_searches: number;
    weak_searches: number;
    success_rate: number;
    average_best_distance: number;

    top_queries: {
      query: string;
      search_count: number;
    }[];
  };

  knowledge_gaps: {
    total_gaps: number;
    high_priority_gaps: number;
    medium_priority_gaps: number;
    low_priority_gaps: number;
    average_gap_distance: number;

    top_gaps: {
      query: string;
      occurrence_count: number;
      average_distance: number;
      priority: string;
      latest_search: string;
    }[];
  };

  department_health: {
    total_departments: number;
    average_department_health: number;

    departments: {
      department_id: number;
      department_name: string;
      total_documents: number;
      documents_with_quality_score: number;
      average_quality_score: number;
      category_distribution: Record<string, number>;
      duplicate_documents: number;
      duplicate_rate: number;
      knowledge_health_score: number;
      knowledge_health_level: string;
    }[];
  };
}
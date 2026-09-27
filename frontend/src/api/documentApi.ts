import api from "./axios";

export interface Document {
  id: number;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  file_path: string;
  file_hash: string;
  status: string;

  category: string | null;
  classification_confidence: number | null;

  is_duplicate: boolean;
  duplicate_of_document_id: number | null;
  duplicate_similarity: number | null;

  quality_score: number | null;
  quality_level: string | null;

  uploaded_at: string;
  uploaded_by: number;
}

export interface DocumentIntelligence {
  document_id: number;
  filename: string;
  file_type: string;
  file_size: number;
  status: string;

  category: string | null;
  classification_confidence: number | null;

  quality: {
    score: number | null;
    level: string | null;
  };

  duplicate: {
    is_duplicate: boolean;
    duplicate_of_document_id: number | null;
    similarity: number | null;
  };

  uploaded_at: string;
  uploaded_by: number;
}

export async function getDocumentIntelligence(
  documentId: number
): Promise<DocumentIntelligence> {

  const response =
    await api.get<DocumentIntelligence>(
      `/api/v1/documents/intelligence/${documentId}`
    );

  return response.data;
}

export async function getDocuments(): Promise<Document[]> {
  const response = await api.get<Document[]>(
    "/api/v1/documents"
  );

  return response.data;
}

export async function uploadDocument(
  file: File,
  onProgress?: (progress: number) => void
) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/api/v1/documents/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },

      onUploadProgress: (progressEvent) => {
        if (!progressEvent.total) {
          return;
        }

        const progress = Math.round(
          (progressEvent.loaded * 100) /
            progressEvent.total
        );

        onProgress?.(progress);
      },
    }
  );

  return response.data;
}
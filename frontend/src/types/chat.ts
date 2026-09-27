export interface ChatSource {
  document_id: number;
  document_name: string;
  chunk_index: number;
}

export interface ChatResponse {
  answer: string;
  conversation_id: number;
  sources: ChatSource[];
}

export interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
}
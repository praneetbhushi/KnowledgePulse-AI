import api from "./axios";
import type { ChatResponse } from "../types/chat";

export const askQuestion = async (
  question: string,
  conversationId?: number
): Promise<ChatResponse> => {

  const response = await api.post("/api/v1/chat/", {
    question,
    conversation_id: conversationId,
  });

  return response.data;
};
import { useState } from "react";

import {
  Box,
  Button,
  Container,
  Divider,
  Paper,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import SmartToyIcon from "@mui/icons-material/SmartToy";

import ChatInput from "../components/chat/ChatInput";
import ChatMessage from "../components/chat/ChatMessage";
import TypingIndicator from "../components/chat/TypingIndicator";
import SourceCard from "../components/chat/SourceCard";

import { useChat } from "../hooks/useChat";

import type {
  ChatMessage as ChatMessageType,
} from "../types/chat";

export default function Chat() {
  const [messages, setMessages] =
    useState<ChatMessageType[]>([]);

  const [conversationId, setConversationId] =
    useState<number>();

  const chatMutation = useChat();

  const sendQuestion = (question: string) => {
    const userMessage: ChatMessageType = {
      id: Date.now(),
      role: "user",
      content: question,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    chatMutation.mutate(
      {
        question,
        conversationId,
      },
      {
        onSuccess(data) {
          setConversationId(
            data.conversation_id
          );

          const aiMessage: ChatMessageType = {
            id: Date.now() + 1,
            role: "assistant",
            content: data.answer,
            sources: data.sources,
          };

          setMessages((prev) => [
            ...prev,
            aiMessage,
          ]);
        },

        onError(error) {
          console.error(error);

          const errorMessage: ChatMessageType = {
            id: Date.now() + 1,
            role: "assistant",
            content:
              "Sorry, I couldn't process your question. Please try again.",
          };

          setMessages((prev) => [
            ...prev,
            errorMessage,
          ]);
        },
      }
    );
  };

  const startNewChat = () => {
    setMessages([]);
    setConversationId(undefined);
    chatMutation.reset();
  };

  return (
    <Container
      maxWidth="md"
      sx={{
        py: 4,
      }}
    >
      {/* HEADER */}

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
          gap: 2,
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1.5,
          }}
        >
          <SmartToyIcon
            sx={{
              fontSize: 38,
            }}
          />

          <Box>
            <Typography
              variant="h4"
              sx={{
                fontWeight: 700,
              }}
            >
              KnowledgePulse AI
            </Typography>

            <Typography
              variant="body2"
              color="text.secondary"
            >
              Enterprise Knowledge Assistant
            </Typography>
          </Box>
        </Box>

        <Button
          variant="outlined"
          startIcon={<AddIcon />}
          onClick={startNewChat}
        >
          New Chat
        </Button>
      </Box>

      {/* CHAT WINDOW */}

      <Paper
        elevation={2}
        sx={{
          minHeight: 520,
          maxHeight: 650,
          overflowY: "auto",
          p: 3,
          borderRadius: 3,
        }}
      >
        {/* EMPTY CHAT */}

        {messages.length === 0 && (
          <Box
            sx={{
              minHeight: 450,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
            }}
          >
            <Box
              sx={{
                maxWidth: 500,
                width: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 2,
              }}
            >
              <SmartToyIcon
                sx={{
                  fontSize: 64,
                }}
              />

              <Typography
                variant="h5"
                sx={{
                  fontWeight: 600,
                }}
              >
                Ask KnowledgePulse AI
              </Typography>

              <Typography
                color="text.secondary"
              >
                Ask questions about your uploaded
                documents and get answers based on
                your enterprise knowledge base.
              </Typography>

              <Divider
                sx={{
                  width: "100%",
                  my: 1,
                }}
              />

              <Typography
                variant="body2"
                color="text.secondary"
              >
                Try asking:
              </Typography>

              <Typography
                variant="body2"
                sx={{
                  fontWeight: 500,
                }}
              >
                "What skills are mentioned in the
                document?"
              </Typography>

              <Typography
                variant="body2"
                sx={{
                  fontWeight: 500,
                }}
              >
                "What is the name of the candidate?"
              </Typography>
            </Box>
          </Box>
        )}

        {/* MESSAGES */}

        {messages.map((message) => (
          <Box key={message.id}>
            <ChatMessage
              role={message.role}
              message={message.content}
            />

            {message.sources &&
              message.sources.length > 0 && (
                <Box
                  sx={{
                    ml: {
                      xs: 0,
                      sm: 7,
                    },
                    mb: 2,
                  }}
                >
                  <Typography
                    variant="caption"
                    color="text.secondary"
                  >
                    Sources
                  </Typography>

                  {message.sources.map(
                    (source) => (
                      <SourceCard
                        key={
                          source.document_id +
                          "-" +
                          source.chunk_index
                        }
                        source={source}
                      />
                    )
                  )}
                </Box>
              )}
          </Box>
        ))}

        {/* LOADING */}

        {chatMutation.isPending && (
          <TypingIndicator />
        )}
      </Paper>

      {/* INPUT */}

      <ChatInput
        onSend={sendQuestion}
        loading={chatMutation.isPending}
      />
    </Container>
  );
}
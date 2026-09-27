import { useState } from "react";

import {
  Box,
  Button,
  TextField,
} from "@mui/material";

interface Props {
  onSend: (question: string) => void;
  loading: boolean;
}

export default function ChatInput({
  onSend,
  loading,
}: Props) {
  const [question, setQuestion] =
    useState("");

  const handleSend = () => {
    if (!question.trim() || loading) {
      return;
    }

    onSend(question.trim());

    setQuestion("");
  };

  return (
    <Box
      sx={{
        display: "flex",
        gap: 1.5,
        mt: 2,
        alignItems: "flex-start",
      }}
    >
      <TextField
        fullWidth
        multiline
        maxRows={4}
        placeholder="Ask a question about your documents..."
        value={question}
        disabled={loading}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
        onKeyDown={(e) => {
          if (
            e.key === "Enter" &&
            !e.shiftKey &&
            !loading
          ) {
            e.preventDefault();
            handleSend();
          }
        }}
      />

      <Button
        variant="contained"
        onClick={handleSend}
        disabled={
          loading || !question.trim()
        }
        sx={{
          minWidth: 90,
          height: 56,
        }}
      >
        {loading ? "..." : "Send"}
      </Button>
    </Box>
  );
}
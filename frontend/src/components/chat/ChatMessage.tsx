import {
  Avatar,
  Box,
  Paper,
  Typography,
} from "@mui/material";

import SmartToyIcon from "@mui/icons-material/SmartToy";

interface Props {
  role: "user" | "assistant";
  message: string;
}

export default function ChatMessage({
  role,
  message,
}: Props) {
  const isUser = role === "user";

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser
          ? "flex-end"
          : "flex-start",
        alignItems: "flex-start",
        mb: 2,
        gap: 1.5,
      }}
    >
      {!isUser && (
        <Avatar
          sx={{
            width: 38,
            height: 38,
          }}
        >
          <SmartToyIcon />
        </Avatar>
      )}

      <Paper
        elevation={1}
        sx={{
          p: 2,
          maxWidth: {
            xs: "85%",
            sm: "75%",
          },
          borderRadius: 2,
          bgcolor: isUser
            ? "primary.main"
            : "grey.100",
          color: isUser
            ? "white"
            : "text.primary",
        }}
      >
        <Typography
          sx={{
            whiteSpace: "pre-wrap",
            lineHeight: 1.6,
          }}
        >
          {message}
        </Typography>
      </Paper>
    </Box>
  );
}
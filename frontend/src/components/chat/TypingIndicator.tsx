import {
  CircularProgress,
  Box,
  Typography,
} from "@mui/material";

export default function TypingIndicator() {

  return (

    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 2,
        mt: 2,
      }}
    >

      <CircularProgress size={20} />

      <Typography>

        AI is thinking...

      </Typography>

    </Box>

  );

}
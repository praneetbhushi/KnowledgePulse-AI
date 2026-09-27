import {
  Box,
  Card,
  CardContent,
  Typography,
} from "@mui/material";

import DescriptionIcon from "@mui/icons-material/Description";

import type {
  ChatSource,
} from "../../types/chat";

interface Props {
  source: ChatSource;
}

export default function SourceCard({
  source,
}: Props) {
  return (
    <Card
      variant="outlined"
      sx={{
        mt: 1,
        borderRadius: 2,
      }}
    >
      <CardContent
        sx={{
          py: 1.5,
          "&:last-child": {
            pb: 1.5,
          },
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
          }}
        >
          <DescriptionIcon fontSize="small" />

          <Typography
            variant="subtitle2"
            sx={{
              wordBreak: "break-word",
            }}
          >
            {source.document_name}
          </Typography>
        </Box>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            mt: 0.5,
          }}
        >
          Chunk {source.chunk_index}
        </Typography>
      </CardContent>
    </Card>
  );
}
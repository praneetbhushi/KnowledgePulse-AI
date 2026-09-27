import { LinearProgress, Typography, Box } from "@mui/material";

interface UploadProgressProps {
  progress: number;
}

export default function UploadProgress({
  progress,
}: UploadProgressProps) {
  return (
    <Box sx={{ mt: 3 }}>
      <LinearProgress
        variant="determinate"
        value={progress}
      />

      <Typography sx={{ mt: 1 }}>
        {progress}%
      </Typography>
    </Box>
  );
}
import {
  Card,
  CardContent,
  Typography,
} from "@mui/material";

interface Props {
  children: React.ReactNode;
}

export default function UploadCard({
  children,
}: Props) {
  return (
    <Card
      sx={{
        maxWidth: 700,
        mx: "auto",
        mt: 5,
      }}
    >
      <CardContent>
        <Typography
          variant="h4"
          gutterBottom
        >
          Upload Documents
        </Typography>

        <Typography
          color="text.secondary"
          sx={{ mb: 2 }}
        >
          Upload PDF, DOCX and TXT files to
          your enterprise knowledge base.
        </Typography>

        {children}
      </CardContent>
    </Card>
  );
}
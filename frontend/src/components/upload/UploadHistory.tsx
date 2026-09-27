import {
  Chip,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import DescriptionIcon from "@mui/icons-material/Description";

import type { Document } from "../../api/documentApi";

interface Props {
  documents: Document[];
}

function getStatusColor(status: string) {
  switch (status.toLowerCase()) {
    case "processed":
      return "success";

    case "processing":
      return "warning";

    case "failed":
      return "error";

    default:
      return "default";
  }
}

function formatFileSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;

  if (bytes < 1024 * 1024)
    return `${(bytes / 1024).toFixed(1)} KB`;

  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export default function UploadHistory({
  documents,
}: Props) {
  return (
    <>
      <Typography
        variant="h5"
        sx={{
          mt: 5,
          mb: 2,
        }}
      >
        Recent Uploads
      </Typography>

      <TableContainer component={Paper}>

        <Table>

          <TableHead>

            <TableRow>

              <TableCell>Document</TableCell>

              <TableCell>Status</TableCell>

              <TableCell>Category</TableCell>

              <TableCell>Size</TableCell>

            </TableRow>

          </TableHead>

          <TableBody>

            {documents.map((doc) => (

              <TableRow key={doc.id}>

                <TableCell>

                  <DescriptionIcon
                    sx={{
                      mr: 1,
                      verticalAlign: "middle",
                    }}
                  />

                  {doc.original_filename}

                </TableCell>

                <TableCell>

                  <Chip
                    label={doc.status}
                    color={getStatusColor(doc.status)}
                    size="small"
                  />

                </TableCell>

                <TableCell>

                  {doc.category ?? "-"}

                </TableCell>

                <TableCell>

                  {formatFileSize(doc.file_size)}

                </TableCell>

              </TableRow>

            ))}

          </TableBody>

        </Table>

      </TableContainer>
    </>
  );
}
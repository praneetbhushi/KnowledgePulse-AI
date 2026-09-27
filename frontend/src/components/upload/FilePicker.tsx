import { Box, Button, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { useDropzone } from "react-dropzone";
import toast from "react-hot-toast";
interface Props {
  file: File | null;
  onFileChange: (file: File | null) => void;
}

export default function FilePicker({
  file,
  onFileChange,
}: Props) {

  const { getRootProps, getInputProps } =
    useDropzone({

      accept: {
        "application/pdf": [".pdf"],
        "text/plain": [".txt"],
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
          [".docx"],
      },

      multiple: false,

      onDrop: (acceptedFiles) => {
  if (acceptedFiles.length === 0) {
    toast.error("Unsupported file type.");
    return;
  }

  const file = acceptedFiles[0];

  if (file.size > 10 * 1024 * 1024) {
    toast.error("Maximum file size is 10 MB.");
    return;
  }

  onFileChange(file);
},

    });

  return (

    <Box

      {...getRootProps()}

      sx={{
        border: "2px dashed #2196f3",
        borderRadius: 2,
        p: 5,
        textAlign: "center",
        cursor: "pointer",
      }}
    >

      <input {...getInputProps()} />

      <CloudUploadIcon
        sx={{
          fontSize: 60,
          color: "#1976d2",
        }}
      />

      <Typography variant="h6" sx={{ mt: 2 }}>
        {file
          ? file.name
          : "Drag & Drop your file here"}
      </Typography>

      <Typography color="text.secondary">
        or click to browse
      </Typography>

      <Button
        variant="contained"
        sx={{ mt: 3 }}
      >
        Choose File
      </Button>

    </Box>

  );

}
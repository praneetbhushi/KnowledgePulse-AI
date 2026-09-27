import { useState } from "react";
import { Button, Typography } from "@mui/material";
import toast from "react-hot-toast";

import UploadCard from "../components/upload/UploadCard";
import FilePicker from "../components/upload/FilePicker";
import UploadProgress from "../components/upload/UploadProgress";
import UploadHistory from "../components/upload/UploadHistory";

import { uploadDocument } from "../api/documentApi";
import { useDocuments } from "../hooks/useDocuments";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);

  const {
    data: documents = [],
    refetch,
  } = useDocuments();

  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
  if (!file) return;

  setUploading(true);

  try {
    await uploadDocument(file, (progress) => {
      setProgress(progress);
    });

    toast.success("Upload successful!");

    await refetch();

    setFile(null);

    setTimeout(() => {
      setProgress(0);
    }, 1000);

  } catch {
    toast.error("Upload failed");
    setProgress(0);
  } finally {
    setUploading(false);
  }
};

  return (
    <>
      <UploadCard>

        <FilePicker
          file={file}
          onFileChange={setFile}
        />

        {file && (
          <Typography sx={{ mt: 3 }}>
            Selected File: <b>{file.name}</b>
          </Typography>
        )}

        <Button
          variant="contained"
          fullWidth
          sx={{ mt: 3 }}
          disabled={!file || uploading}
          onClick={handleUpload}
        >
          {uploading ? "Uploading..." : "Upload"}
        </Button>

        {progress > 0 && progress < 100 && (
          <UploadProgress progress={progress} />
        )}

      </UploadCard>

      <UploadHistory documents={documents} />
    </>
  );
}
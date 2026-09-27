class TextChunkingService:
    
    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 100,
    ):

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += chunk_size - overlap
    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 100,
    ):

        chunks = []

        start = 0

        chunk_id = 1

        while start < len(text):

            end = start + chunk_size

            chunks.append({
                "chunk_id": chunk_id,
                "text": text[start:end],
                "start": start,
                "end": min(end, len(text)),
            })

            chunk_id += 1
            start += chunk_size - overlap

        return chunks   

text_chunking_service = TextChunkingService()
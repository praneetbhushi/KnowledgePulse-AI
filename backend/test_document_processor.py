from app.services.document_processor import document_processor


file_path = "uploads/test.pdf"

text = document_processor.extract_text(
    file_path=file_path,
    file_type="pdf"
)

print("=" * 50)
print("EXTRACTED TEXT")
print("=" * 50)

print(text)

print("=" * 50)
print(f"Total characters: {len(text)}")
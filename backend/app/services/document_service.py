import os
import uuid
import hashlib
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.document import Document

from app.repositories.document_repository import (
    document_repository,
)

from app.core.upload_config import (
    ALLOWED_EXTENSIONS,
)

from app.core.exceptions.custom_exceptions import (
    InvalidFileTypeException,
)

from app.services.document_processor import (
    document_processor,
)

from app.services.document_processing_service import (
    document_processing_service,
)

from app.services.text_processor import (
    text_processor,
)

from app.services.embedding_service import (
    embedding_service,
)

from app.services.vector_store_service import (
    vector_store_service,
)

from app.services.document_classification_service import (
    document_classification_service,
)

from app.services.duplicate_detection_service import (
    duplicate_detection_service,
)

from app.services.knowledge_quality_service import (
    knowledge_quality_service,
)

UPLOAD_DIR = "uploads"


class DocumentService:

    def calculate_file_hash(
        self,
        file_path: str,
    ):

        sha = hashlib.sha256()

        with open(file_path, "rb") as f:

            while True:

                data = f.read(8192)

                if not data:
                    break

                sha.update(data)

        return sha.hexdigest()
    def upload_document(

        self,

        db: Session,

        file: UploadFile,

        user_id: int,

    ):

        # -----------------------------------
        # Validate filename
        # -----------------------------------

        if not file.filename:

            raise InvalidFileTypeException(
                "Invalid filename."
            )

        extension = (
            file.filename
            .split(".")[-1]
            .lower()
        )

        if extension not in ALLOWED_EXTENSIONS:

            raise InvalidFileTypeException(
                f"{extension} files are not allowed."
            )

        # -----------------------------------
        # Upload directory
        # -----------------------------------

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True,
        )

        unique_filename = (
            f"{uuid.uuid4()}.{extension}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename,
        )

        # -----------------------------------
        # File size and content validation
        # -----------------------------------

        file_content = file.file.read()

        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

        if not file_content:
            raise InvalidFileTypeException(
                "Uploaded file is empty."
            )

        if len(file_content) > MAX_FILE_SIZE:
            raise InvalidFileTypeException(
                "File size must not exceed 10 MB."
            )

        file_hash = hashlib.sha256(file_content).hexdigest()


        with open(
            file_path,
            "wb",
        ) as buffer:

            buffer.write(
                file_content
            )

        # -----------------------------------
        # SHA256 Hash
        # -----------------------------------

        file_hash = self.calculate_file_hash(
            file_path
        )

        existing_document = (
            document_repository.get_by_hash(
                db,
                file_hash,
            )
        )

        if existing_document:

            print(
                "Duplicate file skipped."
            )

            return existing_document

        # -----------------------------------
        # Create PostgreSQL Document
        # -----------------------------------

        document = Document(

            filename=unique_filename,

            original_filename=file.filename,

            file_hash=file_hash,

            file_type=extension,

            file_size=len(file_content),

            file_path=file_path,

            uploaded_by=user_id,

            status="processing",

        )

        document = (
            document_repository.create(
                db,
                document,
            )
        )

        try:
            # ---------------------------------
            # STEP 1 : Extract Text
            # ---------------------------------

            extracted_text = document_processor.extract_text(
                file_path=file_path,
                file_type=extension,
            )

            if not extracted_text.strip():
                raise Exception("No text extracted from document.")

            # ---------------------------------
            # STEP 2 : Clean Text
            # ---------------------------------

            cleaned_text = text_processor.clean_text(
                extracted_text
            )

            # ---------------------------------
            # STEP 3 : Duplicate Detection
            # ---------------------------------

            duplicate_result = (
                duplicate_detection_service.detect_duplicate(
                    cleaned_text
                )
            )

            document.is_duplicate = duplicate_result["is_duplicate"]

            duplicate_document_id = (
                duplicate_result["duplicate_of_document_id"]
            )

            if duplicate_document_id is not None:
                duplicate_document = (
                    db.query(Document)
                    .filter(Document.id == duplicate_document_id)
                    .first()
                )

                if duplicate_document is None:
                    print(
                        f"WARNING: Duplicate document "
                        f"{duplicate_document_id} no longer exists."
                    )

                    document.is_duplicate = False
                    document.duplicate_of_document_id = None
                    document.duplicate_similarity = None

                else:
                    document.duplicate_of_document_id = (
                        duplicate_document_id
                    )

                    document.duplicate_similarity = (
                        duplicate_result["similarity"]
                    )

            else:
                document.duplicate_of_document_id = None
                document.duplicate_similarity = None

            # ---------------------------------
            # STEP 4 : Document Classification
            # ---------------------------------

            classification = (
                document_classification_service.classify(
                    cleaned_text
                )
            )

            document.category = classification["category"]

            document.classification_confidence = (
                classification["confidence"]
            )

            # ---------------------------------
            # STEP 5 : Knowledge Quality
            # ---------------------------------

            quality = (
                knowledge_quality_service.calculate_quality_score(
                    text=cleaned_text,
                    classification_confidence=document.classification_confidence,
                    is_duplicate=document.is_duplicate,
                )
            )

            document.quality_score = (
                quality["quality_score"]
            )

            document.quality_level = (
                quality["quality_level"]
            )

            db.commit()

            db.refresh(document)

            # ---------------------------------
            # STEP 6 : Detect Sections
            # ---------------------------------

            sections = (
                document_processing_service.process_document(
                    file_path
                )
            )

            print("\n========== SECTIONS ==========\n")

            for section in sections:

                print(
                    section["section"]
                )

            # ---------------------------------
            # STEP 7 : Semantic Chunking
            # ---------------------------------

            chunks = text_processor.chunk_sections(
                sections
            )

            print("\n========== CHUNKS ==========\n")

            for index, chunk in enumerate(
                chunks,
                start=1,
            ):

                print(
                    f"Chunk {index}"
                )

                print(
                    f"Page : {chunk['page']}"
                )

                print(
                    f"Section : {chunk['section']}"
                )

                print(
                    chunk["text"][:200]
                )

                print("-" * 60)

            # ---------------------------------
            # STEP 8 : Generate Embeddings
            # ---------------------------------

            chunk_texts = [

                chunk["text"]

                for chunk in chunks

            ]

            embeddings = (
                embedding_service.generate_embeddings(
                    chunk_texts
                )
            )

            print(
                f"Generated {len(embeddings)} embeddings."
            )

            # ---------------------------------
            # STEP 9 : Store in ChromaDB
            # ---------------------------------

            vector_store_service.add_document_chunks(

                document_id=document.id,

                chunks=chunks,

                embeddings=embeddings,

            )

            # ---------------------------------
            # STEP 10 : Store Whole Document Embedding
            # ---------------------------------

            duplicate_detection_service.store_document_embedding(
                document_id=document.id,
                embedding=duplicate_result["embedding"],
            )

            # ---------------------------------
            # STEP 11 : Mark Processing Complete
            # ---------------------------------

            document.status = "processed"

            db.commit()

            db.refresh(document)

            print("\n========== DOCUMENT PROCESSED ==========")

            print(f"ID          : {document.id}")
            print(f"Filename    : {document.original_filename}")
            print(f"Category    : {document.category}")
            print(f"Quality     : {document.quality_score}")
            print(f"Chunks      : {len(chunks)}")
            print("========================================\n")
            print("Vectors stored successfully.")

        except Exception as e:
            db.rollback()

            document.status = "failed"
            db.commit()
            db.refresh(document)

            print(f"DOCUMENT PROCESSING ERROR: {type(e).__name__}: {e}")

            raise HTTPException(
                status_code=500,
                detail="Document processing failed."
            )

            # Re-raise exception so we can
            # see the actual error during
            # development.

            raise


        # ---------------------------------
        # STEP 20: Return document
        # ---------------------------------
        return document

    def calculate_file_hash(
        self,
        file_path: str,
    ):

        sha = hashlib.sha256()

        with open(file_path, "rb") as f:

            while True:
                chunk = f.read(8192)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()
    def get_documents(
        self,
        db: Session,
    ):
        return document_repository.get_all(db)
# ---------------------------------
# Create DocumentService instance
# ---------------------------------
document_service = DocumentService()
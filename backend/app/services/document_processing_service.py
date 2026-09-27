from pathlib import Path
import re

from pypdf import PdfReader
from docx import Document
from pptx import Presentation
from app.services.text_processor import (
    text_processor
)

class DocumentProcessingService:

    SECTION_HEADINGS = [
        "CAREER OBJECTIVE",
        "SUMMARY",
        "ABOUT",
        "EDUCATION",
        "TECHNICAL SKILLS",
        "SKILLS",
        "PROJECTS",
        "EXPERIENCE",
        "CERTIFICATIONS",
        "CERTIFICATES",
        "ACHIEVEMENTS",
        "PUBLICATIONS",
        "HACKATHONS",
        "PERSONAL DETAILS",
        "REFERENCES",
    ]

    def process_document(
        self,
        file_path: str,
    ):

        suffix = Path(file_path).suffix.lower()

        if suffix == ".pdf":
            pages = self.extract_pdf(file_path)

        elif suffix == ".docx":
            text = self.extract_docx(file_path)
            pages = [
                {
                    "page": 1,
                    "text": text
                }
            ]

        elif suffix == ".pptx":
            text = self.extract_pptx(file_path)
            pages = [
                {
                    "page": 1,
                    "text": text
                }
            ]

        elif suffix == ".txt":
            text = self.extract_txt(file_path)
            pages = [
                {
                    "page": 1,
                    "text": text
                }
            ]

        else:
            raise ValueError(
                "Unsupported file type"
            )

        sections = self.detect_sections(pages)

        chunks = text_processor.chunk_sections(
            sections
        )

        return chunks

    def extract_pdf(
        self,
        file_path: str,
    ):

        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            text = (
                page.extract_text()
                or ""
            )

            text = self.clean_text(
                text
            )

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

        return pages

    def extract_docx(
        self,
        file_path: str,
    ):

        document = Document(
            file_path
        )

        text = "\n".join(

            paragraph.text

            for paragraph in document.paragraphs

            if paragraph.text.strip()

        )

        return self.clean_text(text)

    def extract_pptx(
        self,
        file_path: str,
    ):

        presentation = Presentation(
            file_path
        )

        text = []

        for slide in presentation.slides:

            for shape in slide.shapes:

                if hasattr(
                    shape,
                    "text"
                ):

                    if shape.text.strip():

                        text.append(
                            shape.text
                        )

        return self.clean_text(
            "\n".join(text)
        )

    def extract_txt(
        self,
        file_path: str,
    ):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return self.clean_text(
                file.read()
            )

    def clean_text(
        self,
        text: str,
    ):

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove zero-width and non-breaking spaces
        text = (
            text.replace("\u200b", "")
                .replace("\ufeff", "")
                .replace("\xa0", " ")
        )

        # Remove trailing spaces from each line
        lines = [line.strip() for line in text.split("\n")]

        # Rebuild the text
        text = "\n".join(lines)

        # Collapse multiple spaces/tabs
        text = re.sub(r"[ \t]+", " ", text)

        # Keep paragraph structure (max two newlines)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def detect_sections(
        self,
        pages,
    ):
        sections = []

        current_section = "General"
        buffer = ""
        current_page = 1

        heading_pattern = re.compile(
            r"^[A-Z][A-Z &\-]{2,}$"
        )

        for page in pages:

            current_page = page["page"]

            for line in page["text"].splitlines():

                line = line.strip()

                if not line:
                    continue

                upper = line.upper()

                # -----------------------------------------
                # Detect section heading
                # -----------------------------------------

                if (
                    upper in self.SECTION_HEADINGS
                    or heading_pattern.match(upper)
                ):

                    # Save previous section
                    if buffer:

                        sections.append(
                            {
                                "page": current_page,
                                "section": current_section,
                                "text": buffer.strip(),
                            }
                        )

                        buffer = ""

                    # IMPORTANT:
                    # This MUST be inside the line loop
                    current_section = line.title()

                    continue

                # -----------------------------------------
                # Normal content
                # -----------------------------------------

                buffer += line + "\n"

        # ---------------------------------------------
        # Save final section
        # ---------------------------------------------

        if buffer:

            sections.append(
                {
                    "page": current_page,
                    "section": current_section,
                    "text": buffer.strip(),
                }
            )

        # ---------------------------------------------
        # Debug output
        # ---------------------------------------------

        print(
            "\n========== DETECTED SECTIONS ==========\n"
        )

        for section in sections:

            print(
                f"Page {section['page']}"
            )

            print(
                f"Section : {section['section']}"
            )

            print(
                section["text"][:200]
            )

            print(
                "-" * 50
            )

        return sections


document_processing_service = (
    DocumentProcessingService()
)
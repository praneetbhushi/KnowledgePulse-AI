import re

class TextProcessor:

    def clean_text(self, text: str):

        text = text.replace("\r", "\n")

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        return text.strip()

    def chunk_sections(
        self,
        sections,
        max_words: int = 180,
    ):

        chunks = []

        for section in sections:

            page = section["page"]
            title = section["section"]

            words = section["text"].split()

            if len(words) <= max_words:

                chunks.append(
                    {
                        "page": page,
                        "section": title,
                        "text": section["text"],
                        "word_count": len(words),
                    }
                )

                continue

            start = 0

            while start < len(words):

                end = start + max_words

                chunk_words = words[start:end]

                chunks.append(
                    {
                        "page": page,
                        "section": title,
                        "text": " ".join(chunk_words),
                        "word_count": len(chunk_words),
                    }
                )

                start = end - 30

        print("\n========== SEMANTIC CHUNKS ==========\n")

        for index, chunk in enumerate(chunks, start=1):

            print(f"Chunk {index}")

            print(f"Page : {chunk['page']}")

            print(f"Section : {chunk['section']}")

            print(f"Words : {chunk['word_count']}")

            print(chunk["text"][:150])

            print("-" * 60)

        return chunks


text_processor = TextProcessor()
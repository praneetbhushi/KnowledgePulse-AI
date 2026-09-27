from app.ai.llm_service import llm_service

context = """
KnowledgePulse AI is an Enterprise Knowledge Health
and Intelligence Platform.

It supports document upload,
semantic search,
RAG,
and AI-powered chat.
"""

question = "What does KnowledgePulse AI support?"

answer = llm_service.generate_answer(
    question=question,
    context=context,
)

print("\nAI Response:\n")
print(answer)
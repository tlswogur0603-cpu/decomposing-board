from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.constants import POST_CHUNK_OVERLAP, POST_CHUNK_SIZE

POST_CHUNK_SEPARATORS = [
    "\n\n",
    "\n",
    ". ",
    "? ",
    "! ",
    "。 ",
    " ",
    "",
]


def split_post_content(content: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=POST_CHUNK_SIZE,
        chunk_overlap=POST_CHUNK_OVERLAP,
        length_function=len,
        separators=POST_CHUNK_SEPARATORS,
    )

    chunks = [
        chunk.strip()
        for chunk in splitter.split_text(content)
        if chunk.strip()
    ]

    return chunks or [content.strip()]

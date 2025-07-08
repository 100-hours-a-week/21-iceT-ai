import os, logging, pickle
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document

logger = logging.getLogger(__name__)
load_dotenv()

# 1. md 문서 로드
loader = DirectoryLoader(
    path="docs/algorithm",
    glob="**/*.md",
    loader_cls=TextLoader,
    use_multithreading=True,
)
raw_docs = loader.load()

# 2. 각 문서를 알고리즘 제목(#)만 추출해 indexing
docs_for_index = []
for doc in raw_docs:
    lines = doc.page_content.splitlines()
    # 첫 줄이 '#' 제목
    first_line = lines[0].strip() if lines else ""
    if first_line.startswith("#"):
        title = first_line.lstrip("#").strip()
        # Document page_content = 알고리즘 제목, metadata = 파일 경로 + full content
        docs_for_index.append(
            Document(
                page_content=title,
                metadata={
                    "source": doc.metadata["source"],
                    "full_content": doc.page_content
                },
            )
        )

# 3. BM25 인덱싱
bm25 = BM25Retriever.from_documents(docs_for_index)

# 4. pickle 저장
INDEX_SAVE_PATH = os.getenv("VECTOR_STORE_PATH")
os.makedirs(INDEX_SAVE_PATH, exist_ok=True)
index_file = os.path.join(INDEX_SAVE_PATH, "bm25_index.pkl")
with open(index_file, "wb") as f:
    pickle.dump(bm25, f)

logger.info("BM25 알고리즘 제목 인덱스 저장 완료: %s", index_file)
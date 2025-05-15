from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from src.core.embedding_model import get_embedder
import os, logging, dotenv

# 로깅
logger = logging.getLogger(__name__)

# 환경변수 설정
dotenv.load_dotenv()

# 1. Markdown 문서 로드 (docs/ 폴더 내 .md 파일 대상)
loader = DirectoryLoader(
    path="docs",
    glob="**/*.md",
    loader_cls=TextLoader,
    use_multithreading=True,
)
docs = loader.load()

# 2. 문서 분할
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "section"),     # 모듈 전체
        ("##", "subsection"), # 함수 그룹
        ("###", "function")   # 개별 함수
    ]
)
chunks = splitter.split_documents(docs)


# 3. 벡터스토어 생성
embedder = get_embedder()
vectorstore = FAISS.from_documents(chunks, embedding=embedder)

# 4. 로컬 저장
INDEX_SAVE_PATH = os.getenv("VECTOR_STORE_PATH")
os.makedirs(INDEX_SAVE_PATH, exist_ok=True)
vectorstore.save_local(INDEX_SAVE_PATH)

logger.info(f" 벡터스토어 저장 완료: {INDEX_SAVE_PATH}")

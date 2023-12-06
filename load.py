import openai
from langchain.schema.document import Document

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders import UnstructuredODTLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import UnstructuredXMLLoader

openai.api_key = "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"
class audio_loader:
    def __init__(self, filepath):
        self.audio_file = open(filepath, "rb")

    def load(self):
        transcript = openai.Audio.transcribe("whisper-1", self.audio_file)
        return [Document(page_content=transcript["text"])]

loader_dict = {
    ".pdf": UnstructuredPDFLoader,
    ".txt": TextLoader,
    ".docx": Docx2txtLoader,
    ".dox": Docx2txtLoader,
    ".html": BSHTMLLoader,
    ".csv": CSVLoader,
    ".md": UnstructuredMarkdownLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".xls": UnstructuredExcelLoader,
    ".odt": UnstructuredODTLoader,
    ".pptx": UnstructuredPowerPointLoader,
    ".xml": UnstructuredXMLLoader,
    ".wav": audio_loader,
    ".mp3": audio_loader
}

def load(user_id, filepath, ext):
    loader = loader_dict.get(ext, TextLoader)(filepath)
    docs = loader.load()
    processed_docs = [
        Document(
            page_content=doc.page_content,
            metadata={"source": filepath, "user_id": user_id}    
        ) 
    for doc in docs]
    return processed_docs

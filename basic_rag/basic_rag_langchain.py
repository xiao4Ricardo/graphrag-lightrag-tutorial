import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

def build_index(input_path: str, index_path: str):
    """
    加载文本文档，分块并使用 Ollama Embedding 构建 FAISS 向量索引。
    """
    text_loader_kwargs = {'encoding': 'utf-8'}
    loader = DirectoryLoader(input_path, glob="./*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    documents = loader.load()

    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # 向量化与存储
    embeddings = OllamaEmbeddings(
        model="qwen3-embedding:0.6b",
        base_url="http://localhost:11434"
    )
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(index_path)
    print(f"FAISS 向量索引已成功保存至: {index_path}")

if __name__ == "__main__":
    input_dir = "./inputs"
    output_index = "index_faiss"
    if os.path.exists(input_dir):
        build_index(input_dir, output_index)
    else:
        print(f"请先创建输入目录并添加 .txt 文本文件: {input_dir}")

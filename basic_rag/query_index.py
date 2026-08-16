import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY_HERE")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

def get_embeddings():
    return OllamaEmbeddings(
        model="qwen3-embedding:0.6b",
        base_url="http://localhost:11434"
    )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def query_index(index_path: str):
    if not os.path.exists(index_path):
        print(f"错误: 找不到索引路径 {index_path}")
        return

    db = FAISS.load_local(index_path, get_embeddings(), allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model="qwen-plus",
        openai_api_key=DASHSCOPE_API_KEY,
        openai_api_base=DASHSCOPE_BASE_URL,
    )

    prompt = ChatPromptTemplate.from_template(
        "根据以下参考资料回答问题，如果资料中没有相关信息请如实说明。\n\n"
        "参考资料:\n{context}\n\n"
        "问题: {question}"
    )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print(f"已成功加载索引: {index_path}，输入 'quit' 或 'q' 退出问答交互。\n")
    while True:
        user_input = input("问题: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue

        docs = retriever.invoke(user_input)
        answer = chain.invoke(user_input)

        print(f"\n回答:\n{answer}")
        print("\n--- 检索到的参考来源文档片段 ---")
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "未知来源")
            print(f"[{i}] {source}")
            print(doc.page_content[:200] + "...\n")

if __name__ == "__main__":
    query_index("index_faiss")

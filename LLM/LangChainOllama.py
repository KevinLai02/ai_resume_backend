from langchain_community.document_loaders import TextLoader

# -------------載入文件----------------
loader = TextLoader(file_path='./txt/crew.txt',encoding="UTF-8")
docs = loader.load()
# print(docs[0])


from langchain.indexes import VectorstoreIndexCreator
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import(CharacterTextSplitter, RecursiveCharacterTextSplitter)
from langchain_community.vectorstores import Chroma

def Initialize_LLM():
    # -------------分割文件-----------------
    embeddings_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    chatmodel = ChatOllama(
        model = "llama3.1",
        temperature = 0.8,
        num_predict = 1024
    )
    # index = VectorstoreIndexCreator(embedding=embeddings_model).from_loaders([loader])
    text_splitter = RecursiveCharacterTextSplitter(
        separators=' \n',
        chunk_size=10,
        chunk_overlap=2
    )
    chunks = text_splitter.split_documents(docs)
    # print(chunks)
    # -----------------------文字轉向量---------------------------
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory='./chroma_db/db',
        collection_metadata={"hnsw:space":"cosine"}
    )
    db = Chroma(
        persist_directory='./chroma_db/db',
        embedding_function=embeddings_model
    )
    retriever = db.as_retriever(search_type="similarity",
                            search_kwargs={"k": 6})
    return chatmodel,retriever

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate

def chatLLM(UserQuestiion,chatmodel,retriever):
    prompt = ChatPromptTemplate.from_messages([
        ('system','你是一位善用工具的面試官, '
                '請自己判斷上下文來回答問題, 不要盲目地使用工具'),
        MessagesPlaceholder(variable_name="chat_history"),
        ('human','{input}'),
    ])

    str_parser = StrOutputParser()
    template = (
        "請根據以下內容加上自身判斷回答問題:\n"
        "{context}\n"
        "問題: {question}"
        )
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | chatmodel
        | str_parser
    )
    llmAnwser = chain.invoke(UserQuestiion)
    return llmAnwser

LLM = Initialize_LLM()
chatmodel = LLM[0]
retriever= LLM[1]
# retrieved_docs = retriever.invoke("船員資格")
# print(f'傳回 {len(retrieved_docs)} 筆資料')

# UserQuestiion = "我是一名具有三年工作經歷的前端工程師，擅長使用 HTML、CSS 和 JavaScript 開發高效且美觀的網頁應用程式。我熟悉 React 和 Vue 框架，並且在跨瀏覽器相容性和響應式設計方面有豐富的經驗。我熱衷於學習新技術，並且樂於與團隊合作解決複雜的技術問題，致力於提供最佳的用戶體驗。請根據上文問一個問題"
# print(chatLLM(UserQuestiion,chatmodel,retriever))


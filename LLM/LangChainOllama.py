from langchain_community.document_loaders import TextLoader, PyPDFLoader

# -------------載入文件----------------
loader = TextLoader(file_path='./txt/crew.txt',encoding="UTF-8")
docs = loader.load()
# print(docs[0])



# print(pages[0].page_content)

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
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate


def chatLLM(UserQuestiion,chatmodel,retriever):
    prompt = ChatPromptTemplate.from_messages([
        ('system','你是一位善用工具的面試官, '
                '請自己判斷上下文來回答問題, 不要盲目地使用工具'),
        # MessagesPlaceholder(variable_name="chat_history"),
        ('human','{input}'),
    ])

    str_parser = StrOutputParser()
    template = (
        "你是面試官只會根據資料問問題, 且只會問面試相關問題, \n"
        "你不會說多餘的話, 你的回答開頭只會以'請問'來問: \n"
        "我會讓你用中文或英文回答，你就只能用中文或英文回答"
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

def rateLLM(UserQuestiion,chatmodel):
    prompt = ChatPromptTemplate.from_messages([
        ('system','你是一位善用工具的語言模型, '
                '請自己判斷上下文來回答問題, 不要盲目地使用工具'),
        # MessagesPlaceholder(variable_name="chat_history"),
        ('human','{input}'),
    ])

    str_parser = StrOutputParser()
    template = (
        "你是評分面試官只會根據資料評總分, 只會以專業性、建設性、表達方式評分, 三個分數各為100分, \n"
        "你的回答只會有 '專業性、建設性、表達方式'加上分數 以及給予這次面試建議與改進方向 "
        # "{context}\n"
        "問題: {question}"
        )
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | chatmodel
        | str_parser
    )
    llmAnwser = chain.invoke(UserQuestiion)
    return llmAnwser

def resumeLLM(UserQuestiion,chatmodel):
    prompt = ChatPromptTemplate.from_messages([
        ('system','你是一位善用工具的面試官, '
                '請自己判斷上下文來回答問題, 不要盲目地使用工具'),
        # MessagesPlaceholder(variable_name="chat_history"),
        ('human','{input}'),
    ])

    str_parser = StrOutputParser()
    template = (
        "你會幫我找出此人的學歷,工作經歷,專業技能,技術領域,自傳, \n"
        "你不會說多餘的話, 你的回答只會有 '學歷,工作經歷,專業技能,技術領域,自傳'其中一個我問的問題, 加上找到的資料 "
        # "{context}\n"
        "問題: {question}"
        )
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | chatmodel
        | str_parser
    )
    llmAnwser = chain.invoke(UserQuestiion)
    return llmAnwser


# retrieved_docs = retriever.invoke("船員資格")
# print(f'傳回 {len(retrieved_docs)} 筆資料')

# UserQuestiion = "我是一名具有三年工作經歷的前端工程師，擅長使用 HTML、CSS 和 JavaScript 開發高效且美觀的網頁應用程式。我熟悉 React 和 Vue 框架，並且在跨瀏覽器相容性和響應式設計方面有豐富的經驗。我熱衷於學習新技術，並且樂於與團隊合作解決複雜的技術問題，致力於提供最佳的用戶體驗。請根據上文問一個問題"
# print(chatLLM(UserQuestiion,chatmodel,retriever))

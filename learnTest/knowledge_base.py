import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import RedisChatMessageHistory
from langchain.chains.llm import LLMChain
from typing import List, Tuple, Union
from langchain.schema import BaseMessage
from langchain.callbacks import get_openai_callback
from app.FileLoader.loader_factory import FileLoaderFactory
from app.model.beikeai import BeikeEmbeddings
from app.server_config import Config

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "7ec85e66e4075d59e75d37581862c6d6534b680bd68ef1c71183fc73e9be1694"

# This needs to be consolidated.
CHAT_TURN_TYPE = Union[Tuple[str, str], BaseMessage]

_ROLE_MAP = {"human": "Human: ", "ai": "Assistant: "}


def _get_chat_history(chat_history: List[CHAT_TURN_TYPE]) -> str:
    buffer = ""
    for dialogue_turn in chat_history:
        if isinstance(dialogue_turn, BaseMessage):
            role_prefix = _ROLE_MAP.get(dialogue_turn.type, f"{dialogue_turn.type}: ")
            buffer += f"\n{role_prefix}{dialogue_turn.content}"
        elif isinstance(dialogue_turn, tuple):
            human = "Human: " + dialogue_turn[0]
            ai = "Assistant: " + dialogue_turn[1]
            buffer += "\n" + "\n".join([human, ai])
        else:
            raise ValueError(
                f"Unsupported chat history format: {type(dialogue_turn)}."
                f" Full chat history: {chat_history} "
            )
    return buffer


class LocalKnowledgeBase():
    def __init__(self, source_files: list, index_name: str, prompt: str):
        """Initialize with source doc and index name'."""
        self.index_name = index_name
        self.index_path = Config.BASE_DIR + '/vectorData/' +  index_name
        self.source_files = source_files
        self.vectordb = None
        self.prompt = prompt

    def index(self):
        # 初始化 openai 的 embeddings 对象
        #embeddings = OpenAIEmbeddings()
        embeddings = BeikeEmbeddings()
        # 将 document 通过 openai 的 embeddings 对象计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
        print("index build start:"+self.index_path)
        if os.path.exists(self.index_path):
            print("index exist")
            # 索引已存在无需重新构建，直接加载即可
            self.vectordb = Chroma(persist_directory=self.index_path, embedding_function=embeddings)
        else:
            # 加载所有文件
            print(self.source_files)
            for source in self.source_files:
                loader = None
                print("load source:"+source["path"])
                if os.path.exists(source["path"]):
                    # 给予文件类型加载各自类型的file_loader
                    loader = FileLoaderFactory.create_loader(source["path"])
                if loader is None:
                    continue
                # doc进行分片
                text_splitter = CharacterTextSplitter(separator=source["doc_separator"], chunk_size=300, chunk_overlap=0)
                pages = loader.load_and_split(text_splitter=text_splitter)
                if self.vectordb is None:
                    print("create new index"+self.index_path)
                    # 基于分片后的pages进行索引构建，存储在chroma中
                    self.vectordb = Chroma.from_documents(pages, embeddings, persist_directory=self.index_path)
                else:
                    print("add new document to exist index:"+self.index_path)
                    # 对于已经存在索引的情况，增加新的pages
                    self.vectordb.add_documents(pages)
            if self.vectordb is not None:
                self.vectordb.persist()
        if self.vectordb is None:
            print("index build fail:"+self.index_name)
            return False
        else:
            print("index build succ:"+self.index_name)
            return True


    def searchBatch(self, questions: list):
        retriever = self.vectordb.as_retriever(search_kwargs={"k": 3})
        qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever,verbose=True)
        for question in questions:
            with get_openai_callback() as cb:
                res = qa.run(question)
                print({question+res})
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost (USD): ${cb.total_cost}")

    def getRelevantDoc(self, question):
        retriever = self.vectordb.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(question)
        return docs

    def search(self, question: str):
        retriever = self.vectordb.as_retriever(search_kwargs={"k": 1})
        qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever,verbose=True)
        with get_openai_callback() as cb:
            res = qa.run(question)
            print({question+res})
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            return res

    def chat_request(self, request_id: str, question: str):
        template = """你是一个专门为房产中介提供新房楼盘的咨询人员，如下内容包含新房楼盘的信息，请根据这些信息以及历史聊天记录回答，回答内容必须是中文：
        {input_document}
        {chat_history}
        Human: {question}
        Chatbot:"""

        history = RedisChatMessageHistory(request_id, ttl=240)
        chat_history_str = _get_chat_history(history.messages)
        print(self.prompt)
        prompt = PromptTemplate(
            input_variables=["chat_history", "question", "input_document"],
            template=self.prompt
        )

        retriever = self.vectordb.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(question)

        condense_question_chain = LLMChain(llm=OpenAI(temperature=0, max_retries=1, model_name="gpt-3.5-turbo"), prompt=prompt)
        with get_openai_callback() as cb:
            answer = condense_question_chain.run(
                question=question, chat_history=chat_history_str, input_document=docs, verbose=True
            )
            print({question+answer})
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            history.add_user_message(question)
            history.add_ai_message(answer)
            return answer


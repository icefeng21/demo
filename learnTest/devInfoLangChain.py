import os

from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

data_path = "/Applications/workSpace/pythonProgram/demo/data/"
file_name = "link_console_contract_poseidon74e347f2-fae0-44be-9445-023ee5fc1914.txt"
file_path = data_path + file_name
BASE_DIR = "/Applications/workSpace/pythonProgram/demo"
vector_path = data_path + "vector" + file_name
# openAI的Key
# os.environ["OPENAI_API_KEY"] = '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'
os.environ["OPENAI_API_KEY"] = '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'
# 导入文本text
loader = UnstructuredFileLoader(
    file_path)
# 导入文本doc
# loader = UnstructuredWordDocumentLoader("")
# 导入csv
# loader = CSVLoader(
#     BASE_DIR + "/data/link_console_contract_poseidon74e347f2-fae0-44be-9445-023ee5fc1914.txt")
# 导入image
# loader = UnstructuredImageLoader(
#     "/Applications/workSpace/pythonProgram/demo/data/wecom-temp-526213-803a77ed7b067d33ed1633e9eb79390a.jpg")

# 将文本转成 Document 对象
document = loader.load()
print(f'documents:{len(document)}')

# 初始化文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

# 分割  documents
documents = text_splitter.split_documents(document)

print(f'documents:{len(documents)}')

# 初始化 openai embeddings
embeddings = OpenAIEmbeddings()
vector_store = None
# 将数据存入向量存储
if os.path.exists(vector_path):
    vector_store = Chroma(persist_directory=vector_path, embedding_function=embeddings)
else:
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory=vector_path)
# 通过向量存储初始化检索器
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

system_template = """
Use the following context to answer the user's question.
If you don't know the answer, say you don't, don't try to make it up. And answer in Chinese.
-----------
{context}
-----------
{chat_history}
"""

# 构建初始 messages 列表，这里可以理解为是 openai 传入的 messages 参数
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template('{question}')
]

# 初始化 prompt 对象
prompt = ChatPromptTemplate.from_messages(messages)

# 初始化问答链
# qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.1, max_tokens=2048), retriever,
#
#                                            condense_question_prompt=prompt)
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="refine", retriever=retriever, verbose=True)

chat_history = []
# 循环输入问题，直到输入 exit 退出
while True:
    try:
        query = input("请输入问题：")
        if not query:
            print("问题为空，请重新输入：")
            continue
        if query == "exit":
            print("退出程序")
            break
        # 判断query是否UTF-8编码（本地测试的时候有时会异常，所以加上这个判断）
        query = query.encode("utf-8").decode("utf-8")
        result = qa.run(query)
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError: ", e)
        continue
    print(result)

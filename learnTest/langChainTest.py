import os

# from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain import OpenAI

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Config:
    '''这里只定义基础的静态配置数据'''
    # APP_NAME = 'python_standard'
    BASE_DIR = "/Applications/workSpace/pythonProgram/demo"
    # HOST_NAME = "http://127.0.0.1:5000"


# openAI的Key
os.environ["OPENAI_API_KEY"] = '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'
# 谷歌搜索的Key
# os.environ["SERPAPI_API_KEY"] = '**********'

# 导入文本
# loader = UnstructuredFileLoader(fr"D:\a\program\pythonProject\b.txt")
loader = UnstructuredWordDocumentLoader("/Users/xugao/Desktop/link_console_contract_poseidond8dce48c-c21d-4d4e-adf4-8a509ca639c6.docx")

# /Users/xugao/Desktop/link_console_contract_poseidond8dce48c-c21d-4d4e-adf4-8a509ca639c6.docx
# 将文本转成 Document 对象
document = loader.load()
print(f'documents:{len(document)}')

# 初始化文本分割器
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0
)

# 切分文本
split_documents = text_splitter.split_documents(document)
print(f'documents:{len(split_documents)}')

# 加载 llm 模型
llm = OpenAI(model_name="text-davinci-003", max_tokens=1500)

"""
chain_type：chain类型
    stuff: 这种最简单粗暴，会把所有的 document 一次全部传给 llm 模型进行总结。如果document很多的话，势必会报超出最大 token 限制的错，所以总结文本的时候一般不会选中这个。
    map_reduce: 这个方式会先将每个 document 进行总结，最后将所有 document 总结出的结果再进行一次总结。
    refine: 这种方式会先总结第一个 document，然后在将第一个 document 总结出的内容和第二个 document 一起发给 llm 模型在进行总结，以此类推。这种方式的好处就是在总结后一个 document 的时候，会带着前一个的 document 进行总结，给需要总结的 document 添加了上下文，增加了总结内容的连贯性。
    这种一般不会用在总结的 chain 上，而是会用在问答的 chain 上，他其实是一种搜索答案的匹配方式。首先你要给出一个问题，他会根据问题给每个 document 计算一个这个 document 能回答这个问题的概率分数，然后找到分数最高的那个 document ，在通过把这个 document 转化为问题的 prompt 的一部分（问题+document）发送给 llm 模型，最后 llm 模型返回具体答案。
"""
# 创建总结链
chain = load_summarize_chain(llm, chain_type="refine", verbose=True)

# 执行总结链，（为了快速演示，只总结前5段）
chain.run(split_documents[:5])
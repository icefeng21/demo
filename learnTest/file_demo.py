import os
# def read():
#     with open('/Users/xugao/Downloads/111', 'r') as f:
#         # print(f.read())
#         for line in f.readlines():
#             print(line.strip()) # 把末尾的'\n'删掉
# # read()
#
# def file1():
#     print(os.name)
#     print(os.uname())
#     print(os.environ.get('PATH'))
#     print(os.path.abspath('.'))
# file1()

# self.index_name = index_name
index_path = "/Applications/workSpace/pythonProgram/openAi-Document-Format"
file_path = index_path + '/data'
# self.source_files = source_files
file_names = os.listdir(file_path)
print(file_names)

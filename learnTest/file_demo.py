import os
def read():
    with open('/Users/xugao/Downloads/111', 'r') as f:
        # print(f.read())
        for line in f.readlines():
            print(line.strip()) # 把末尾的'\n'删掉
# read()

def file1():
    print(os.name)
    print(os.uname())
    print(os.environ.get('PATH'))
    print(os.path.abspath('.'))
file1()
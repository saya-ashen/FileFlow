# 实现简易客户端功能
# 读取本地文件，发送到服务器端

import requests

# 定义文件传输服务端的地址和端口
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8000

# 定义文件传输服务端的URL
UPLOAD_URL = f"http://{SERVER_ADDRESS}:{SERVER_PORT}/upload"

# 每次读取文件的大小
CHUNK_SIZE = 1024 * 1024

# 循环读取本地文件
with open("../test/testfile.png", "rb") as f:
    while True:
        # 读取文件内容
        file_content = f.read(CHUNK_SIZE)
        if not file_content:
            break

        # 构造JSON格式的文件信息
        filename = "testfile.png"
        filesize = len(file_content)
        file_info = {
            "filename": filename,
            "filesize": filesize,
            "filecontent": file_content,
        }

        # 将文件信息发送到文件传输服务端
        response = requests.post(UPLOAD_URL, json=file_info)

        # 返回上传结果
        if response.status_code == 200:
            print(response.json())
        else:
            print("文件上传失败")
            break

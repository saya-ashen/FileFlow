# 实现一个文件传输的服务端，服务端和客户端之间使用josn格式的数据进行通信，客户端上传文件时先发送文件的大小，然后发送文件的内容，服务端接收到文件后，将文件保存到本地
# josn文件格式：{"filename": "test.txt", "filesize": 1024, "filecontent": "xxxxxx"}，其中filecontent是文件的内容，使用base64编码
# 服务端接收到文件后，将文件保存到本地，文件名为filename，文件内容为filecontent，文件大小为filesize，文件先进行base64解码，将分片的文件内容拼接起来，然后保存到本地
# 服务端接收到文件后，返回一个json格式的数据，{"status": "success", "msg": "文件上传成功"}，其中status表示上传状态，msg表示上传的消息

# 首先实现一个http服务，用于接收文件上传的请求，然后实现一个文件上传的服务，用于接收文件的内容，最后实现一个文件保存的服务，用于将文件保存到本地
# 服务端使用多线程的方式实现，每个线程都是一个独立的服务，用于接收一个客户端的请求，然后将文件保存到本地

import http.server
import json
import socketserver
import urllib.parse

import requests

# 定义文件传输服务端的地址和端口
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8000

# 定义文件传输服务端的URL
UPLOAD_URL = f"http://{SERVER_ADDRESS}:{SERVER_PORT}/upload"


# 定义HTTP请求处理器
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # 解析请求参数
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        post_data = urllib.parse.parse_qs(post_data.decode())
        filename = post_data["filename"][0]
        filecontent = post_data["filecontent"][0]

        # 构造JSON格式的文件信息
        filesize = len(filecontent)
        file_info = {
            "filename": filename,
            "filesize": filesize,
            "filecontent": filecontent,
        }

        # 将文件信息发送到文件传输服务端
        response = requests.post(UPLOAD_URL, json=file_info)

        # 返回上传结果
        if response.status_code == 200:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.content)
        else:
            self.send_error(500, "文件上传失败")


# 启动HTTP服务器
with socketserver.TCPServer(("", 8080), RequestHandler) as httpd:
    print("HTTP服务器已启动, 监听端口8080...")
    httpd.serve_forever()

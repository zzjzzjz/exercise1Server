# import util.file as fileUtil
import os

import util.file_tree as fileUtil
import socket
import json
import time
import hashlib
import select
UDP_SEND_DATA_SIZE = 1024 * 10  # udp一次发送的数据大小
from threading import Thread



def startFileDirectoryServer(path: str, ip: str, port: int):

    files = getfiletree(path)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    while True:
        client, addr = server.accept()
        print(str(client) + "  " + str(addr))
        th = Thread(target=__fileDirectory, args=(client, files))
        th.start()


def __fileDirectory(client, files: list):
    for line in files:
        if line == '\n' or line == '':
            client.setblocking(False)
            # 清空缓存
            clearSocketBuffer(client)
            client.setblocking(True)
            pass
        length = str(len(line.encode('utf8')))
        client.send(length.encode('utf8'))# 解决粘包问题
        ready = client.recv(1024).decode('utf8')
        if ready != length:
            print('文件目录获取错误')
            break
        client.send(line.encode('utf8'))
    client.close()


def startFileTCPTransferServer(path: str, ip: str, port: int):
    try:
        CONNECT_TUBLE = (ip, port)
        # print('TCP > '+str(CONNECT_TUBLE))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(CONNECT_TUBLE)
        server.listen(10)
    except OSError:
        print("该请求的地址无效!!!TCP传输失败")

    while True:
        client, addr = server.accept()
        th = Thread(target=__fileTCPTransfer, args=(client, path))
        th.start()


def __fileTCPTransfer(client, path: str):
    fileName = client.recv(4096)
    path = path + "/" + fileName.decode("utf-8")

    print(path)
    try:

        file = open(path, 'rb')
        fileSize = os.stat(path).st_size
        print(fileSize)
    except:  # 文件不存在则关闭连接
        sendData = {'ok': False}
        sendData = str(sendData).encode('utf-8')
        client.send(sendData)
        client.close()
        return
    sendData = {'ok': True, 'fileSize': fileSize}
    sendData = str(sendData).encode('utf-8')
    print(sendData)
    client.send(sendData)
    data = file.read(1024 * 5)
    while data:
        client.send(data)
        data = file.read(1024 * 5)
    file.close()
    client.close()


def startFileUDPTransferServer(path: str, ip: str, port: int):
    try:
        CONNECT_TUBLE = (ip,port)
        # print('UDP > '+str(CONNECT_TUBLE))
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(CONNECT_TUBLE)
    except OSError:
        print("该请求的地址无效!!!UDP传输失败")
    while True:
        data, addr = server.recvfrom(1024)  # 收到用户文件请求信息
        data = eval(data.decode('utf-8'))  # 将接受信息转化为字典类型，{'fileName':x,'id':x}包括请求文件名以及偏移量。
        try:
            file = open(path + '\\' + data['fileName'], 'rb')  # 打开文件
            # print("大小:" + str(os.stat(path + '\\' + data['fileName']).st_size))
            # print("偏移量:" + str(UDP_SEND_DATA_SIZE * data['id']))
            print(str((UDP_SEND_DATA_SIZE * data['id'])/(os.stat(path + '\\' + data['fileName']).st_size)))
            file.seek(UDP_SEND_DATA_SIZE * data['id'])  # 请求文件偏移量
            fileData = file.read(UDP_SEND_DATA_SIZE)  # 读取数据
            file.close()
            if not fileData:  # 文件读取已结束
                sendData = {'id': data['id'], 'fileData': fileData, 'end': True, 'ok': True,
                            'per': 100}  # ok代表是否成功读取文件数据
            else:
                per = int(
                    (UDP_SEND_DATA_SIZE * data['id'] / os.stat(path + '\\' + data['fileName']).st_size) * 100)  # 进度
                sendData = {'id': data['id'], 'fileData': fileData, 'end': False, 'per': per,
                            'ok': True}  # 封装响应信息，包含数据偏移量、文件字节数据、文件是否结束，并转化为bytes类型
            __addMd5ToDict(sendData)  # 给sendData字典加上他对应的md5值
            sendData = str(sendData).encode('utf-8')

            server.sendto(sendData, addr)
        except:
            sendData = {'id': 0, 'fileData': b'', 'end': False, 'ok': False}
            __addMd5ToDict(sendData)  # 给sendData字典加上他对应的md5值
            server.sendto(str(sendData).encode('utf-8'), addr)

    # th = Thread(target=__fileUDPTransfer, args=(server, path))
    # th.start()


def __fileUDPTransfer(server, basePath: str):  # 不用了
    while True:
        print('开始')
        path = basePath
        data, addr = server.recvfrom(1024 * 10)  # 文件下载请求
        data = eval(data.decode('utf-8'))

        if (data['type'] == 1):  # type=1判断是不是请求文件的请求
            fileName = data['fileName']  #
            path = path + "\\" + fileName
            file = open(path, 'rb')
            id = 0
            fileData = file.read(1024)
            while fileData:
                sendData = {'id': id, 'data': fileData, 'end': False}
                server.sendto(str(sendData).encode('utf-8'), addr)
                data, addr = server.recvfrom(1024)
                data = eval(data.decode('utf-8'))
                print(data)
                id = data['id']
                file.seek(id * 1024)
                fileData = file.read(1024)
                print(str(id))
            print('结束')
            sendData = {'id': id, 'end': True}
            server.sendto(str(sendData).encode('utf-8'), addr)
            print(data)



def __addMd5ToDict(ob: dict):  # 在字典对象中加入md5值的属性
    md5 = hashlib.md5(str(ob).encode('utf-8')).hexdigest()
    ob['md5'] = md5


def getfiletree(path):
    # files = fileUtil.findFilesByPath(path)
    fileUtil.begin(path)
    files = []
    # length = 0
    all_file_txt = open(file="./all_file.txt", encoding='utf8', mode='r')
    for line in all_file_txt.readlines():
        # length = length + len(line)
        files.append(line.strip('\n'))
    all_file_txt.close()
    return files

def clearSocketBuffer(conn: socket.socket):
    timeout_in_seconds = 0.5
    while True:
        ready = select.select([conn], [], [], timeout_in_seconds)
        if ready[0]:
            data = conn.recv(4)
            print("清空数据:", data)
        else:
            print('超时清空')
            return

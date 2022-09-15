import util.file as fileUtil
import socket
import json
import time
from threading import Thread
def startFileDirectoryServer(path:str,ip:str,port:int):
    files = fileUtil.findFilesByPath(path)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(10)
    while True:
        client, addr = server.accept()
        print(str(client)+"  "+str(addr))
        th=Thread(target=__fileDirectory,args=(client,files))
        th.start()


def __fileDirectory(client,files:list):
    client.send(json.dumps(files).encode('utf-8'))
    client.close()
def startFileTCPTransferServer(path:str,ip:str,port:int):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,9091))
    server.listen(10)

    while True:
        client, addr = server.accept()
        th = Thread(target=__fileTCPTransfer, args=(client, path))
        th.start()

def __fileTCPTransfer(client,path:str):

    fileName=client.recv(4096)
    path=path+"\\"+fileName.decode("utf-8")
    print(path)
    file=open(path,'rb')

    data=file.read(1024)
    while data:
        client.send(data)
        print('12')
        data=file.read(1024)
    file.close()
    client.close()


def startFileUDPTransferServer(path:str,ip:str,port:int):
    server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind((ip,port))


    th = Thread(target=__fileUDPTransfer, args=(server, path))
    th.start()

def __fileUDPTransfer(server, basePath: str):
    while True:
        print('开始')
        path=basePath
        data,addr=server.recvfrom(1024)#文件下载请求
        data=eval(data.decode('utf-8'))

        if(data['type']==1):#type=1判断是不是请求文件的请求
            fileName=data['fileName']#
            path = path + "\\" + fileName
            file=open(path,'rb')
            id=0
            fileData=file.read(1024)
            while fileData:
                sendData={'id':id,'data':fileData,'end':False}
                server.sendto(str(sendData).encode('utf-8'), addr)
                data,addr=server.recvfrom(1024)
                data=eval(data.decode('utf-8'))
                print(data)
                id=data['id']
                file.seek(id*1024)
                fileData=file.read(1024)
                print(str(id))
            print('结束')
            sendData={'id':id,'end':True}
            server.sendto(str(sendData).encode('utf-8'),addr)
            print(data)
            
            

        #file = open(path, 'rb')

    

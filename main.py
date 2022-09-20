import util.file as fileUtil
import util.network as networkUtil
import threading
import socket
BASE_PATH="E:/test"

if __name__=="__main__":

    th=threading.Thread(target=networkUtil.startFileDirectoryServer,args=(BASE_PATH,"0.0.0.0",9090))#访问文件列表进程
    th.start()
    th1 = threading.Thread(target=networkUtil.startFileTCPTransferServer, args=(BASE_PATH, "0.0.0.0", 9091))#TCP传输文件进程
    th1.start()
    networkUtil.startFileUDPTransferServer(BASE_PATH, "0.0.0.0",9092)#UDP传输文件进程
import util.file as fileUtil
import util.network as networkUtil
import threading
import socket
DEST_IP = "0.0.0.0"
DEST_PORT = 9091
BASE_PATH = "D://作业//网络攻击与防御"

if __name__ == "__main__":
    th = threading.Thread(target=networkUtil.startFileDirectoryServer, args=(BASE_PATH, "0.0.0.0", 9090))  # 访问文件列表进程
    th.start()
    th1 = threading.Thread(target=networkUtil.startFileTCPTransferServer,
                           args=(BASE_PATH, "0.0.0.0", 9091))  # TCP传输文件进程
    th1.start()
    networkUtil.startFileUDPTransferServer(BASE_PATH, "0.0.0.0", 9092)  # UDP传输文件进程

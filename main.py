import util.file as fileUtil
import util.network as networkUtil
import threading
import socket
# DEST_IP = "192.168.88.129"
DEST_IP = "0.0.0.0"
BASE_PATH = "D:\OneDrive - bestpigs\Videos\录屏"

if __name__ == "__main__":
    th = threading.Thread(target=networkUtil.startFileDirectoryServer, args=(BASE_PATH, '0.0.0.0', 9090))  # 访问文件列表进程
    th.start()
    th1 = threading.Thread(target=networkUtil.startFileTCPTransferServer,
                           args=(BASE_PATH, DEST_IP, 9091))  # TCP传输文件进程
    th1.start()
    th2 = threading.Thread(target=networkUtil.startFileUDPTransferServer,args=(BASE_PATH, DEST_IP, 9092))
    # networkUtil.startFileUDPTransferServer(BASE_PATH, DEST_IP, 9092)  # UDP传输文件进程
    th2.start()

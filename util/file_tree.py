import os
import os.path


def begin(BASE_PATH):
    # BASE_PATH = 'D:\\作业\\网络攻击与防御'
    all_file_txt = open(file="./all_file.txt", encoding='utf8', mode='w')
    all_file_txt.close()
    all_file_txt = open(file="./all_file.txt", encoding='utf8', mode='a+')
    dfs_showdir(BASE_PATH, 0, all_file_txt)
    all_file_txt.close()

def dfs_showdir(path, depth, filename):
    try:
        if depth == 0:
            rootpath = "root:[" + path + "]"
            # print(rootpath)
            filename.writelines(rootpath+"\n")
        for item in os.listdir(path):
            if '.git' not in item:
                filetree = "| " * depth + "+--" + item
                # print(filetree)
                filename.write(filetree+"\n")
                newitem = path + '/' + item
                if os.path.isdir(newitem):
                    dfs_showdir(newitem, depth + 1, filename)
    except PermissionError:
        pass


if __name__ == '__main__':
    BASE_PATH = 'D:\\作业\\网络攻击与防御'
    all_file_txt = open(file="./all_file.txt", encoding='utf8', mode='w')
    all_file_txt.close()
    all_file_txt = open(file="./all_file.txt", encoding='utf8', mode='a+')
    dfs_showdir(BASE_PATH, 0, all_file_txt)
    all_file_txt.close()
    print("文件树写入完成...")

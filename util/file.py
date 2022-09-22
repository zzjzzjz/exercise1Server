import os


def findFilesByPath(path):
    try:
        files = os.listdir(path)
    except:
        return None
    return files


if __name__ == '__main__':
    result = findFilesByPath("C:\\Users\\86133\\Desktop\\大创")
    if result == None:
        print("it is none")
    else:
        print(result)

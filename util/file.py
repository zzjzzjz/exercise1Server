import os


def findFilesByPath(path):
    try:
        files=os.listdir(path)
    except:
        return None
    return files



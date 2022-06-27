import os


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print(path + " " + "successfully create")
        return True
    else:
        print(path + "directory already exists")
        return False

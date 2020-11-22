import os
def check_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
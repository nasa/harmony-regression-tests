import os

def cleanup(file):

    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file " + file + " does not exist")

    return

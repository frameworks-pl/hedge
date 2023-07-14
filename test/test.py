import os

for file in os.listdir("."):
    if not os.path.isdir(file) and file.endswith(".py") and file != __file__:
        print("{file}".format(file=file))

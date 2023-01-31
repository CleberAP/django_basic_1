import os

class MyKeys:

    def __init__(self):
        self.dict_keys = {}
        self.read_file_to_dict()

    def read_file_to_dict(self):
        try:
            file_path = os.getcwd()+"\\my_keys.txt"
        except:
            file_path = os.getcwd()+"/my_keys.txt"
        file = open(file_path, mode='r')
        lines = file.readlines()
        file.close()

        for line in lines:
            list_line = line.split(":::")
            self.dict_keys[list_line[0]] = list_line[1].strip()


    def get_by_key(self, key):
        return self.dict_keys[key]

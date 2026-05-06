from io import BytesIO
import datetime as dt
import json as js

class Users():
    "The class to save user's data..."

    def __init__(self, output_path):
        self.output_path = output_path
        self.omit_keys = ["matrix_status", "matrix_input", "matrix", "chain"]

    #Saving the user's data...
    def save_user_data(self, chat_id, the_data):
        file = open(self.output_path + str(chat_id) + ".json", "w")
        filtered_data = dict((k, v) for k, v in the_data.items() if not k in self.omit_keys)
        js.dump(the_data, file, skipkeys=True, indent=1)
        file.close()

    #To recover the user's data...
    def load_user_data(self, chat_id, chat_data):
        try:
            the_data = js.load(open(self.output_path + str(chat_id) + ".json", "r"))
            for key in the_data:
                chat_data[key] = the_data[key]
        except:
            pass

    #To create a new matrix text file for the user...
    def new_matrix(self, chat_id, header, matrix_string):
        file = open(self.output_path + str(chat_id) + "_matrix.txt", "w")
        file.write(header)
        file.write(matrix_string)
        file.write("\n\n")
        file.close()

    #To update the user's matrix text file...
    def update_matrix(self, chat_id, operation, matrix_string):
        file = open(self.output_path + str(chat_id) + "_matrix.txt", "a")
        file.write(operation + "\n\n")
        file.write(matrix_string)
        file.write("\n\n")
        file.close()

    #To get the user's matrix text file...
    def get_matrix_history(self, chat_id):
        return open(self.output_path + str(chat_id) + "_matrix.txt", "r")

    #Printing Users()...
    def __str__(self):
        return "- musiCal Bot\n" + \
                "  I am the class in charge of working with user's data...\n" + \
                "  gitlab.com/musicaltools/caltoolsbot\n" + \
                "  rodrigovalla@protonmail.ch"

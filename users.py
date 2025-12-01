import datetime as dt
import json as js

class Users():
    "The class to save user's data..."

    def __init__(self, output_path):
        self.output_path = output_path
        self.omit_keys = ["matrix", "chain"]

    #Saving the user's data...
    def save_user_data(self, id, the_data):
        file = open(self.output_path + str(id) + ".json", "w")
        filtered_data = dict((k, v) for k, v in the_data.items() if not k in self.omit_keys)
        js.dump(the_data, file, skipkeys=True, indent=1)
        file.close()

    #To recover the user's data...
    def load_user_data(self, id, chat_data):
        try:
            the_data = js.load(open(self.output_path + str(id) + ".json", "r"))
            for key in the_data:
                chat_data[key] = the_data[key]
        except:
            pass

    #Printing Users()...
    def __str__(self):
        return "- musiCal Bot\n" + \
                "  I am the class in charge of working with user's data...\n" + \
                "  gitlab.com/musicaltools/caltoolsbot\n" + \
                "  rodrigovalla@protonmail.ch"

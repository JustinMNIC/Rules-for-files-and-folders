import shutil
import os
import customtkinter as ctk
import json

"""
criteria = {
    "name": "all" or [], # if "all" then select all files, if [] then for each name in the list select the files only if the name is in the list
    "type": "all" or [], # if "all" then select all files, if [] then for each type in the list select the files only if the type is in the list
    "size": "all" or {"above_or_below": "above",
                        "size": ""}, # if "all" then select all files, if {"above_or_below": "above", size} then select files above the size, if {"above_or_below": "below", size} then select files below the size
    "date_modified": "all" or {"before_or_after": "before",
                                "date": ""}, # if "all" then select all files, if {"before_or_after": "before", date} then select files before the date, if {"before_or_after": "after", date} then select files after the date
}

exception = {
    "name": None or [], # if None pass this criteria, if [] for each str in the list select the files only if the name is not in the list
    "type": None or [], # if None pass this criteria, if [] for each type in the list select the files only if the type or file is not in the list ( explample: directory, .png, .html etc.)
    "size": None or {"above_or_below": "above",
                        "size": ""}, # if none pass this criteria, if {"above_or_below": "above", size} then do not select the files above the size, if {"above_or_below": "below", size} then do not select files below the size
    "date_modified": None or {"before_or_after": "before",
                                "date": ""},  # if None pass this criteria, if {"before_or_after": "before", date} then do not select files before the date, if {"before_or_after": "after", date} then do not select files after the date
}
"""


class Executor_Rule():
    def __check_criteria(self, file, criteria):
        if criteria["name"] == "all" or file.name in criteria["name"]:
            if criteria["type"] == "all" or file.type in criteria["type"]:
                if criteria["size"] == "all" or ((criteria["size"]["above_or_below"] == "above" and file.size > criteria["size"]["size"])) or ((criteria["size"]["above_or_below"] == "below" and file.size < criteria["size"]["size"])):
                    if criteria["date_modified"] == "all" or ((criteria["date_modified"]["before_or_after"] == "before" and file.date_modified < criteria["date_modified"]["date"])) or (criteria["date_modified"]["before_or_after"] == "after" and file.date_modified > criteria["date_modified"]["date"]):
                        return True
        return False
    
    def __check_exception(self, file, exception):
        if exception["name"] == None or file.name not in exception["name"]:
            if exception["type"] == None or file.type not in exception["type"]:
                if exception["size"] == None or ((exception["size"]["above_or_below"] == "above" and file.size > exception["size"]["size"])) or ((exception["size"]["above_or_below"] == "below" and file.size < exception["size"]["size"])):
                    if exception["date_modified"] == None or ((exception["date_modified"]["before_or_after"] == "before" and file.date_modified < exception["date_modified"]["date"])) or (exception["date_modified"]["before_or_after"] == "after" and file.date_modified > exception["date_modified"]["date"]):
                        return True
        return False
        
    def move_files(self, source, destination, criteria = None, exception = None):
        for file in os.scandir(source):
            if file.is_file():
                if criteria != None:
                    if self.__check_criteria(file, criteria):
                        if exception != None:
                            if self.__check_exception(file, exception):
                                shutil.move(file, destination)
                        else:
                            shutil.move(file, destination)
                else:
                    if exception != None:
                        if self.__check_exception(file, exception):
                            shutil.move(file, destination)
                    else:
                        shutil.move(file, destination)
            else:
                self.move_files(file, destination, criteria, exception)
                
    def copy_files(self, source, destination, criteria = None, exception = None):
        for file in os.scandir(source):
            if file.is_file():
                if criteria != None:
                    if self.__check_criteria(file, criteria):
                        if exception != None:
                            if self.__check_exception(file, exception):
                                shutil.copy(file, destination)
                        else:
                            shutil.copy(file, destination)
                else:
                    if exception != None:
                        if self.__check_exception(file, exception):
                            shutil.copy(file, destination)
                    else:
                        shutil.copy(file, destination)
            else:
                self.copy_files(file, destination, criteria, exception)
                
    def delete_files(self, source, criteria = None, exception = None):
        for file in os.scandir(source):
            if file.is_file():
                if criteria != None:
                    if self.__check_criteria(file, criteria):
                        if exception != None:
                            if self.__check_exception(file, exception):
                                os.remove(file)
                        else:
                            os.remove(file)
                else:
                    if exception != None:
                        if self.__check_exception(file, exception):
                            os.remove(file)
                    else:
                        os.remove(file)
            else:
                self.delete_files(file, criteria, exception)
        
        
class GUI_Rules_for_files_and_folders(ctk.CTk):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title("Rules for files and folders")
            self.geometry("1000x800")
            
            self.grid_columnconfigure([i for i in range(4)], weight = 1, uniform= "yes")
            self.grid_rowconfigure([i for i in range(13)], weight = 1, uniform= "yes")
            
            
            ### Display rules
            self.frame_my_rules = ctk.CTkFrame(self)
            self.frame_my_rules.grid(row = 0, column = 0, columnspan = 1, rowspan = 13, sticky = "news")
            
            self.label_for_my_rules = ctk.CTkLabel(self.frame_my_rules, text = "My rules", font = ("Arial", 20))
            self.label_for_my_rules.pack(side = "top", fill = "x")
            
            ### button new rule
            self.button_new_rule = ctk.CTkButton(self, text = "New rule", command = self.new_rule)
            self.button_new_rule.grid(column = 1, row = 0, sticky = "news")
            
    def new_rule(self):
        # open the windows explorer where the user can select the directory
        pass
            
            


if __name__ == "__main__":
    app = GUI_Rules_for_files_and_folders()
    app.mainloop()
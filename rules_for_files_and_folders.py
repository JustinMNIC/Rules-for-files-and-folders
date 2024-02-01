import customtkinter as ctk
import getpass
import os
from tkinter import filedialog
import shutil

appearange_program = "system"
ctk.set_appearance_mode(appearange_program)

class Rules(ctk.CTk):
    if ctk.get_appearance_mode == "light":
        _bg_oposite_col = "black"
        _text_oposite_col = "white"
    else:
        _bg_oposite_col = "white"
        _text_oposite_col = "black"
    
    var_first_timer = False #TODO integrate this into the json file 
    
    var_info_about_the_dir_selected = "Please select a directory"
    
    welcome_messages = [
        "Welcome to 'Rules for files and folders'",
        "This program helps you organize your files and folders.\n\nYou can perform different tasks with this program, for example:\ncopy, edit, rename, sort, move files (and other functions).\n",
        "If anything doesn't work as expected, email me at: <iustin.cordon@yahoo.com>",
        "Good luck! :)"
    ]
    
    dict_cash_for_the_curent_rule = {}
    
    #______________________ vars above 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Rules for files and folders")
        
        self.geometry("820x420")
        
        self.grid_rowconfigure([i for i in range(40)], weight= 1, uniform= "yes")   # >> 1 row or col == 21 pix  
        self.grid_columnconfigure([i for i in range(20)], weight= 1, uniform = "yes")   # rows&col config. will be changed after the welcome message  
        
        #when the program starts
        self.message_at_the_start = ctk.CTkLabel(self, text = "")
        self.message_at_the_start.grid(row=14, rowspan=5, column=9, columnspan=2, sticky = "ns")
        
        #main-menu 
        self.ask_for_dir = ctk.CTkEntry(self, placeholder_text= "Ctrl C + V  your PATH here.. or -->", corner_radius= 10)

        self.ask_for_dir.bind("<Key>", lambda event: self.update_var_info_about_the_dir_selected(current_directory=self.ask_for_dir.get()))

        self.button_ask_dir = ctk.CTkButton(self, text= "Click here to select folder", command= self.comand_ask_dir, corner_radius= 30)
        
        #main-menu > display info about the dir selected
        
        self.info_about_the_dir_selected = ctk.CTkLabel(master = self,
                                                        text= self.var_info_about_the_dir_selected,
                                                        corner_radius= 7,
                                                        bg_color= self._bg_oposite_col,
                                                        font= ("Arial", 14),
                                                        text_color= self._text_oposite_col)
        
        # main-menu > > what files, folders, what action to be performed, exeptions etc 
        
        self.drop_down_menu_what_files = ctk.CTkOptionMenu(master = self,
                                                           values= ["All files", "All files exept..","Specific files"],
                                                           command= self.command_for_drop_down_menu_what_files)
        self.drop_down_menu_what_files.set("All files")
        
        
        self.drop_down_menu_what_action_will_be_performed = ctk.CTkOptionMenu(master = self,
                                                                              values= ["Move", "Copy", "Delete", "Sort folder (must be a folder)"],
                                                                              command= lambda event: self.commad_for_drop_down_menu_what_action_will_be_performed(action = self.drop_down_menu_what_action_will_be_performed.get()))


        self.wanna_save_the_rule_for_later = ctk.CTkSegmentedButton(master = self,
                                                                    values = ["Don't save this rule", "Save it for later"],
                                                                    command= lambda x: self.commad_for_wanna_save_the_rule_for_later(self.wanna_save_the_rule_for_later.get()))
        self.wanna_save_the_rule_for_later.set("Don't save this rule")
        
        self.drop_dowon_menu_when_do_you_want_the_rule_to_rul = ctk.CTkOptionMenu(master = self,
                                                                                  values= ["Contonuesly", "Every X time", "At a specific event"],
                                                                                  command= lambda x: self.command_for_drop_dowon_menu_when_do_you_want_the_rule_to_rul(self.drop_dowon_menu_when_do_you_want_the_rule_to_rul.get()))
        
        self.Every_X_time_when_exactly = ctk.CTkEntry(master = self,
                                                      placeholder_text= "Type please")
        
        self.button_run = ctk.CTkButton(master = self,
                                        text = "Run",
                                        command= self.command_for_button_run)
        ##functions to run at the start 
        
        #UX stuff, just chnage the welcome mesage depending wether the user is a first-timer or not 
        self.are_you_a_first_timer(self.var_first_timer)
        

#_________________________________________________________________________________________________________________________________________________________________________________________________
    def are_you_a_first_timer(self, var_first_timer):
        if var_first_timer:
            index = 0
            self.first_timer(index)
        elif not var_first_timer:
            self.welcome_back()
   
    def first_timer(self, index):
        if index  > 3:
            self.after(1000, self.show_main_frame) 
        else:
            sentence = self.welcome_messages[index]
            self.message_at_the_start.configure(text = sentence) # the range that it reffers to is the 'welcome_message' var (class var:list)
            
            if len(sentence) // 3 < 40:
                reading_time = 3500
            else:
                reading_time = 5500
                
            self.after(reading_time, lambda i = index + 1: self.first_timer(i))

    def welcome_back(self):
        try:
            user = getpass.getuser()
        except:
            user = ""
        self.message_at_the_start.configure(text = f"Welcome back {user} !!")
        self.after(1, self.show_main_frame) #TODO -- change the timer to 2500 , after 
        
    ### main-frame_________ 
    
    #place the widgets 
    def show_main_frame(self):
        self.message_at_the_start.destroy()
        self.geometry("1200x600")
        self.ask_for_dir.grid(row = 1, rowspan = 3, column = 0, columnspan = 9, padx = 2, sticky = "news")
        self.button_ask_dir.grid(row = 1, rowspan = 3, column = 9, columnspan = 2, padx = 2, sticky = "news")
        
        self.info_about_the_dir_selected.grid(row = 0, rowspan = 40, column = 11, columnspan = 9, padx = 2, pady = 2, sticky = "news") 
        
        self.drop_down_menu_what_files.grid(row = 5, rowspan = 2, ipady = 2, column = 0, columnspan = 9, sticky = "ew")        
        self.drop_down_menu_what_action_will_be_performed.grid(row = 9, rowspan = 2, ipady = 2, column = 0, columnspan = 9, sticky = "ew")
        self.wanna_save_the_rule_for_later.grid(row = 14, rowspan = 2, ipady = 2, column = 0, columnspan = 2, sticky = "news")
        
        self.button_run.grid(row = 39, rowspan = 2, ipady = 2, ipadx= 2, column = 8, columnspan = 3, sticky = "news")

    #display info about the dir selected 
    def comand_ask_dir(self):
        current_directory = filedialog.askdirectory(title="Select a directory")
        self.update_var_info_about_the_dir_selected(current_directory)
    
    def update_var_info_about_the_dir_selected(self, current_directory):
        try:
            with os.scandir(current_directory) as it:
                files_in_selected_dir = ""
                for entry in it:
                    if entry.is_file():
                        file_type = entry.name.split('.')[-1] +" file" if '.' in entry.name else "Unknown"
                    elif entry.is_dir():
                        file_type = "Folder"
                    else:
                        file_type = "Unknown"
                    
                    files_in_selected_dir += f"{file_type}: {entry.name}\n"
        except:
            files_in_selected_dir = "Please make sure the path is correct"

        self.dict_cash_for_the_curent_rule["dir"] = current_directory #update the dict the for the current rule 
        
        self.var_info_about_the_dir_selected = f"Directory selected: {current_directory} \n\n {files_in_selected_dir}"
        self.info_about_the_dir_selected.configure(text = self.var_info_about_the_dir_selected)
            
    #the user chooses what happens with the dir they have selected
    def command_for_drop_down_menu_what_files(self, choice):                                                    #"All files", "All files exept..","Specific files",
        self.dict_cash_for_the_curent_rule["files"] = choice
        if choice == "All files":
            self.user_selected_all_files()
        elif choice == "All files exept..":
            self.user_selected_all_files_exept_something__ask()
        elif choice == "Specific files":
            self.user_selected_specific_files()

    
    def user_selected_all_files(self):
        pass
    
    def user_selected_all_files_exept_something__ask(self):
        pass
    
    def user_selected_specific_files(self):
        pass
    
    #actions 
    def commad_for_drop_down_menu_what_action_will_be_performed(self, action):                                   # "Move", "Copy", "Delete", "Sort folder (must be a folder)"
        self.dict_cash_for_the_curent_rule["action"] =  action
    
    #save_for_later in Json format 
    def commad_for_wanna_save_the_rule_for_later(self, value):
        if value == "Save it for later":
            self.dict_cash_for_the_curent_rule["save"] = "yes"
            self.drop_dowon_menu_when_do_you_want_the_rule_to_rul.grid(row = 17, rowspan = 2, column = 0, columnspan = 3, ipady = 2, sticky = "ew")
        elif value == "Don't save this rule":
            self.dict_cash_for_the_curent_rule["save"] = "no"
            
    def command_for_drop_dowon_menu_when_do_you_want_the_rule_to_rul(self, value):                              # "Contonuesly", "Every X time", "At a specific time"
        self.dict_cash_for_the_curent_rule["when_run"] = value
        print(self.dict_cash_for_the_curent_rule)
        
        if value == "Every X time":
            self.Every_X_time_when_exactly.grid(row = 19, rowspan = 2, ipady = 2, ipadx = 2, column = 0, columnspan = 3, sticky = "ew")
            self.Every_X_time_when_exactly.bind("<Key>", lambda event: self.validator(string = self.Every_X_time_when_exactly.get()))
    
    #run the actual script                                                                         {'dir': 'C:/Users/iusti/Desktop/stuff', 'files': 'All files', 'action': 'Move', 'save': 'yes', 'when_run': 'Contonuesly'}
    def command_for_button_run(self, directory, files_option, action):
        files = []

        if files_option == 'All files':
            files = get_files_in_directory(directory)
        elif files_option == 'Specific files':
            # Modify this condition based on your specific criteria
            # Here, it selects files containing 'keyword' in their names
            files = [file for file in get_files_in_directory(directory) if 'keyword' in file.name]

        if action == 'Move':
            destination = 'path/to/move/files'
            move_files(files, destination)
        elif action == 'Delete':
            delete_files(files)
        elif action == 'Rename':
            new_name = 'new_name.txt'
            rename_files(files, new_name)
        elif action == 'Sort':
            destination = 'path/to/sort/files'
            sort_files_by_type(files, destination)
    

    def get_files_in_directory(self, dir, what):
        with os.scandir(dir) as entries:
            if what == "files":
                return [entry for entry in entries if entry.is_file()]
            elif what == "folders":
                return [entry for entry in entries if entry.is_dir()]

    def move_files(files, destination):
        for file in files:
            shutil.move(file.path, destination)

    def delete_files(files):
        for file in files:
            os.remove(file.path)

    def rename_files(files, new_name):
        index = 0
        for file in files:
            if index == 0:
                new_path = os.path.join(os.path.dirname(file.path), new_name)
                os.rename(file.path, new_path)
            else:
                new_path = os.path.join(os.path.dirname(file.path), new_name + f"({index})")
                os.rename(file.path, new_path)
            index += 1

    def sort_files_by_type(files, destination):
        for file in files:
            file_type = file.name.split('.')[-1] if '.' in file.name else 'Unknown'
            file_type_folder = os.path.join(destination, file_type)

            if not os.path.exists(file_type_folder):
                os.makedirs(file_type_folder)

            new_path = os.path.join(file_type_folder, file.name)
            shutil.move(file.path, new_path)
    
if __name__ == "__main__":
    rules = Rules()
    rules.mainloop()
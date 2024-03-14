import shutil
import os
import customtkinter as ctk
import json
from tkinter import filedialog, messagebox 
from PIL import Image
import time 

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


ctk.set_default_color_theme("green")# Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("dark")# Modes: "system" (standard), "light", "dark"

class GUI_Rules_for_files_and_folders(ctk.CTk):
    current_directory = ""
    count_panda = 0

    cash_criteria_name = []
    cash_criteria_type = []
    cash_criteria_size = {}
    
    cash_exception_name = []
    cash_exception_type = []
    cash_exception_size = {}
    
    cash_criterias_selected = ""
    cash_exceptions_selected = ""
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title("Rules for files and folders")
            self.geometry("1050x803")   #y = 73 (one unit of height)
            
            ### Display rules
            self.frame_display_rules = ctk.CTkFrame(master = self,
                                                    width= 300,
                                                    height = 803)
            self.frame_display_rules.place(x = 0, y = 0)
            self.label_my_rules = ctk.CTkLabel(master = self.frame_display_rules,
                                               text = "My Rules",
                                               font = ("Consolas", 24, "bold"),
                                               text_color= "lightblue")
            self.label_my_rules.place(x = 100, y = 10)
            
            self.scrollable_frame_for_my_rules = ctk.CTkScrollableFrame(master = self.frame_display_rules,
                                                                        width = 300,
                                                                        height = 750)
            self.scrollable_frame_for_my_rules.place(x = 0, y = 50)
            
            ### frame for buttons and entrie
            self.frame_for_buttons = ctk.CTkFrame(master = self,
                                                  width = 750,
                                                  height = 73,
                                                  border_width = 1)
            self.frame_for_buttons.place(x = 300, y = 0)
            
            self.button_new_rule = ctk.CTkButton(master = self.frame_for_buttons,
                                                 text = "New Rule",
                                                 font = ("Consolas", 22),
                                                 command = self.create_new_rule,
                                                 fg_color= "green",
                                                 hover_color= "darkgreen")
            self.button_new_rule.place(x = 5, y = 20)
            #for future use
            self.button_save_rule = ctk.CTkButton(master = self.frame_for_buttons,
                                                  text = "Save",
                                                  font = ("Consolas", 22),
                                                  fg_color= "green",
                                                  hover_color= "darkgreen",
                                                  command= self.pre_check_before_saving_the_rule)   
            #self.button_save_rule.place(x = 150, y = 20)
            
            self.entry_box_give_nikname = ctk.CTkEntry(master = self.frame_for_buttons,
                                                       font = ("Consolas", 22),
                                                       placeholder_text= "Give a nikname to your rule",
                                                       width = 400)
            #self.entry_box_give_nikname.place(x = 300, y = 20)
            
            ## for fun
            self.sleeping_panda = ctk.CTkImage(light_image=Image.open("sleeping_panda.png"),
                                dark_image=Image.open("sleeping_panda.png"),
                                size=(750, 730))
            
            ### functions to run at the start 
            self.display_rules()
            self.display_panda()
    
    def display_panda(self):
        self.label_sleeping_panda = ctk.CTkLabel(master = self, image= self.sleeping_panda, text="")
        self.label_sleeping_panda.place(x = 300, y = 73)
        self.label_text_panda = ctk.CTkLabel(master = self,
                                        text = "Wake up the sleeping bamboo-lover!",
                                        font = ("Consolas", 30, "bold"),
                                        fg_color = "transparent")
        self.label_text_panda.place(x = 350, y = 400)
        self.label_sleeping_panda.bind("<Button-1>", self.you_woke_him_up)
        
    def you_woke_him_up(self, event):
        if self.count_panda == 3:        
            he_woke_up = ctk.CTkImage(light_image=Image.open("he_woke_up.png"),
                                        dark_image=Image.open("he_woke_up.png"),
                                        size=(750, 730))
            self.label_sleeping_panda.configure(image=he_woke_up)
            self.label_text_panda.configure(text = "You woke him up!\nNow let's do some actual work :)",
                                            fg_color = "lightgreen",
                                            font = ("Consolas", 30, "bold"))
        else:
            self.count_panda += 1
    
    def pre_check_before_saving_the_rule(self):        
        if self.json_new_rule["action"] == None:
            messagebox.showerror("Error", "You must select an action for your rule")
        elif self.json_new_rule["action"] == "Move" and self.json_new_rule["where_to_move"] == None:
            messagebox.showerror("Error", "You must select a destination for your files")
        elif self.json_new_rule["action"] == "Copy" and self.json_new_rule["where_to_copy"] == None:
            messagebox.showerror("Error", "You must select a destination for your files")
        else:
            self.save_the_rule()
            
    def save_the_rule(self):
        top_level_window = ctk.CTkToplevel()
        top_level_window.geometry("1000x500")
        
        top_level_window_label = ctk.CTkLabel(master = top_level_window,
                                              text = "Are you sure you want to SAVE & RUN this rule?\n Once saved the rule will be executed, and it will continue to be executed till you delete it.\n\nInformation my be lost\n\nespecially if you selected the 'Delete' action",
                                              font= ("Consolas", 24, "bold"),
                                              text_color= "red",
                                              wraplength= 980)
        top_level_window_label.place(x = 10, y = 10)
        
        top_level_window_label_show_rules_info = ctk.CTkLabel(master = top_level_window,
                                                              text= f"Name of the rule: {self.entry_box_give_nikname.get() if self.entry_box_give_nikname.get() != "" else time.strftime("%Y-%m-%d %H:%M:%S")}\n\nTarget directory: {self.json_new_rule['target_directory']}\nAction: {self.json_new_rule['action']}\nWhere to move: {self.json_new_rule['where_to_move'] if self.json_new_rule['where_to_move'] != None else None}\nWhere to copy: {self.json_new_rule['where_to_copy'] if self.json_new_rule['where_to_copy'] != None else None}\nCriteria: {self.json_new_rule['criteria']}\nException: {self.json_new_rule['exception']}",
                                                                font= ("Consolas", 18),
                                                                wraplength= 980)
        top_level_window_label_show_rules_info.place(x = 200, y = 230)
        
        top_level_window_button_save = ctk.CTkButton(master = top_level_window,
                                                        text = "Save",
                                                        font = ("Consolas", 22),
                                                        fg_color= "green",
                                                        hover_color= "darkgreen",
                                                        command= self.new_rule_set_up) 
        top_level_window_button_save.place(x = 425, y = 450)
        
        top_level_window.focus_set()
        
    def new_rule_set_up(self):
        pass #TODO 
    
    def display_rules(self):
        try:
            with open("rules_for_files_and_folders.json", "r") as file:
                rules = json.load(file)
            if rules != {}:
                for rule in rules:
                    Rules(master = self.scrollable_frame_for_my_rules, nikname = rule, rule_id = rules[rule])  #TODO check if this works properly
            else:
                ctk.CTkLabel(master = self.scrollable_frame_for_my_rules, text = "No rules found", font = ("Consolas", 18)).pack()
        except:
            with open("rules_for_files_and_folders.json", "w") as file:
                json.dump({}, file)
            ctk.CTkLabel(master = self.scrollable_frame_for_my_rules, text = "Welcome!\nClick on 'New Rule'\nto start", font = ("Consolas", 18)).pack()
    
    def reset_vars_and_widgets(self):
        self.count_panda = 0
        self.cash_criteria_name = []
        self.cash_criteria_type = []
        self.cash_criteria_size = {}
        self.cash_exception_name = []
        self.cash_exception_type = []
        self.cash_exception_size = {}
        self.cash_criterias_selected = ""
        self.cash_exceptions_selected = ""
        
        for widget in self.winfo_children():
            if widget not in [self.frame_display_rules, self.frame_for_buttons]:
                widget.destroy()
    
    def create_new_rule(self):
        self.reset_vars_and_widgets()
        
        self.label_sleeping_panda.destroy()
        self.label_text_panda.destroy()
        
        self.button_save_rule.place(x = 150, y = 20)
        self.entry_box_give_nikname.place(x = 300, y = 20)
        
        self.current_directory = filedialog.askdirectory()
        
        self.json_new_rule = {
                "target_directory": self.current_directory,
                "action": None,
                "where_to_move": None,
                "where_to_copy": None,
                "criteria": {
                    "name": None,
                    "type": None,
                    "size": None,
                },
                "exception": {
                    "name": None,
                    "type": None,
                    "size": None,
            }
        }
        
        #self.current_directory
        self.label_text_display_text = ctk.CTkLabel(master = self,
                                                    text = self.current_directory,
                                                    wraplength= 750,
                                                    font = ("Consolas", 18))
        self.label_text_display_text.place(x = 310, y = 80)
        ### action 
        self.label_text_display_text_action = ctk.CTkLabel(master = self,
                                                        text = "Select the action for your rule:",
                                                        font = ("Consolas", 18, "bold"))
        self.label_text_display_text_action.place(x = 310, y = 140)
        
        self.option_menu_action = ctk.CTkOptionMenu(master = self,
                                                    values= ["Move", "Copy", "Delete"],
                                                    font= ("Consolas", 22),
                                                    command= self.func_action,
                                                    width= 150) 
        self.option_menu_action.place(x = 310, y = 170)
        
        
        ### criterias
        self.label_show_text_criteria = ctk.CTkLabel(master = self,
                                                    text = "Criterias",
                                                    font = ("Consolas", 24, "bold"),
                                                    text_color= "darkgreen")
        self.label_show_text_criteria.place(x = 310, y = 320)
        
        self.option_menu_criteria = ctk.CTkOptionMenu(master = self,
                                                      values = ["Name", "Type", "Size"],
                                                      command= self.func_criteria,
                                                      font= ("Consolas", 22),
                                                        width= 150)
        self.option_menu_criteria.place(x = 310, y = 350)
        self.option_menu_criteria.set("Name")
        
        self.label_show_crierias_selected = ctk.CTkLabel(master = self,
                                                        text = f"Criterias selected:\nKey-word(s): {self.cash_criteria_name if self.cash_criteria_name != [] else None}\nType: {self.cash_criteria_type if self.cash_criteria_type != [] else None}\nSize: {self.cash_criteria_size if self.cash_criteria_size != {} else None}",
                                                        font = ("Consolas", 18))
        self.label_show_crierias_selected.place(x = 310, y = 380)   
        
        ### exceptions
        self.label_show_text_exception = ctk.CTkLabel(master = self,
                                                        text = "Exceptions",
                                                        font = ("Consolas", 24, "bold"),
                                                        text_color= "darkgreen")
        self.label_show_text_exception.place(x = 310, y = 550)
        
        self.option_menu_exception = ctk.CTkOptionMenu(master = self,
                                                      values = ["Name", "Type", "Size"],
                                                      command= self.func_exception,
                                                      font= ("Consolas", 22),
                                                        width= 150)
        self.option_menu_exception.place(x = 310, y = 585)
        self.option_menu_exception.set("Name")
        
    def func_exception(self, choice):
        try:
            self.entry_exception_name.destroy()
        except:
            pass
        try:
            self.entry_exception_type.destroy()
        except:
            pass
        try:
            self.option_menu_exception_size.destroy()
        except:
            pass
        
        if choice == "Name":
            self.entry_exception_name = ctk.CTkEntry(master = self,
                                                    font = ("Consolas", 20),
                                                    placeholder_text= "Enter key-word(s)",
                                                    width = 400)
            self.entry_exception_name.place(x = 480, y = 585)
            self.entry_exception_name.bind("<Return>", lambda event: self.func_exceptions_name_or_type_updated(event= event, choice= "Name"))
        elif choice == "Type":
            self.entry_exception_type = ctk.CTkEntry(master = self,
                                                    font = ("Consolas", 22),
                                                    placeholder_text= "Type",
                                                    width = 400)
            self.entry_exception_type.place(x = 480, y = 585)
            self.entry_exception_type.bind("<Return>", lambda event: self.func_exceptions_name_or_type_updated(event= event, choice= "Type"))
        elif choice == "Size":
            self.option_menu_exception_size = ctk.CTkOptionMenu(master = self,
                                                               values = ["Above", "Below"],
                                                               font= ("Consolas", 22),
                                                               width= 150)
            self.option_menu_exception_size.place(x = 480, y = 585)
            self.option_menu_exception_size.set("Above")
            self.entry_exception_size = ctk.CTkEntry(master = self, font = ("Consolas", 20), placeholder_text= "Type number", width = 150)
            self.entry_exception_size.place(x = 640, y = 585)
            self.entry_exception_size.bind("<Return>", self.func_exception_size)
            # entry_exception_size can only accept numbers
            self.entry_exception_size.bind("<Key>", self.only_numbers)
            self.option_menu_exception_size_measurment = ctk.CTkOptionMenu(master = self,
                                                                        values = ["Byte(s)", "Kilobyte(s)", "Megabyte(s)", "Gigabyte(s)", "Terabyte(s)"],
                                                                        font= ("Consolas", 20),
                                                                        width= 150)
            self.option_menu_exception_size_measurment.place(x = 800, y = 585)
            self.option_menu_exception_size_measurment.set("Megabytes")
            
        self.label_show_exceptions_selected = ctk.CTkLabel(master = self,
                                                    text = f"Exceptions selected:\nKey-word(s): {self.cash_exception_name if self.cash_exception_name != [] else None}\nType: {self.cash_exception_type if self.cash_exception_type != [] else None}\nSize: {self.cash_exception_size if self.cash_exception_size != {} else None}",
                                                    font = ("Consolas", 18))
        self.label_show_exceptions_selected.place(x = 310, y = 620)
            
    def func_exception_size(self, event):
        if self.entry_exception_size.get() == "":
            messagebox.showerror("Hey", "You must enter a number, then press enter.")
        else:
            self.json_new_rule["exception"]["size"] = {"above_or_below": "above",
                                                "size": 0,
                                                "measure": ""}
            
            self.json_new_rule["exception"]["size"]["above_or_below"] = self.option_menu_exception_size.get().lower()
            self.json_new_rule["exception"]["size"]["size"] = int(self.entry_exception_size.get())
            self.json_new_rule["exception"]["size"]["measure"] = self.option_menu_exception_size_measurment.get()
            
            self.update_label_show_exceptions_selected()
            
    def func_exceptions_name_or_type_updated(self, event, choice): # add the widget to the try distroy
        if choice == "Name":
            if self.entry_exception_name.get() == "":
                messagebox.showerror("Error", "You must enter a key-word")
            elif self.entry_exception_name.get() in self.cash_exception_name:
                messagebox.showerror("Error", "You can't enter the same key-word twice")
            else:
                self.cash_exception_name.append(self.entry_exception_name.get())
            #reset the entry box
            self.entry_exception_name.delete(0, "end")
            self.update_label_show_exceptions_selected()
        elif choice == "Type":
            if self.entry_exception_type.get() == "":
                messagebox.showerror("Error", "You must enter a type of file, expample: dir (folder), .png, .html, .txt etc.")
            elif self.entry_exception_type.get() in self.cash_exception_type:
                messagebox.showerror("Error", "You can't enter the same type of file twice")
            else:
                self.cash_exception_type.append(self.entry_exception_type.get())
            #reset the entry box
            self.entry_exception_type.delete(0, "end")
            self.update_label_show_exceptions_selected()

    def update_label_show_exceptions_selected(self):
        self.label_show_exceptions_selected.configure(text= f"Exceptions selected:\nKey-word(s): {self.cash_exception_name if self.cash_exception_name != [] else None}\nType: {self.cash_exception_type if self.cash_exception_type != [] else None}\nSize: { self.json_new_rule["exception"]["size"]["above_or_below"] + " " + str(self.json_new_rule["exception"]["size"]["size"]) + " " + self.json_new_rule["exception"]["size"]["measure"] if self.json_new_rule["exception"]["size"] != None else None}")
        
    def func_criteria(self, choice):
        try:
            self.entry_criteria_name.destroy()
        except:
            pass
        try:
            self.entry_criteria_type.destroy()
        except:
            pass
        try:
            self.option_menu_criteria_size.destroy()
        except:
            pass
        
        if choice == "Name":
            self.entry_criteria_name = ctk.CTkEntry(master = self,
                                                    font = ("Consolas", 20),
                                                    placeholder_text= "Enter key-word(s)",
                                                    width = 400)
            self.entry_criteria_name.place(x = 480, y = 350)
            self.entry_criteria_name.bind("<Return>", lambda event: self.func_criterias_name_or_type_updated(event= event, choice= "Name"))
        elif choice == "Type":
            self.entry_criteria_type = ctk.CTkEntry(master = self,
                                                    font = ("Consolas", 22),
                                                    placeholder_text= "Type",
                                                    width = 400)
            self.entry_criteria_type.place(x = 480, y = 350)
            self.entry_criteria_type.bind("<Return>", lambda event: self.func_criterias_name_or_type_updated(event= event, choice= "Type"))
        elif choice == "Size":
            self.option_menu_criteria_size = ctk.CTkOptionMenu(master = self,
                                                               values = ["Above", "Below"],
                                                               font= ("Consolas", 22),
                                                               width= 150)
            self.option_menu_criteria_size.place(x = 480, y = 350)
            self.option_menu_criteria_size.set("Above")
            self.entry_criteria_size = ctk.CTkEntry(master = self, font = ("Consolas", 20), placeholder_text= "Type number", width = 150)
            self.entry_criteria_size.place(x = 640, y = 350)
            self.entry_criteria_size.bind("<Return>", self.func_criteria_size)
            # entry_criteria_size can only accept numbers
            self.entry_criteria_size.bind("<Key>", self.only_numbers)
            self.option_menu_criteria_size_measurment = ctk.CTkOptionMenu(master = self,
                                                                        values = ["Byte(s)", "Kilobyte(s)", "Megabyte(s)", "Gigabyte(s)", "Terabyte(s)"],
                                                                        font= ("Consolas", 20),
                                                                        width= 150)
            self.option_menu_criteria_size_measurment.place(x = 800, y = 350)
            self.option_menu_criteria_size_measurment.set("Megabytes")
            
    def only_numbers(self, event):
        if event.char not in "1234567890":
            return "break"
            
    def func_criteria_size(self, event):
        if self.entry_criteria_size.get() == "":
            messagebox.showerror("Hey", "You must enter a number, then press enter.")
        else:
            self.json_new_rule["criteria"]["size"] = {"above_or_below": "above",
                                                "size": 0,
                                                "measure": ""}
            
            self.json_new_rule["criteria"]["size"]["above_or_below"] = self.option_menu_criteria_size.get().lower()
            self.json_new_rule["criteria"]["size"]["size"] = int(self.entry_criteria_size.get())
            self.json_new_rule["criteria"]["size"]["measure"] = self.option_menu_criteria_size_measurment.get()
            
            self.update_label_show_crierias_selected()
            

    def update_label_show_crierias_selected(self):
        self.label_show_crierias_selected.configure(text= f"Criterias selected:\nKey-word(s): {self.cash_criteria_name if self.cash_criteria_name != [] else None}\nType: {self.cash_criteria_type if self.cash_criteria_type != [] else None}\nSize: { self.json_new_rule["criteria"]["size"]["above_or_below"] + " " + str(self.json_new_rule["criteria"]["size"]["size"]) + " " + self.json_new_rule["criteria"]["size"]["measure"] if self.json_new_rule["criteria"]["size"] != None else None}")
    
    def func_criterias_name_or_type_updated(self, event, choice): # add the widget to the try distroy 
        if choice == "Name":
            if self.entry_criteria_name.get() == "":
                messagebox.showerror("Error", "You must enter a key-word")
            elif self.entry_criteria_name.get() in self.cash_criteria_name:
                messagebox.showerror("Error", "You can't enter the same key-word twice")
            else:
                self.cash_criteria_name.append(self.entry_criteria_name.get())
            #reset the entry box
            self.entry_criteria_name.delete(0, "end")
            self.update_label_show_crierias_selected()
        elif choice == "Type":
            if self.entry_criteria_type.get() == "":
                messagebox.showerror("Error", "You must enter a type of file, expample: dir (folder), .png, .html, .txt etc.")
            elif self.entry_criteria_type.get() in self.cash_criteria_type:
                messagebox.showerror("Error", "You can't enter the same type of file twice")
            else:
                self.cash_criteria_type.append(self.entry_criteria_type.get())
            #reset the entry box
            self.entry_criteria_type.delete(0, "end")
            self.update_label_show_crierias_selected()
    
    def func_action(self, choice):
        self.json_new_rule["action"] = choice
        
        if choice == "Delete":
            pass
        elif choice == "Move":
            self.button_where_to_move = ctk.CTkButton(master = self,
                                                        text = "Where?",
                                                        font = ("Consolas", 22),
                                                        command = self.func_where_to_move,
                                                        fg_color= "green",
                                                        hover_color= "darkgreen")
            self.button_where_to_move.place(x = 310, y = 210)
        elif choice == "Copy":
            self.button_where_to_copy = ctk.CTkButton(master = self,
                                                        text = "Where?",
                                                        font = ("Consolas", 22),
                                                        command = self.func_where_to_copy,
                                                        fg_color= "green",
                                                        hover_color= "darkgreen")
            self.button_where_to_copy.place(x = 310, y = 210)
    
    def func_where_to_move(self):
        cash = filedialog.askdirectory()
        if cash == self.current_directory:
            messagebox.showerror("Error", "You can't move the files to the same directory")
        else:
            self.func_2_where_to_move(cash)
            
    def func_2_where_to_move(self, cash):
        self.json_new_rule["where_to_move"] = cash
        self.label_show_where_the_file_will_be_moved = ctk.CTkLabel(master = self,
                                                                    text = f"Move to: {cash}",
                                                                    text_color= "green",
                                                                    font = ("Consolas", 18),
                                                                    wraplength= 600)
        self.label_show_where_the_file_will_be_moved.place(x = 460, y = 210)
    
    def func_where_to_copy(self):
        cash = filedialog.askdirectory()
        if cash == self.current_directory:
            messagebox.showerror("Error", "You can't copy the files to the same directory")
        else:
            self.func_2_where_to_copy(cash)
    
    def func_2_where_to_copy(self, cash):
        self.json_new_rule["where_to_copy"] = filedialog.askdirectory()
        self.label_show_where_the_file_will_be_copied = ctk.CTkLabel(master = self,
                                                                    text = f"Copy to: {self.json_new_rule["where_to_copy"]}",
                                                                    text_color= "green",
                                                                    font = ("Consolas", 18),
                                                                    wraplength= 600)
        self.label_show_where_the_file_will_be_copied.place(x = 460, y = 210)
    
class Rules(ctk.CTk):    
    def __init__(self, *args, nikname, rule_id, **kwargs):
            super().__init__(*args, nikname, rule_id, **kwargs)
            self.nikname = nikname
            self.rule_id = rule_id
            self.frame_rule = ctk.CTkFrame(master = self)
            self.frame_rule.pack(side = "top", fill = "x")
            self.title = ctk.CTkLabel(master = self.frame_rule, text = self.nikname if self.nikname != None else "My Rule", font = ("Consolas", 18), wraplength= 250)
            self.title.pack(side = "left", fill = "x")
            self.delte_rule = ctk.CTkButton(master = self.frame_rule, text = "Del.", font = ("Consolas", 18), command = self.delete_rule)
            self.delte_rule.pack(side = "right", fill = "x")
            
    def delete_rule(self):
        with open("rules_for_files_and_folders.json", "r") as file:
            rules = json.load(file)
        del rules[self.nikname]
        with open("rules_for_files_and_folders.json", "w") as file:
            json.dump(rules, file)
        self.destroy()
        

if __name__ == "__main__":
    app = GUI_Rules_for_files_and_folders()
    app.mainloop()
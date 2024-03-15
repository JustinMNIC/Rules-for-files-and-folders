import shutil
import os
import customtkinter as ctk
import json
from tkinter import filedialog, messagebox 
from PIL import Image
import time 


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
            self.start()
            
    def start(self):
        Executor.start(Executor)
        if Executor.running == False:
            self.after(30000, self.start)
    
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
        with open("rules_for_files_and_folders.json", "r") as file:
            data_json = json.load(file)
            
        if self.json_new_rule["action"] == None:
            messagebox.showerror("Error", "You must select an action for your rule")
        elif self.json_new_rule["action"] == "Move" and self.json_new_rule["where_to_move"] == None:
            messagebox.showerror("Error", "You must select a destination for your files")
        elif self.json_new_rule["action"] == "Copy" and self.json_new_rule["where_to_copy"] == None:
            messagebox.showerror("Error", "You must select a destination for your files")
        elif self.entry_box_give_nikname.get() in data_json.keys():
            messagebox.showerror("Error", "You already have a rule with that name\n\nPlease select another name for your rule")
        else:
            self.func_create_top_level_and_ask_for_confirmation_to_save_the_rule()
            
    def func_create_top_level_and_ask_for_confirmation_to_save_the_rule(self):
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
                                                        command= self.func_finally_save_the_rule) 
        top_level_window_button_save.place(x = 425, y = 450)
        
        top_level_window.focus_set()
        
    def func_finally_save_the_rule(self):
        #save the rule to the json file 
        
        with open("rules_for_files_and_folders.json", "r") as file:
            data_json = json.load(file)
            
        new_rule = {}
        new_rule[self.entry_box_give_nikname.get() if self.entry_box_give_nikname.get() != "" else time.strftime("%Y-%m-%d %H:%M:%S")] = self.json_new_rule
        
        data_json.update(new_rule)
        
        with open("rules_for_files_and_folders.json", "w") as file:
            json.dump(data_json, file, indent= 4)
         
        self.reset_vars_and_widgets()
        self.display_rules()
        
    
    def display_rules(self):
        if not os.path.exists("rules_for_files_and_folders.json"):
            with open("rules_for_files_and_folders.json", "w") as file:
                json.dump({}, file)
            ctk.CTkLabel(master = self.scrollable_frame_for_my_rules, text = "Welcome!\nClick on 'New Rule'\nto start", font = ("Consolas", 18)).pack()
        elif os.path.exists("rules_for_files_and_folders.json"):
            #if the json file is empty ({}) then display "No rules found"
            with open("rules_for_files_and_folders.json", "r") as file:
                rules = json.load(file)
            if rules == {}:
                ctk.CTkLabel(master = self.scrollable_frame_for_my_rules, text = "No rules found", font = ("Consolas", 18)).pack()
            else:
                for widget in self.scrollable_frame_for_my_rules.winfo_children():
                    widget.destroy()
                for rule_name, rule_details in rules.items():
                    self.rule = ctk.CTkFrame(master = self.scrollable_frame_for_my_rules, width = 300, height = 50, border_width = 1)
                    self.rule.pack(side = "top", fill = "x")
                    self.rule_name = ctk.CTkLabel(master = self.rule, text = rule_name, font = ("Consolas", 18, "bold"), text_color= "lightblue")
                    self.rule_name.pack(side = "left")
                    self.button_delete_rule = ctk.CTkButton(master = self.rule,
                                                       text = "Delete",
                                                       font = ("Consolas", 18),
                                                       hover_color= "darkred",
                                                       command = lambda: self.rule_deleted(rule_name))
                    self.button_delete_rule.pack(side = "right")
    
    def rule_deleted(self, rule_name):
        #remove rule_name from the json file
        with open("rules_for_files_and_folders.json", "r") as file:
            data_json = json.load(file)
        data_json.pop(rule_name)
        with open("rules_for_files_and_folders.json", "w") as file:
            json.dump(data_json, file, indent= 4)

        #remove all rules from the scrollable_frame_for_my_rules
        for widget in self.scrollable_frame_for_my_rules.winfo_children():
            widget.destroy()
            
        self.display_rules()
        
    def reset_vars_and_widgets(self):
        self.current_directory = ""
        self.count_panda = 0
        
        self.cash_criteria_name = []
        self.cash_criteria_type = []
        self.cash_criteria_size = {}
        
        self.cash_exception_name = []
        self.cash_exception_type = []
        self.cash_exception_size = {}
        
        self.cash_criterias_selected = ""
        self.cash_exceptions_selected = ""
        
        self.button_save_rule.place_forget()
        self.entry_box_give_nikname.place_forget()
        
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
                                                      values = ["No criteria", "Name", "Type", "Size"],
                                                      command= self.func_criteria,
                                                      font= ("Consolas", 22),
                                                        width= 150)
        self.option_menu_criteria.place(x = 310, y = 350)
        self.option_menu_criteria.set("No criteria")
        
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
                                                      values = ["No exceptions", "Name", "Type", "Size"],
                                                      command= self.func_exception,
                                                      font= ("Consolas", 22),
                                                        width= 150)
        self.option_menu_exception.place(x = 310, y = 585)
        self.option_menu_exception.set("No exceptions")
        
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
            try:
                self.label_show_where_the_file_will_be_moved.destroy()
                self.button_where_to_move.destroy()
            except:
                pass
            try:
                self.button_where_to_copy.destroy()
                self.label_show_where_the_file_will_be_copied.destroy()
            except:
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
    
    def path_doesnt_exist(self, rule_name, path):
        messagebox.showerror("Error", f"The path: {path} doesn't exist\n\nPlease update the path for the rule: {rule_name}")
        #chanege the name of the rule to Error: Path
        with open("rules_for_files_and_folders.json", "r") as file:
            data_json = json.load(file)
        data_json["Error: Path"] = data_json.pop(rule_name)
        with open("rules_for_files_and_folders.json", "w") as file:
            json.dump(data_json, file, indent= 4)
        self.display_rules()
        
        
class Executor():
    running = False
    def start(self):
        self.running = True
        
        with open("rules_for_files_and_folders.json", "r") as file:
            data_json = json.load(file)
            
        for name, data in data_json.items():
            
            self.check_if_path_still_exists(self, data["target_directory"], name)
            
            if data["action"] == "Move":
                self.check_if_path_still_exists(self, data["where_to_move"], name)
                self.move_files(self = self, data = data)
            elif data["action"] == "Copy":
                self.check_if_path_still_exists(self, data["where_to_copy"], name)
                self.copy_files(self = self, data = data)
            elif data["action"] == "Delete":
                self.delete_files(self, data)
            
        self.running = False
              
    def move_files(self, data):
        for root, dirs, files in os.walk(data["target_directory"]):
            for file in files:
                if self.check_criteria(self, data, file) and self.check_exceptions(self, data, file):
                    shutil.move(os.path.join(root, file), data["where_to_move"])
            for dir in dirs:
                if self.check_criteria(self, data, dir) and self.check_exceptions(self, data, dir):
                    shutil.move(os.path.join(root, dir), data["where_to_move"])
                    
    def copy_files(self, data):
        for root, dirs, files in os.walk(data["target_directory"]):
            for file in files:
                if self.check_criteria(self, data, file) and self.check_exceptions(self, data, file):
                    shutil.copy(os.path.join(root, file), data["where_to_copy"])
            for dir in dirs:
                if self.check_criteria(self, data, dir) and self.check_exceptions(self, data, dir):
                    shutil.copy(os.path.join(root, dir), data["where_to_copy"])
                    
    def delete_files(self, data):
        for root, dirs, files in os.walk(data["target_directory"]):
            for file in files:
                if self.check_criteria(self, data, file) and self.check_exceptions(self, data, file):
                    os.remove(os.path.join(root, file))
            for dir in dirs:
                if self.check_criteria(self, data, dir) and self.check_exceptions(self, data, dir):
                    shutil.rmtree(os.path.join(root, dir))
    
    def check_criteria(self, data, file):
        if "." in file:
            cash = file.split(".")
            file_name, file_type = cash[0], cash[1]
        else:
            file_name, file_type = file, "folder"
        
        C_size = False
        C_name = False
        C_type = False
        
        #criteria name
        if data["criteria"]["name"] != None:
            for name in data["criteria"]["name"]:
                if name in file_name:
                    C_name = True
        else:
            C_name = True
        
        #criteria type
        if data["criteria"]["type"] != None:
            for variants in ["dir", "folder", "directory"]:
                if variants in data["criteria"]["type"]:
                    if os.path.isdir(file):
                        C_type = True
            for typee in data["criteria"]["type"]:
                if typee in file_type:
                    C_type = True
        else:
            C_type = True
        
        #criteria size
        if data["criteria"]["size"] != None:
            if data["criteria"]["size"]["above_or_below"] == "above":
                if os.path.getsize(file) > data["criteria"]["size"]["size"]:
                    C_size = True
                else:
                    C_size = False
            elif data["criteria"]["size"]["above_or_below"] == "below":
                if os.path.getsize(file) < data["criteria"]["size"]["size"]:
                    C_size = True
                else:
                    C_size = False
        else:
            C_size = True
        return True if C_name and C_type and C_size else False
    
    def check_exceptions(self, data, file):
        if "." in file:
            cash = file.split(".")
            file_name, file_type = cash[0], cash[1]
        else:
            file_name, file_type = file, "folder"
        
        E_size = False
        E_name = False
        E_type = False
        
        if data["exception"]["name"] != None:
            for name in data["exception"]["name"]:
                if name in file_name:
                    E_name = True
        else:
            E_name = True
            
        if data["exception"]["type"] != None:
            for variants in ["dir", "folder", "directory"]:
                if variants in data["exception"]["type"]:
                    if os.path.isdir(file):
                        E_type = True
            for typee in data["exception"]["type"]:
                if typee in file_type:
                    E_type = True
        else:
            E_type = True
            
        if data["exception"]["size"] != None:
            if data["exception"]["size"]["above_or_below"] == "above":
                if os.path.getsize(file) > data["exception"]["size"]["size"]:
                    E_size = True
                else:
                    E_size = False
            elif data["exception"]["size"]["above_or_below"] == "below":
                if os.path.getsize(file) < data["exception"]["size"]["size"]:
                    E_size = True
                else:
                    E_size = False
        else:
            E_size = True
        return False if E_name and E_type and E_size else True
    
    def check_if_path_still_exists(self, path, rule_name):
        if os.path.exists(path):
            return True
        else:
            GUI_Rules_for_files_and_folders.path_doesnt_exist(path, rule_name)
            
if __name__ == "__main__":
    app = GUI_Rules_for_files_and_folders()
    app.mainloop()
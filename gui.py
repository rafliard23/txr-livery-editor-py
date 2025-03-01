import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from customtkinter import filedialog
import json
import os
import subprocess

version = "v1.0 RC2"
main_author = "rafli.ard23"
        
class control_frame(ctk.CTkFrame):
    first_run = True

    def __init__(self, master, car_list_section, **kwargs):
        super().__init__(master, **kwargs)
        self.car_list_section = car_list_section

        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_rowconfigure(8, weight=1)

        self._default_tmp_path = "./bin/temp/tmp.json"
        
        # Save File IO Function
        self.button_open = ctk.CTkButton(self, text="Open", width=100,command=self.button_open_filedialog_callback)
        self.button_open.grid(row=0, column=0, padx=20, pady=(40, 20), sticky="ew")
        self.button_auto = ctk.CTkButton(self, text="Autoload", width=100, command=self.button_autoload_callback)
        self.button_auto.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.button_save = ctk.CTkButton(self, text="Save", width=100, command=self.button_save_callback)
        self.button_save.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.separator = ttk.Separator(self, orient='horizontal').grid(row=3, columnspan=3)

        # Livery IO Function
        self.button_backup = ctk.CTkButton(self, text="Backup", width=100, command=self.button_backup_filedialog_callback)
        self.button_backup.grid(row=4, column=0, padx=20, pady=(20, 20), sticky="ew")
        self.button_restore = ctk.CTkButton(self, text="Restore", width=100, command=self.button_restore_filedialog_callback)
        self.button_restore.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Show Version and Author
        self.ver_info = ctk.CTkLabel(self, text=version)
        self.ver_info.grid(row=8, column=0, padx=20, pady=(0, 5), sticky="ews")
        self.author_info = ctk.CTkLabel(self, text=f"by: {main_author}")
        self.author_info.grid(row=9, column=0, padx=20, pady=(0, 20), sticky="ews")

    @property
    def default_tmp_path(self):
        """Getter for the temporary file path"""
        return self._default_tmp_path

    @default_tmp_path.setter
    def default_tmp_path(self, path):
        """Setter for the temporary file path"""
        self._default_tmp_path = path

    def init_last_selected(self, last_selected, last_name):
        self.label_action = ctk.CTkLabel(self, text="Last selected:")
        self.label_action.grid(row=6, column=0, padx=20, pady=(20, 0), sticky="new")
        self.last_selected_text = tk.StringVar()
        self.last_selected_text.set(f"#{last_selected} {last_name}")
        self.button_action = ctk.CTkButton(self, textvariable=self.last_selected_text,
                                           width=100, state="disabled",
                                           text_color_disabled="white")
        self.button_action.grid(row=7, column=0, padx=20, pady=(10, 20), sticky="new")
        self.first_run = False

    def show_last_selected(self, last_selected, last_name):
        # Show status and its indicator
        if (self.first_run == True):
            self.init_last_selected(last_selected, last_name)
        else:
            self.last_selected_text = tk.StringVar()
            self.last_selected_text.set(f"#{last_selected} {last_name}")
            self.button_action.configure(textvariable=self.last_selected_text)
        
    def open_default_sav(self):
        default_save_path = os.environ['LOCALAPPDATA']
        default_save_path = os.path.join(default_save_path, 'TokyoXtremeRacer\Saved\SaveGames')
        
        steam_id = [item for item in os.listdir(default_save_path) if os.path.isdir(os.path.join(default_save_path, item))]
        
        if not steam_id:
            print("No save directory found!")
            return None
        
        default_save_path = os.path.join(default_save_path, steam_id[0], 'UserData_00.sav').replace("\\","/")
        return default_save_path
    
    def sav_to_json(self, path):
        if path:
            subprocess.run(['./bin/uesave', 'to-json', '-i', f'{path}', '-o', f'{self.default_tmp_path}'])
            
    def json_to_sav(self, path):
        if path:
            subprocess.run([f'./bin/uesave', 'from-json', '-i', f'{self.default_tmp_path}', '-o', f'{path}'])

    def restore_stickers(self):
        target_id = self.car_list_section.get_last_selected()

        data = self.default_tmp_path
        if not os.path.exists(data):
            print("Error: JSON file not found!")
            return
        
        with open(data, "r", encoding="utf-8") as buffer_data:
            data = json.load(buffer_data)

        stickers = filedialog.askopenfilename(filetypes=[('Livery Files', '*.livery'),
                                                             ('All Files', '*.*')]).replace("\\","/")
        
        with open(stickers, "r", encoding="utf-8") as stickers_data:
            stickers = json.load(stickers_data)
        

        cars = data["root"]["properties"]["user_info_0"]["Struct"]["Struct"]["MyCars_0"]["Map"]

        target_car = next((car for car in cars if car["key"]["Int"] == target_id), None)

        if target_car:
            target_car["value"]["Struct"]["Struct"]["BodyStickers_0"] = stickers["BodyStickers_0"]
            target_car["value"]["Struct"]["Struct"]["RearWingStickers_0"] = stickers["RearWingStickers_0"]

            with open(self.default_tmp_path, "w", encoding="utf-8") as buffer_data:
                json.dump(data, buffer_data, indent=2, separators=(",",":"))
        

    def dumping_stickers(self):
        target_id = self.car_list_section.get_last_selected()
        target_name = self.car_list_section.get_last_name()

        data = self.default_tmp_path
        if not os.path.exists(data):
            print("Error: JSON file not found!")
            return
        
        with open(data,"r") as file:
            data = json.load(file)

        cars = data["root"]["properties"]["user_info_0"]["Struct"]["Struct"]["MyCars_0"]["Map"]

        target_car = next((car for car in cars if car["key"]["Int"] == target_id), None)

        if target_car:
            vehicle_livery = {
                "BodyStickers_0": target_car["value"]["Struct"]["Struct"]["BodyStickers_0"],
                "RearWingStickers_0": target_car["value"]["Struct"]["Struct"]["RearWingStickers_0"]
            }

            save_path = filedialog.asksaveasfilename(filetypes=[('Livery Files', '*.livery'),
                                                    ('All Files', '*.*')],
                                                    defaultextension='.livery',
                                                    confirmoverwrite=True,
                                                    initialfile=f"{target_name}_Untitled.livery")

            with open(save_path, "w", encoding="utf-8") as buffer_data:
                json.dump(vehicle_livery, buffer_data, ensure_ascii=False)

    def button_open_filedialog_callback(self):
        default_save_path = os.environ['LOCALAPPDATA']
        default_save_path = os.path.join(default_save_path, 'TokyoXtremeRacer').replace("\\","/")

        path = filedialog.askopenfilename(filetypes=[('UE5 Save File', '*.sav'),
                                                    ('All Files', '*.*')],
                                                    initialdir=default_save_path).replace("\\","/")
        if path:
            self.sav_to_json(path)
            self.car_list_section.update_car_list()
        self.master.title(f"Tokyo Xtreme Racer - Livery Tool | {path}")

    def button_save_callback(self):
        default_save_path = os.environ['LOCALAPPDATA']
        default_save_path = os.path.join(default_save_path, 'TokyoXtremeRacer').replace("\\","/")
        
        path = filedialog.asksaveasfilename(filetypes=[('UE5 Save File', '*.sav'),
                                                    ('All Files', '*.*')],
                                                    defaultextension='.sav',
                                                    initialdir=default_save_path,
                                                    confirmoverwrite=True,
                                                    initialfile=f"UserData_00.sav")
        if path:
            self.json_to_sav(path)

    def button_autoload_callback(self):
        path = self.open_default_sav()
        self.sav_to_json(path)
        self.car_list_section.update_car_list()
        self.master.title(f"Tokyo Xtreme Racer - Livery Tool | {path}")

    def button_restore_filedialog_callback(self):
        self.restore_stickers()

    def button_backup_filedialog_callback(self):
        self.dumping_stickers()

    def button_callback(self):
        print("button pressed")


class car_list_frame(ctk.CTkScrollableFrame):
    def __init__(self, master, control_section, **kwargs):
        super().__init__(master, **kwargs)
        self.control_section = control_section  # Store reference to control_frame
        # self.list_car()
        
    def update_car_list(self):
        """Refresh the car list when a new save file is loaded."""
        for widget in self.winfo_children():
            widget.destroy()  # Clear old buttons

        # Reload data
        data = self.control_section.default_tmp_path # Get path from control_frame
        if not os.path.exists(data):
            print("Error: JSON file not found!")
            return
        
        with open(data,"r") as file:
            data = json.load(file)

        # Navigate to MyCars_0
        my_cars = (
            data.get("root", {})
            .get("properties", {})
            .get("user_info_0", {})
            .get("Struct", {})
            .get("Struct", {})
            .get("MyCars_0", {})
            .get("Map", [])
        )
        # Extract all CarNameId_0 values
        self.car_names = [
            self.car["value"]["Struct"]["Struct"]["CarNameId_0"]["Name"]
            for self.car in my_cars
            if "CarNameId_0" in self.car["value"]["Struct"]["Struct"]
        ]

        self.car_id = [
            self.car["key"]["Int"]
            for self.car in my_cars
            if "Int" in self.car["key"]
        ]

        for labels, button_id in zip(self.car_names, self.car_id):
            stats = ctk.CTkButton(self, text=f"#{button_id} {labels}", width=240, font=ctk.CTkFont("Arial", 16),
                                  command=lambda c=button_id, n=labels: self.button_callback(c, n))
            stats.pack(pady=5)

    
    def button_callback(self, car_id, car_names):
        """Function that gets called when a button is clicked"""
        self.last_selected = car_id  # Store the last clicked button
        self.last_name = car_names
        self.control_section.show_last_selected(self.last_selected, self.last_name)
        # print(f"Selected: {self.last_selected}, {self.last_name}")

    def get_last_selected(self):
        """Retrieve the last clicked button value"""
        return self.last_selected
    
    def get_last_name(self):
        """Retrieve the last clicked button value"""
        return self.last_name

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window attributes
        self.title("Tokyo Xtreme Racer - Livery Tool")
        self.iconbitmap('./app.ico')
        self.geometry(f"{520}x{560}")

        # Adjust rows and columns
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.car_list_section = car_list_frame(self, None)

        self.control_section = control_frame(self, self.car_list_section, width=160)
        self.control_section.grid(row=0, rowspan=3, column=0, sticky="ns")

        self.car_list_section.control_section = self.control_section
        self.car_list_section.grid(row=0, rowspan=3, column=1, padx = 20, pady = 20, sticky="nsew")

app = App()
app.mainloop()
from tkinter import filedialog
import requests
import json
import customtkinter as ctk
import os
import threading as thr
import configparser
import glob

APP_PATH: str = os.path.dirname(os.path.realpath(__file__))
THEME_PATH: str = os.path.join(APP_PATH, "theme/")

settings = configparser.ConfigParser()
settings_file_path = "settings.ini"


def set_settings():
    try:
        if os.path.exists(settings_file_path):
            settings.read(settings_file_path)

            theme = settings["Settings"].get("theme")
            appearance = settings["Settings"].get("appearance")

            try:
                ctk.set_default_color_theme(THEME_PATH + f"{theme}")

            except Exception as e:
                print(f"Error while reading theme: {e}")
                ctk.set_default_color_theme(THEME_PATH + "default.json")
                settings["Settings"]["theme"] = "default.json"

                with open(settings_file_path, "w") as cf:
                    settings.write(cf)

            try:
                ctk.set_appearance_mode(str(appearance))

            except Exception as e:
                print(f"Error while reading appearance mode: {e}")
                ctk.set_appearance_mode("light")
                settings["Settings"]["appearance"] = "light"

                with open(settings_file_path, "w") as cf:
                    settings.write(cf)

        else:
            ctk.set_default_color_theme(THEME_PATH + "default.json")
            ctk.set_appearance_mode("light")
            settings["Settings"] = {
                "theme": "default.json",
                "host": "http://localhost:11434",
                "appearance": "light"
            }

            with open(settings_file_path, "w") as cf:
                settings.write(cf)

    except Exception as e:
        print(f"Error settings.ini: {e}")

set_settings()

theme = settings["Settings"].get("theme")
appearance = settings["Settings"].get("appearance")
host = settings["Settings"].get("host")

error_log = []
model_list = []
themes_files = []

class GPLLicense(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("GPL License")
        self.geometry("500x300")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.label = ctk.CTkLabel(self, text="""
Copyright (c) 2025 by Kamil Wiśniewski <tomteipl@gmail.com>

This program lets you talk with AI models using the Ollama API.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses/gpl-3.0.en.html>
        """,)
        self.label.grid(row=0, column=0, sticky="nsew", padx=10)

class ErrorWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Error logs")
        self.geometry("600x400")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.error_output = ctk.CTkTextbox(self, height=390, width=590, cursor="arrow")
        self.error_output.grid(row=0, column=0, padx=5, pady=5, sticky="nsew",)

        error_lines = "\n\n".join(error_log)
        self.error_output.insert("1.0", error_lines)
        self.error_output.configure(wrap="word", state="disabled", font=("", 14))

class SelectTheme(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Select Theme")
        self.geometry("500x400")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=1, padx=5, pady=2, sticky="nswe")
        top_frame.configure(fg_color="transparent")

        self.button_1 = ctk.CTkButton(top_frame, text="Gruvbox", command=lambda: self.theme_file("gruvbox.json"))
        self.button_1.grid(row=0, column=0,)
        self.button_1.configure(font=("", 14), fg_color=["#d79921", "#b57614"],
            hover_color=["#cc241d", "#9d0006"],
            border_color=["#3c3836", "#ebdbb2"],
            text_color=["#FFFFFF", "#FFFFFF"],
            )
        self.button_1_textbox = ctk.CTkTextbox(top_frame, cursor="arrow")
        self.button_1_textbox.grid(row=0, column=1, sticky="we", pady=5)
        self.button_1_textbox.insert("end" ,"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco.")
        self.button_1_textbox.configure(height=80, width=350, state="disabled",
            fg_color=["#ebdbb2", "#3c3836"],
            border_color=["#3c3836", "#ebdbb2"],
            text_color=["#282828", "#FFFFFF"],
            )

        self.button_2 = ctk.CTkButton(top_frame, text="Default", command=lambda: self.theme_file("default.json"))
        self.button_2.grid(row=1, column=0)
        self.button_2.configure(font=("", 14),
            fg_color=["#978dfd", "#191a19"],
            hover_color=["#6f68bd", "#4b4d4b"],
            border_color=["#3a3666", "#02b508"],
            text_color=["#FFFFFF", "#00ff04"],
            )
        self.button_2_textbox = ctk.CTkTextbox(top_frame, cursor="arrow")
        self.button_2_textbox.grid(row=1, column=1, sticky="we", pady=5)
        self.button_2_textbox.insert("end" ,"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco.")
        self.button_2_textbox.configure(height=80, width=350, state="disabled",
            fg_color=["#7d76d3", "#141414"],
            border_color=["#3a3666", "#02b508"],
            text_color=["#FFFFFF", "#00ff04"],
            )

        self.button_3 = ctk.CTkButton(top_frame, text="Tokyo Night", command=lambda: self.theme_file("tokyo_night.json"))
        self.button_3.grid(row=2, column=0)
        self.button_3.configure(font=("", 14),
            fg_color=["#2959aa", "#7aa2f7"],
            hover_color=["#8c4351", "#f7768e"],
            border_color=["#5a3e8e", "#565f89"],
            text_color=["#FFFFFF", "#24283b"],
            )
        self.button_3_textbox = ctk.CTkTextbox(top_frame, cursor="arrow")
        self.button_3_textbox.grid(row=2, column=1, sticky="we", pady=5)
        self.button_3_textbox.insert("end" ,"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco.")
        self.button_3_textbox.configure(height=80, width=350, state="disabled",
            fg_color=["#e6e7ed", "#414868"],
            border_color=["#5a3e8e", "#565f89"],
            text_color=["#5a3e8e", "#bb9af7"],
            )
        
        self.restart_label = ctk.CTkLabel(top_frame, text="Restart after select!")
        self.restart_label.grid(row=3, column=0, columnspan=2, sticky="we", pady=10)
        self.restart_label.configure(font=("", 20))

        menu_frame = ctk.CTkFrame(self)
        menu_frame.grid(row=0, sticky="nw", pady=(5,15), padx=5)
        menu_frame.configure(fg_color="transparent")

        self.fetch_themes()
        self.themes_list_var = ctk.StringVar(value=themes_files[0])
        self.themes_list_var.trace_add("write", lambda *args: self.theme_file(self.themes_list_var.get()))
        self.themes_list = ctk.CTkOptionMenu(menu_frame, variable=self.themes_list_var, values=themes_files,)
        self.themes_list.grid(row=0, column=0, sticky="w")
        self.themes_list.configure(dynamic_resizing=True)

        self.theme_label = ctk.CTkLabel(menu_frame, text="<-- Check for custom themes.")
        self.theme_label.grid(row=0, column=1, sticky="w", padx=5)
        self.theme_label.configure(font=("", 13))

        self.selected_label = ctk.CTkLabel(self, text="Selected theme: ")
        self.selected_label.grid(row=4, column=0, sticky="sw", padx=5)

    def fetch_themes(self):
        folder = glob.glob(APP_PATH + "/theme/*.json")
        file_names = [os.path.split(path)[1] for path in folder]
        themes_files.clear()
        try:
            for f in file_names:
                themes_files.append(f)
                themes_files.sort()

        except IndexError as e:
            error_log.append(f"Themes fetch error: {e}")

    def theme_file(self, theme_name=None):
        if theme_name:
            settings.read(settings_file_path)

            if "Settings" not in settings:
                settings["Settings"] = {}

            settings["Settings"]["theme"] = theme_name
            with open(settings_file_path, "w") as cf:
                settings.write(cf)

        else:
            print("Theme not selected")

        self.selected_label.configure(text=f"Selected theme: {theme_name}")

class OllamaGUIChat(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.messages = []
        self.full_reply = ""
        self.gpl_opened = None
        self.error_opened = None
        self.theme_opened = None
        self.response = None

        self.title("Ollama GUI Chat")
        self.geometry("800x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.setup_ui()


    def setup_ui(self):

        # top panel buttons
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, padx=5,pady=2, sticky="nswe")
        top_frame.configure(fg_color="transparent")

        self.gpl_button = ctk.CTkButton(top_frame, text="GPL License", command=self.open_gpl)
        self.gpl_button.grid(row=0, column=0, padx=(0,3))
        self.gpl_button.configure(height=20, font=("", 13), width=10, border_width=0)

        self.model_menu_var = ctk.StringVar()
        #self.model_menu_var.set(model_list[0])
        self.model_menu_var.trace_add("write", self.on_model_change)
        self.model_menu = ctk.CTkOptionMenu(top_frame, variable=self.model_menu_var, values=model_list)
        self.model_menu.grid(row=0, column=1, padx=(0,3), pady=(1,0))
        self.model_menu.configure(height=23, font=("", 12), dynamic_resizing=True,)

        self.custom_model_name = ctk.CTkEntry(top_frame,)
        self.custom_model_name.grid(row=0, column=2, padx=(0,3),)
        self.custom_model_name.configure(height=20, font=("", 12), placeholder_text="Custom model...")

        top_frame2 = ctk.CTkFrame(self)
        top_frame2.grid(row=0, columnspan=2, padx=5, pady=2, sticky="e")
        top_frame2.configure(fg_color="transparent")

        self.host_url = ctk.CTkEntry(top_frame2)
        self.host_url.grid(row=0, column=0, padx=(20,3), sticky="e")
        self.host_url.configure(height=20, width=230, font=("", 12), placeholder_text="Host URL...")
        self.host_url.insert(0 , host)

        self.theme_var = ctk.StringVar(value=appearance)
        self.theme_switch = ctk.CTkSwitch(top_frame2, text="light/dark mode", variable=self.theme_var, onvalue="dark", offvalue="light", command=self.theme_modes,)
        self.theme_switch.grid(row=0, column=1, padx=(0,5), sticky="e")

        # mid panel
        self.chat_font_var = ctk.StringVar()
        self.chat_font_var.set(value="14")
        self.chat_output = ctk.CTkTextbox(self, height=600, cursor="arrow")
        self.chat_output.grid(row=1, columnspan=2, padx=5, pady=(5, 2), sticky="nsew",)
        self.chat_output.configure(wrap="word", state="disabled", font=("", int(self.chat_font_var.get())))

        mid_frame = ctk.CTkFrame(self)
        mid_frame.grid(row=2, columnspan=2, sticky="e")
        mid_frame.configure(fg_color="transparent")

        mid_frame2 = ctk.CTkFrame(self)
        mid_frame2.grid(row=2, sticky="w")
        mid_frame2.configure(fg_color="transparent")

        self.save_button = ctk.CTkButton(mid_frame, text="Save", command=self.save_chat)
        self.save_button.grid(row=2, column=0, padx=5,)
        self.save_button.configure(height=10, width=45, corner_radius=5, hover_color="#024f04", border_width=2)

        self.load_button = ctk.CTkButton(mid_frame, text="Load", command=self.load_chat)
        self.load_button.grid(row=2, column=1, padx=(0,5),)
        self.load_button.configure(height=10, width=45, corner_radius=5, hover_color="#1f538d", border_width=2)

        self.clear_button = ctk.CTkButton(mid_frame, text="Clear", command=self.clear_chat)
        self.clear_button.grid(row=2, column=2, padx=(0,5),)
        self.clear_button.configure(height=10, width=45, corner_radius=5, hover_color="#3b0103", border_width=2)

        self.autoscroll_var = ctk.StringVar(value="on")
        self.autoscroll_box = ctk.CTkCheckBox(mid_frame2, text="Autoscroll", variable=self.autoscroll_var, onvalue="on", offvalue="off",)
        self.autoscroll_box.grid(row=2, column=0, padx=(5,0),)
        self.autoscroll_box.configure(font=("", 12), checkbox_width=18, checkbox_height=18)

        self.increase_font = ctk.CTkButton(mid_frame2, text=" + ", command=lambda: self.change_font_size(1))
        self.increase_font.grid(row=2,column=1,)
        self.increase_font.configure(width=10, height=10, corner_radius=5, border_width=2)

        self.decrease_font = ctk.CTkButton(mid_frame2, text=" - ", command=lambda: self.change_font_size(-1))
        self.decrease_font.grid(row=2,column=2, padx=(0,5))
        self.decrease_font.configure(width=10, height=10, corner_radius=5, border_width=2)


        self.progress_bar = ctk.CTkProgressBar(mid_frame2, mode="determinate",)
        self.progress_bar.configure(width=150,)

        self.stop_button = ctk.CTkButton(mid_frame2, text="Stop", command=self.stop_response)

        # lower panel
        self.input_field = ctk.CTkTextbox(self, height=100)
        self.input_field.grid(row=3, column=0, padx=5, pady=(5,5), sticky="nswe",)
        self.input_field.configure(wrap="word",)
        self.input_field.focus_set()

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message_thread)
        self.send_button.grid(row=3, column=1, sticky="we", padx=(0,5), pady=(5,5))
        self.send_button.configure(height=100, width=45, corner_radius=5, border_width=2)

        self.copyright_label = ctk.CTkLabel(self, text="Copyright © 2025 by Kamil Wiśniewski | Ver. 2.0.0")
        self.copyright_label.grid(sticky="se", row=4, column=0, columnspan=2, padx=5)
        self.copyright_label.configure(font=("", 10))

        self.settings_button = ctk.CTkButton(self, text="Change theme", command=self.open_theme_window)
        self.settings_button.grid(row=4, column=0, padx=5, sticky="w")
        self.settings_button.configure(height=10, width=10)



        # keybind
        self.custom_model_name.bind("<Return>", self.custom_model)
        self.custom_model_name.bind("<Control-a>", self.keybinds)
        self.input_field.bind("<Control-a>", self.keybinds)
        self.input_field.bind("<Return>", self.keybinds)
        self.host_url.bind("<Return>", self.check_existing_models)
        self.host_url.bind("<Control-a>", self.keybinds)

        self.check_existing_models()

    # functions
    def keybinds(self, event):
        if event.keysym == "Return" and not (event.state & 0x1):  # Enter
            if self.send_button.cget("state") == "normal":
                self.send_message_thread()
                return "break"

        elif event.keysym == "Return" and (event.state & 0x1):  # Shift+Enter
            self.input_field.insert("end", "\n")
            return "break"

        elif event.keysym.lower() == "a" and (event.state & 0x4):  # Ctrl+A
            widget = event.widget
            if widget == self.input_field._textbox:
                widget.tag_add("sel", "1.0", "end")
                return "break"
            
            elif widget == self.host_url._entry:
                widget.select_range(0, "end")
                return "break"
            
            elif widget == self.custom_model_name._entry:
                widget.select_range(0, "end")
            
        return "break"

    def change_font_size(self, increment):
        font_size = int(self.chat_font_var.get()) + increment
        if font_size < 6:
            font_size = 6
        elif font_size > 48:
            font_size = 48

        self.chat_font_var.set(value=f"{font_size}")
        self.chat_output.configure(font=("", font_size))

    def insert_text(self, content):
        self.chat_output.configure(state="normal")
        self.chat_output.insert("end", content)
        self.chat_output.configure(state="disabled")

        try:
            if self.autoscroll_var.get() == "on":
                self.chat_output.see("end")

        except Exception as e:
            error_log.append(f"Autoscroll error: {e}")
            self.open_error_logs()

    def on_model_change(self, *args):
        self.messages = []
        self.insert_text(f"\nModel changed to: {self.model_menu.get()}\n\n")

    def custom_model(self, event):
        cModel = self.custom_model_name.get()
        if event.keysym == "Return" and not (event.state & 0x1):
            if not cModel:
                return

            self.custom_model_name.delete("0", "end")
            self.check_existing_models()
            model_list.append(cModel)
            self.refresh_model_list()
            self.model_menu_var.set(cModel)

    def refresh_model_list(self):
        self.model_menu.configure(values=model_list)

    def theme_modes(self):
        if self.theme_var.get() == "dark":
            ctk.set_appearance_mode("dark")
            settings.read(settings_file_path)
            settings["Settings"]["appearance"] = "dark"
            with open(settings_file_path, "w") as cf:
                settings.write(cf)
        else:
            ctk.set_appearance_mode("light")
            settings.read(settings_file_path)
            settings["Settings"]["appearance"] = "light"
            with open(settings_file_path, "w") as cf:
                settings.write(cf)

    def open_gpl(self):
        if self.gpl_opened is None or not self.gpl_opened.winfo_exists():
            self.gpl_opened = GPLLicense()

        else:
            self.gpl_opened.focus()

    def open_error_logs(self):
        if self.error_opened is None or not self.error_opened.winfo_exists():
            self.error_opened = ErrorWindow()

        else:
            self.error_opened.destroy()
            self.error_opened = ErrorWindow()

    def open_theme_window(self):
        if self.theme_opened is None or not self.theme_opened.winfo_exists():
            self.theme_opened = SelectTheme()

        else:
            self.theme_opened.destroy()
            self.theme_opened = None

    def clear_chat(self):
        self.chat_output.configure(state="normal")
        self.messages = []
        self.chat_output.delete("1.0", "end")
        self.chat_output.configure(state="disabled")

    def save_chat(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        try:
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    for message in self.messages:
                        f.write(f"{message['role']} : {message['content']}\n")

        except Exception as e:
            error_log.append(f"def save_chat: {e}")
            self.open_error_logs()

    def load_chat(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if not file_path:       # if you dont want to see an error each time you cancel loading - keep this intact
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    self.messages.append({"role": "assistant", "content": line})

        except Exception as e:
            error_log.append(f"def load_chat: {e}")
            self.open_error_logs()

    def stop_response(self):
        last_key = len(self.messages) - 1

        if hasattr(self, "response") and self.response:
            self.response = None
            self.messages.pop(last_key)
            self.insert_text("\n\n[AI] : Response canceled.")

        self.hide_progress()
        self.send_button.configure(state="normal")

    def show_progress(self):
        self.progress_bar.grid(row=2, column=3, sticky="we")
        self.progress_bar.start()

        self.stop_button.grid(row=2, column=4, sticky="we", padx=5)
        self.stop_button.configure(height=10, width=10, corner_radius=5, border_width=2, state="normal")

    def hide_progress(self):
        self.progress_bar.stop()
        self.progress_bar.grid_forget()

        self.stop_button.grid_forget()
        self.stop_button.configure(state="disabled")

    # checks for installed LLMs.
    def check_existing_models(self, *args) -> None:
        model_list.clear()
        try:
            api_url = self.host_url.get().rstrip('/api/chat')
            response = requests.get(
                url=api_url + "/api/tags"
            )
            response.raise_for_status()
            data = response.json()
            model_list.extend([model["name"] for model in data["models"]])
            self.model_menu_var.set(model_list[0])
            self.refresh_model_list()

            api_url = self.host_url.get()
            settings.read(settings_file_path)
            settings["Settings"]["host"] = api_url

            with open(settings_file_path, "w") as cf:
                settings.write(cf)

        except requests.exceptions.RequestException as e:
            model_list.clear()
            self.model_menu_var.set("")
            error_log.append(f"Failed to fetch models: {e}")
            self.open_error_logs()

    # threading for app to not freeze on first message.
    # It used to freeze for a while when Ollama was setting up a server
    def send_message_thread(self):
        question = self.input_field.get("1.0", "end").strip()
        if not question:
            return

        self.insert_text(f"[You] :\n{question}\n\n")
        self.input_field.delete("1.0", "end")       # clear input field

        self.messages.append({"role": "user", "content": question})
        self.send_button.configure(state="disabled")        # disable send button

        t1 = thr.Thread(target=self.send_message)
        t1.start()

        self.show_progress()

    def send_message(self):
        model_name = self.model_menu_var.get()

        payload = {
            "model": model_name,
            "messages": self.messages,
            "stream": True
        }

        url = f"{self.host_url.get().rstrip('/api/chat')}/api/chat"

        try:
            response = requests.post(url, json=payload, stream=True)
            self.response = response

            if response.status_code == 200:
                self.insert_text("[AI] :\n")

                # full_reply "", needed for AI to remember the context of messages.
                # Without this, every new message is considered as new chat or whatever.
                full_reply= ""
                try:
                    for line in response.iter_lines(decode_unicode=True):
                        if self.response is None:       # stop response
                            break

                        elif line.strip():
                            try:
                                data = json.loads(line)
                                content = data.get("message", {}).get("content", "")
                                full_reply += content
                                self.insert_text(content)
                                self.update()

                            except json.JSONDecodeError:
                                error_log.append(f"Failed to Decode line: {line}")
                                self.open_error_logs()
                                continue

                    self.messages.append({"role": "assistant", "content": full_reply})
                    self.insert_text("\n\n")

                except Exception as e:
                    error_log.append(f"Failed to get response: {e}")
                    self.open_error_logs()

            else:
                error_log.append(f"Failed to send message, Status Code: {response.status_code}")
                self.open_error_logs()

        except requests.exceptions.RequestException as e:
            error_log.append(f"Request error: {e}")
            self.open_error_logs()

        finally:
            self.send_button.configure(state="normal")
            self.hide_progress()

if __name__ == "__main__":
    ogc_instance = OllamaGUIChat()
    ogc_instance.mainloop()

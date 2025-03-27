from tkinter import filedialog
import requests
import json
import customtkinter as ctk
import os

# TODO: Add `progressbar` to all jsons.
# Fill README.md


APP_PATH: str = os.path.dirname(os.path.realpath(__file__))
THEME_PATH: str = os.path.join(APP_PATH, "theme", "custom-theme.json")

class GPLLicense(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("GPL License")
        self.geometry("500x300")

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


error_log = []
model_list = []

class OllamaGUIChat(ctk.CTk):
    def __init__(self):

        try:
            ctk.set_default_color_theme(THEME_PATH)
        except Exception as e:
            ctk.set_default_color_theme("blue")
            print(f"Error: {e}")
            error_log.append(f"Error: {e}")

        super().__init__()

        ctk.set_appearance_mode("light")

        self.messages = []
        self.full_reply = ""
        self.gpl_opened = None

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
        self.host_url.insert(0 ,"http://localhost:11434")

        self.theme_var = ctk.StringVar(value="off")
        self.theme_switch = ctk.CTkSwitch(top_frame2, text="light/dark mode", variable=self.theme_var, onvalue="on", offvalue="off", command=self.theme_modes,)
        self.theme_switch.grid(row=0, column=1, padx=(0,5), sticky="e")

        # mid panel
        self.chat_font_var = ctk.StringVar()
        self.chat_font_var.set(value="14")
        self.chat_output = ctk.CTkTextbox(self, height=600, cursor="arrow")
        self.chat_output.grid(row=1, columnspan=2, padx=5, pady=(5, 2), sticky="nsew",)
        self.chat_output.insert("1.0", error_log)
        self.chat_output.configure(wrap="word", state="disabled", font=("", int(self.chat_font_var.get())))

        mid_frame = ctk.CTkFrame(self)
        mid_frame.grid(row=2, columnspan=2, sticky="e")
        mid_frame.configure(fg_color="transparent")

        mid_frame2 = ctk.CTkFrame(self)
        mid_frame2.grid(row=2, sticky="w")
        mid_frame2.configure(fg_color="transparent")

        self.save_button = ctk.CTkButton(mid_frame, text="💾 Save", command=self.save_chat)
        self.save_button.grid(row=2, column=0, padx=5,)
        self.save_button.configure(height=10, width=15, corner_radius=5, hover_color="#024f04", border_width=2)

        self.load_button = ctk.CTkButton(mid_frame, text="📂 Load", command=self.load_chat)
        self.load_button.grid(row=2, column=1, padx=(0,5),)
        self.load_button.configure(height=10, width=15, corner_radius=5, hover_color="#1f538d", border_width=2)

        self.clear_button = ctk.CTkButton(mid_frame, text="💀", command=self.clear_chat)
        self.clear_button.grid(row=2, column=2, padx=(0,5),)
        self.clear_button.configure(height=10, width=10, corner_radius=5, hover_color="#3b0103", border_width=2)

        self.autoscroll_var = ctk.StringVar(value="on")
        self.autoscroll_box = ctk.CTkCheckBox(mid_frame2, text="Autoscroll", variable=self.autoscroll_var, onvalue="on", offvalue="off",)
        self.autoscroll_box.grid(row=2, column=0, padx=(5,0),)
        self.autoscroll_box.configure(font=("", 12), checkbox_width=18, checkbox_height=18)

        self.increase_font = ctk.CTkButton(mid_frame2, text="🔺", command=lambda: self.change_font_size(1))
        self.increase_font.grid(row=2,column=1,)
        self.increase_font.configure(width=10, height=10, corner_radius=5, border_width=2)

        self.decrease_font = ctk.CTkButton(mid_frame2, text="🔻", command=lambda: self.change_font_size(-1))
        self.decrease_font.grid(row=2,column=2, padx=(0,5))
        self.decrease_font.configure(width=10, height=10, corner_radius=5, border_width=2)


        self.progress_bar = ctk.CTkProgressBar(mid_frame2, mode="determinate",)
        self.progress_bar.configure(width=150,)

        # lower panel
        self.input_field = ctk.CTkTextbox(self, height=100)
        self.input_field.grid(row=3, column=0, padx=5, pady=(5,5), sticky="nswe",)
        self.input_field.configure(wrap="word",)
        self.input_field.focus_set()

        self.send_button = ctk.CTkButton(self, text="📤", command=self.send_message)
        self.send_button.grid(row=3, column=1, sticky="we", padx=(0,5), pady=(5,5))
        self.send_button.configure(height=100, width=10, corner_radius=5, border_width=2)

        self.copyright_label = ctk.CTkLabel(self, text="Copyright © 2025 by Kamil Wiśniewski | Ver. 1.5")
        self.copyright_label.grid(sticky="se", row=4, column=0, columnspan=2, padx=5)
        self.copyright_label.configure(font=("", 10))



        # keybind
        self.custom_model_name.bind("<Return>", self.custom_model)
        self.input_field.bind("<Control-a>", self.keybinds)
        self.input_field.bind("<Return>", self.keybinds)


        self.check_existing_models()

    # functions
    def keybinds(self, event):
        if event.keysym == "Return" and not (event.state & 0x1):  # Enter
            if self.send_button.cget("state") == "normal":
                self.send_message()
                return "break"

        elif event.keysym == "Return" and (event.state & 0x1):  # Shift+Enter
            self.input_field.insert("end", "\n")
            return "break"

        elif event.keysym.lower() == "a" and (event.state & 0x4):  # Ctrl+A
            self.input_field.tag_add("sel", "1.0", "end")
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
            print(f"Error: {e}")

    def on_model_change(self, *args):
        self.messages = []
        self.insert_text(f"\nModel changed to: {self.model_menu.get()}\n\n")

    def custom_model(self, event):
        cModel = self.custom_model_name.get()
        if event.keysym == "Return" and not (event.state & 0x1):
            if not cModel:
                return

            self.custom_model_name.delete("0", "end")
            model_list.append(cModel)
            self.refresh_model_list()
            self.model_menu_var.set(cModel)

    def refresh_model_list(self):
        self.model_menu.configure(values=model_list)

    def theme_modes(self):
        if self.theme_var.get() == "on":
            ctk.set_appearance_mode("dark")

        else:
            ctk.set_appearance_mode("light")

    def open_gpl(self):
        if self.gpl_opened is None or not self.gpl_opened.winfo_exists():
            self.gpl_opened = GPLLicense()

        else:
            self.gpl_opened.focus()

    def clear_chat(self):
        self.chat_output.configure(state="normal")
        self.messages = []
        self.chat_output.delete("1.0", "end")
        self.chat_output.configure(state="disabled")

    def save_chat(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            with open(file_path, "w") as f:
                for message in self.messages:
                    f.write(f"{message['role']} : {message['content']}\n")

    def load_chat(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        with open(file_path, "r") as f:
            for line in f.readlines():
                self.messages.append({"role": "assistant", "content": line})

    def show_progress(self):
        self.progress_bar.grid(row=2, column=3, sticky="we")
        self.progress_bar.start()

    def hide_progress(self):
        self.progress_bar.stop()
        self.progress_bar.grid_forget()

    # checks for installed LLMs.
    def check_existing_models(self) -> None:
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

        except requests.exceptions.RequestException as e:
            print(f"Error while checking models: {e}")
            self.insert_text(f"Error while checking models: {e}\n\n")

    def send_message(self):
        question = self.input_field.get("1.0", "end").strip()
        if not question:
            return

        model_name = self.model_menu_var.get()

        self.insert_text(f"[You] :\n{question}\n\n")
        self.input_field.delete("1.0", "end")       # clear input field

        self.messages.append({"role": "user", "content": question})
        self.send_button.configure(state="disabled")        # disable send button


        payload = {
            "model": model_name,
            "messages": self.messages,
            "stream": True
        }

        url = f"{self.host_url.get().rstrip('/api/chat')}/api/chat"

        try:
            response = requests.post(url, json=payload, stream=True)

            if response.status_code == 200:
                self.insert_text("[AI] :\n")
                #self.update()

                # full_reply "", needed for AI to remember the context of messages.
                # Without this, every new message is considered as new chat or whatever.
                full_reply= ""
                for line in response.iter_lines(decode_unicode=True):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            full_reply += content
                            self.show_progress()
                            self.insert_text(content)
                            self.update()

                        except json.JSONDecodeError:
                            continue

                self.messages.append({"role": "assistant", "content": full_reply})
                self.insert_text("\n\n")

            else:
                self.insert_text(f"\nError: {response.status_code}\n{response.text}\n\n")

        except requests.exceptions.RequestException as e:
            self.insert_text(f"\nError sending request: {e}\n\n")

        self.send_button.configure(state="normal")
        self.hide_progress()

ollama_gui = OllamaGUIChat()
ollama_gui.mainloop()

from tkinter import filedialog
import requests
import json
import customtkinter as ctk
import os

APP_PATH: str = os.path.dirname(os.path.realpath(__file__))
THEME_PATH: str = os.path.join(APP_PATH, "theme", "custom-theme.json")
ctk.set_default_color_theme(THEME_PATH)

url = "http://localhost:11434/api/chat"

model_list = [
    "llama3.1",
    "llama3.2",
    "llama3.3",
    "gemma3",
    "qwq",
    "deepseek-r1",
    "phi4",
    "phi4-mini",
    "mistral",
    "moondream",
    "starling-lm",
    "codellama",
    "llama2-uncensored",
    "llava",
    "granite3.2",
]

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
        self.label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


class OllamaGUIChat(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")

        self.messages = []
        self.gpl_opened = None

        self.title("Ollama GUI Chat")
        self.geometry("800x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.setup_ui()


    def setup_ui(self):

        # top panel buttons
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(padx=5,pady=2, sticky="nswe")
        top_frame.configure(fg_color="transparent")

        #self.theme_button = ctk.CTkButton(top_frame, text="🌗Toogle theme",)
        #self.theme_button.grid(row=0, column=1, padx=(0,3))
        #self.theme_button.configure(height=20, font=("", 12), width=10)

        self.gpl_button = ctk.CTkButton(top_frame, text="GPL License", command=self.open_gpl)
        self.gpl_button.grid(row=0, column=2, padx=(0,3))
        self.gpl_button.configure(height=20, font=("", 13), width=10,)

        self.model_menu_var = ctk.StringVar()
        self.model_menu_var.set(model_list[0])
        self.model_menu_var.trace_add("write", self.on_model_change)
        self.model_menu = ctk.CTkOptionMenu(top_frame, variable=self.model_menu_var, values=model_list)
        self.model_menu.grid(row=0, column=3, padx=(0,3), pady=(1,0))
        self.model_menu.configure(height=23, font=("", 12), dynamic_resizing=True,)

        self.custom_model_name = ctk.CTkEntry(top_frame,)
        self.custom_model_name.grid(row=0, column=4, padx=(0,3),)
        self.custom_model_name.configure(height=20, font=("", 12), placeholder_text="Custom model...")

        self.theme_var = ctk.StringVar(value="off")
        self.theme_switch = ctk.CTkSwitch(self, text="light/dark mode", variable=self.theme_var, onvalue="on", offvalue="off", command=self.theme_modes)
        self.theme_switch.grid(row=0, columnspan=2, padx=(0,5), sticky="e")

        # mid panel
        self.chat_output = ctk.CTkTextbox(self, height=600)
        self.chat_output.grid(row=1, columnspan=2, padx=5, pady=(5,2), sticky="nsew",)
        self.chat_output.configure(wrap="word", state="disabled",
            font=("", 14)
        )

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_chat)
        self.save_button.grid(row=2, column=0, sticky="e", padx=5)
        self.save_button.configure(height=10, width=10, corner_radius=5, hover_color="#024f04", anchor="center", border_width=2)

        self.clear_button = ctk.CTkButton(self, text="Clear", command=self.clear_chat)
        self.clear_button.grid(row=2, column=1, sticky="e", padx=(0,5))
        self.clear_button.configure(height=10, width=10, corner_radius=5, hover_color="#3b0103", anchor="center", border_width=2)

        # lower panel
        self.input_field = ctk.CTkTextbox(self, height=100)
        self.input_field.grid(row=3, column=0, padx=5, pady=(5,5), sticky="nswe",)
        self.input_field.configure(wrap="word",)
        self.input_field.focus_set()

        self.send_button = ctk.CTkButton(self, text="📤", command=self.send_message)
        self.send_button.grid(row=3, column=1, sticky="we", padx=(0,5), pady=(5,5))
        self.send_button.configure(height=100, width=10, corner_radius=5, anchor="center", border_width=2)

        self.copyright_label = ctk.CTkLabel(self, text="Copyright (c) 2025 by Kamil Wiśniewski")
        self.copyright_label.grid(sticky="se", row=4, column=0, columnspan=2, padx=5)
        self.copyright_label.configure(font=("", 10))



        # keybind
        self.custom_model_name.bind("<Return>", self.custom_model)
        self.input_field.bind("<Control-a>", self.keybinds)
        self.input_field.bind("<Return>", self.keybinds)


    # functions
    def keybinds(self, event):
        if event.keysym == "Return" and not (event.state & 0x1):  # Enter
            self.send_message()
            return "break"

        elif event.keysym == "Return" and (event.state & 0x1):  # Shift+Enter
            self.input_field.insert("end", "\n")
            return "break"

        elif event.keysym.lower() == "a" and (event.state & 0x4):  # Ctrl+A
            self.input_field.tag_add("sel", "1.0", "end")
            return "break"

    def insert_text(self, content):
        self.chat_output.configure(state="normal")
        self.chat_output.insert("end", content)
        self.chat_output.configure(state="disabled")

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
                f.write(self.chat_output.get("1.0", "end"))

    def send_message(self):
        question = self.input_field.get("1.0", "end").strip()
        if not question:
            return

        model_name = self.model_menu_var.get()

        self.insert_text(f"You: {question}\n\n")
        self.input_field.delete("1.0", "end")       # clear input field

        self.messages.append({"role": "user", "content": question})
        self.send_button.configure(state="disabled")        # disable send button

        payload = {
            "model": model_name,
            "messages": self.messages,
            "stream": True
        }

        try:
            response = requests.post(url, json=payload, stream=True)

            if response.status_code == 200:
                self.insert_text("AI: ")
                self.update()

                # full_reply "", needed for AI to remember the context of messages.
                # Without this, every new message is considered as new chat or whatever.
                full_reply = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            full_reply += content
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

ollama_gui = OllamaGUIChat()
ollama_gui.mainloop()

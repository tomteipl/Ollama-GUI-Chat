import requests
import json
import tkinter as tk
from tkinter import scrolledtext, ttk

# Base URL for the local Ollama API
url = "http://localhost:11434/api/chat"
#model_name = "llama3.1"  # Only model being used

class LlamaGUI:
    def __init__(self):
        self.messages = []           # Stores the conversation history

        self.window = tk.Tk()
        self.window.title("Ollama Chat")
        self.window.geometry("700x700")
        self.window.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Top-left frame for buttons
        top_frame = tk.Frame(self.window)
        top_frame.pack(anchor="nw", padx=10, pady=(10, 0))

        #top_label = tk.Label(top_frame, text="Ollama Chat", font=("Arial", 12))
        #top_label.pack(side="top")

        # Dropdown menu with models
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

        self.model_var = tk.StringVar(value=model_list[0])

        self.model_menu = tk.OptionMenu(top_frame, self.model_var, *model_list)
        self.model_menu.pack(side="bottom", fill="both")

        # Chat history (read-only)
        self.text_area = scrolledtext.ScrolledText(
            self.window, width=80, height=25, wrap="word",
            state="disabled"
        )
        self.text_area.pack(pady=5, fill="x")

        # Input field
        self.entry_field = tk.Text(
            self.window, width=80, height=4, wrap="word",
            bg="white"
        )
        self.entry_field.pack(padx=10, pady=5)
        self.entry_field.focus_set()

        # Send button
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message, borderwidth=2)
        self.send_button.pack(pady=5)

        # Theme button
        self.theme_button = tk.Button(top_frame, text="🌗", command=self.toggle_theme, borderwidth=2)
        self.theme_button.pack(side="left")

        # GPL button
        self.gpl_button = tk.Button(top_frame, text="GPL License", command=self.show_gpl_license, borderwidth=2)
        self.gpl_button.pack(side="left")

        # Key bindings
        self.entry_field.bind("<Return>", self.on_enter)
        self.entry_field.bind("<Shift-Return>", self.insert_newline)

        self.custom_theme = None
        self.default_colors()

    def show_gpl_license(self):
        gpl_window = tk.Toplevel(self.window)
        gpl_window.title("GPL License")
        gpl_text = tk.Label(gpl_window, text="""
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
        """, justify="left")

        gpl_text.pack(padx=10, pady=10)

    def insert_newline(self, event):
        self.entry_field.insert(tk.INSERT, "\n")
        return "break"

    def on_enter(self, event):
        self.send_button.invoke()
        return "break"

    def insert_text(self, content):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, content)
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def toggle_theme(self):
        if self.custom_theme:
            self.default_colors()

        else:
            self.load_custom_theme(filename="theme.json")

    def load_custom_theme(self, filename):
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
                self.custom_theme = config
                self.apply_theme_config(config)

        except FileNotFoundError:
            print(f"Config file '{filename}' not found.")

        except json.JSONDecodeError:
            print(f"Invalid JSON in config file '{filename}'.")
            self.apply_theme_config(self.custom_theme)

    def default_colors(self):
        self.custom_theme = None

        text_area_bg = "#7d76d3"
        text_fg = "#FFFFFF"
        window_bg = "#5c549f"
        button_bg = "#978dfd"
        highlight_bg = "#5c549f"

        self.window.config(bg=window_bg)
        self.text_area.config(bg=text_area_bg, fg=text_fg)
        self.entry_field.config(bg=text_area_bg, fg=text_fg)

        self.gpl_button.config(bg=button_bg, fg=text_fg, highlightbackground=highlight_bg)

        self.send_button.config(bg=button_bg, fg=text_fg, highlightbackground=highlight_bg)

        self.theme_button.config(bg=button_bg, fg=text_fg, highlightbackground=highlight_bg)

        self.model_menu.config(bg=button_bg, fg=text_fg, highlightbackground=highlight_bg, justify="center")

    def apply_theme_config(self, config):
        self.window.config(bg=config.get('window_bg', '#5c549f'))
        self.text_area.config(bg=config.get('text_area_bg', '#7d76d3'), fg=config.get('text_fg', '#FFFFFF'))

        self.entry_field.config(bg=config.get('text_area_bg', '#7d76d3'), fg=config.get('text_fg', '#FFFFFF'))

        self.gpl_button.config(bg=config.get('button_bg', '#978dfd'), fg=config.get('text_fg', '#FFFFFF'), highlightbackground=config.get('highlight_bg', '#5c549f'))

        self.send_button.config(bg=config.get('button_bg', '#978dfd'), fg=config.get('text_fg', '#FFFFFF'), highlightbackground=config.get('highlight_bg', '#5c549f'))

        self.theme_button.config(bg=config.get("button_bg", "#978dfd"), fg=config.get('text_fg', '#FFFFFF'), highlightbackground=config.get('highlight_bg', '#5c549f'))

        self.model_menu.config(bg=config.get('button_bg', '#978dfd'), fg=config.get('text_fg', '#FFFFFF'), highlightbackground=config.get('highlight_bg', '#5c549f'), justify="center")


    def send_message(self):
        question = self.entry_field.get("1.0", tk.END).strip()
        if not question:
            return

        model_name = self.model_var.get()

        self.insert_text(f"You: {question}\n\n")
        self.entry_field.delete("1.0", tk.END)

        self.messages.append({"role": "user", "content": question})
        self.send_button.config(state=tk.DISABLED)

        payload = {
            "model": model_name,
            "messages": self.messages,
            "stream": True
        }

        try:
            response = requests.post(url, json=payload, stream=True)

            if response.status_code == 200:
                self.insert_text("AI: ")
                self.window.update()

                full_reply = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            full_reply += content
                            self.insert_text(content)
                            self.window.update()

                        except json.JSONDecodeError:
                            continue

                self.messages.append({"role": "assistant", "content": full_reply})
                self.insert_text("\n\n")

            else:
                self.insert_text(f"\nError: {response.status_code}\n{response.text}\n\n")

        except requests.exceptions.RequestException as e:
            self.insert_text(f"\nError sending request: {e}\n\n")

        self.send_button.config(state=tk.NORMAL)

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    llama_gui = LlamaGUI()
    llama_gui.start()


import requests
import json
import tkinter as tk
from tkinter import scrolledtext

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

class LlamaGUI:
    def __init__(self):
        self.messages = []           # Stores the conversation history

        self.window = tk.Tk()
        self.window.title("Ollama Chat")
        self.window.geometry("800x800")
        self.window.resizable(True, True)
        self.window.pack_propagate(False)

        self.setup_ui()

    def setup_ui(self):
        # Top-left frame for buttons
        top_frame = tk.Frame(self.window)
        top_frame.pack(anchor="nw", pady=(0, 2))

        # Chat history (read-only)
        self.text_area = scrolledtext.ScrolledText(
            self.window, width=80, height=25,wrap="word",
            state="disabled"
        )
        self.text_area.pack(pady=(5, 0), fill="both", expand=True)
        self.text_area.pack_propagate(False)
        self.text_area.config()

        # Clear and Save buttons wrapper
        cs_frame = tk.Frame(self.window)
        cs_frame.pack(pady=(0, 4), anchor="e", padx=13)

        # Clear button
        self.clear_button = tk.Button(cs_frame, text="💀", command=self.clear_chat,)
        self.clear_button.pack(side="right", fill="both")
        self.clear_button.config(relief="flat", borderwidth=1,
            width=1, height=1, font=("", 8),
        )

        # Save button
        self.save_button = tk.Button(cs_frame, text="💾",)
        self.save_button.pack(side="right", fill="both")
        self.save_button.config(relief="flat", borderwidth=1,
            width=1, height=1, font=("", 8),
        )

        # Entry field
        # Wrapper frame to prevent the input field from expanding
        input_frame = tk.Frame(self.window, height=80)
        input_frame.pack(padx=(15, 5), pady=4, fill="x")
        input_frame.pack_propagate(False)

        self.entry_field = tk.Text(
            input_frame, wrap="word",
        )
        self.entry_field.pack(fill="both", expand=True)
        self.entry_field.focus_set()

        # Send button
        self.send_button = tk.Button(self.window, text="🗨️ Send", command=self.send_message, borderwidth=2)
        self.send_button.pack(pady=5)

        # Theme button
        self.theme_button = tk.Button(top_frame, text="🌗Toogle theme", command=self.toggle_theme, borderwidth=1)
        self.theme_button.pack(side="left", fill="both")

        # GPL button
        self.gpl_button = tk.Button(top_frame, text="GPL License", command=self.show_gpl_license, borderwidth=1,)
        self.gpl_button.pack(side="left", fill="both")

        # Model select menu
        self.model_var = tk.StringVar(value=model_list[0])
        self.model_var.trace_add("write", self.on_model_change)
        self.model_menu = tk.OptionMenu(top_frame, self.model_var, *model_list)
        self.model_menu.pack(side="left", fill="both")
        self.model_menu.config(height=1, anchor="w",        # set "width" to stop expanding
            borderwidth=1,
            highlightthickness=1,
        )

        # Custom model name
        self.custom_model_name = tk.Text(
            top_frame, width=18, height=1,
            borderwidth=0,
            highlightthickness=1,
        )
        self.custom_model_name.pack(side="right", fill="both", expand=True,)
        self.custom_model_name.pack_propagate(False)

        # Key bindings
        self.entry_field.bind("<Return>", self.keybindings)
        self.entry_field.bind("<Shift-Return>", self.keybindings)
        self.entry_field.bind("<Control-a>", self.keybindings)
        self.custom_model_name.bind("<Return>", self.custom_model)

        # Toogle on startup
        self.custom_theme = None
        self.load_custom_theme(filename="theme.json")

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

    def keybindings(self, event):
        if event.keysym == "Return" and not (event.state & 0x1):  # Enter
            self.send_message()
            return "break"

        elif event.keysym == "Return" and (event.state & 0x1):  # Shift+Enter
            self.entry_field.insert(tk.END, "\n")
            return "break"

        elif event.keysym.lower() == "a" and (event.state & 0x4):  # Ctrl+A
            self.entry_field.tag_add(tk.SEL, "1.0", tk.END)
            return "break"

    def clear_chat(self):
        self.text_area.config(state="normal")
        self.messages= []
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state="disabled")

    def insert_text(self, content):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, content)
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def refresh_model_list(self):
        self.model_menu["menu"].delete(0, "end")
        for model in model_list:
            self.model_menu["menu"].add_command(
                label=model,
                command=lambda value=model: self.model_var.set(value)
            )

    def custom_model(self, event):
        cModel = self.custom_model_name.get("1.0", tk.END).strip()
        if event.keysym == "Return" and not (event.state & 0x1):
            if not cModel:
                return

            self.custom_model_name.delete("1.0", tk.END)
            model_list.append(cModel)
            self.refresh_model_list()
            self.model_var.set(cModel)

    # clear messages history on model change.
    def on_model_change(self, *args):
        self.messages = []
        self.insert_text(f"\nModel changed to: {self.model_var.get()}\n\n")

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
            self.default_colors()

        except json.JSONDecodeError:
            print(f"Invalid JSON in config file '{filename}'.")
            self.apply_theme_config(self.custom_theme)
            self.default_colors()

    def default_colors(self):
        self.custom_theme = None
        self.window.config(bg="#5c549f")
        self.text_area.config(
            bg="#7d76d3", fg="#FFFFFF",
            font=("", 12),
            highlightbackground="#000",
        )
        self.entry_field.config(
            bg="#7d76d3", fg="#FFFFFF",
            font=("", 12),
            highlightbackground="#000",
        )

        self.gpl_button.config(
            bg="#978dfd", fg="#FFFFFF", highlightbackground="#5c549f",
            pady=0.5,
        )

        self.send_button.config(
            bg="#978dfd", fg="#FFFFFF", highlightbackground="#5c549f"
        )

        self.theme_button.config(
            bg="#978dfd", fg="#FFFFFF", highlightbackground="#5c549f",
            pady=0.5,
        )

        self.model_menu.config(
            bg="#978dfd", fg="#FFFFFF", highlightbackground="#5c549f",
            justify="center",
        )

        self.custom_model_name.config(
            bg="#a9a9a9", fg="#000",
            pady=0.5,
            highlightbackground="#5c549f",
        )

        self.clear_button.config(
            bg="#370405", fg="#FFFFFF", highlightbackground="#978dfd",
        )

        self.save_button.config(
            bg="#0c5601", fg="#FFFFFF", highlightbackground="#978dfd",
        )

    def apply_theme_config(self, config):
        # get theme from JSON tree, example "buttons -> send_button -> bg: #9d604d"
        self.window.config(
            bg=config.get("window", {}).get('bg', '#5c549f')
        )
        self.text_area.config(
            bg=config.get("text_area", {}).get("bg", "#7d76d3"),
            fg=config.get("text_area", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("text_area", {}).get("highlight_bg", "#000"),
            font=("", config.get("text_area", {}).get("font_size", 12)),
        )

        self.entry_field.config(
            bg=config.get("entry_field", {}).get("bg", "#7d76d3"),
            fg=config.get("entry_field", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("entry_field", {}).get("highlight_bg", "#000"),
            font=("", config.get("entry_field", {}).get("font_size", 12)),
        )

        self.gpl_button.config(
            bg=config.get("buttons", {}).get("gpl_button", {}).get("bg", "#978dfd"),
            fg=config.get("buttons", {}).get("gpl_button", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("buttons", {}).get("gpl_button", {}).get("highlight_bg", "#5c549f"),
            pady=0.5,
        )

        self.send_button.config(
            bg=config.get("buttons", {}).get("send_button", {}).get("bg", "#978dfd"),
            fg=config.get("buttons", {}).get("send_button", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("buttons", {}).get("send_button", {}).get("highlight_bg", "#5c549f"),
        )

        self.theme_button.config(
            bg=config.get("buttons", {}).get("theme_button", {}).get("bg", "#978dfd"),
            fg=config.get("buttons", {}).get("theme_button", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("buttons", {}).get("theme_button", {}).get("highlight_bg", "#5c549f"),
            pady=0.5,
        )

        self.model_menu.config(
            bg=config.get("model_menu", {}).get("bg", "#978dfd"),
            fg=config.get("model_menu", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("model_menu", {}).get("highlight_bg", "#5c549f"),
            justify="center",
            pady=0.5,
        )

        self.custom_model_name.config(
            bg=config.get("model_input", {}).get("bg", "#a9a9a9"),
            fg=config.get("model_input", {}).get("fg", "#000"),
            highlightbackground=config.get("model_input", {}).get("highlight_bg", "#5c549f"),
        )

        self.clear_button.config(
            bg=config.get("buttons", {}).get("clear_button", {}).get("bg", "#370405"),
            fg=config.get("buttons", {}).get("clear_button", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("buttons", {}).get("clear_button", {}).get("highlight_bg", "#5c549f"),
        )

        self.save_button.config(
            bg=config.get("buttons", {}).get("save_button", {}).get("bg", "#0c5601"),
            fg=config.get("buttons", {}).get("save_button", {}).get("fg", "#FFFFFF"),
            highlightbackground=config.get("buttons", {}).get("save_button", {}).get("highlight_bg", "#5c549f"),
        )

    def send_message(self):
        question = self.entry_field.get("1.0", tk.END).strip()
        if not question:
            return

        model_name = self.model_var.get()

        self.insert_text(f"You: {question}\n\n")
        self.entry_field.delete("1.0", tk.END)      # clear the input field

        self.messages.append({"role": "user", "content": question})
        self.send_button.config(state=tk.DISABLED)  # disable the send button while waiting for the response

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


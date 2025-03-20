import requests
import json
import tkinter as tk
from tkinter import scrolledtext

# Base URL for the local Ollama API
url = "http://localhost:11434/api/chat"
model_name = "llama3.1"  # Only model being used

class LlamaGUI:
    def __init__(self):
        self.messages = []           # Stores the conversation history
        self.dark_mode = False       # Dark mode toggle

        self.window = tk.Tk()
        self.window.title("Ollama Chat")
        self.window.geometry("700x700")

        self.setup_ui()

    def setup_ui(self):
        # Top-left frame for dark mode toggle
        top_frame = tk.Frame(self.window)
        top_frame.pack(anchor="nw", padx=10, pady=(10, 0))

        self.dark_button = tk.Button(top_frame, text="🌗", command=self.toggle_dark_mode)
        self.dark_button.pack(side="left")

        # Chat history (read-only)
        self.text_area = scrolledtext.ScrolledText(
            self.window, width=80, height=25, wrap="word",
            state="disabled", bg="white", fg="black"
        )
        self.text_area.pack(padx=10, pady=10)

        # Input field
        self.entry_field = tk.Text(
            self.window, width=80, height=4, wrap="word",
            bg="white", fg="black"
        )
        self.entry_field.pack(padx=10, pady=5)
        self.entry_field.focus_set()

        # Send button
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Key bindings
        self.entry_field.bind("<Return>", self.on_enter)
        self.entry_field.bind("<Shift-Return>", self.insert_newline)

        # GPL button
        self.gpl_button = tk.Button(top_frame, text="GPL License", command=self.show_gpl_license)
        self.gpl_button.pack(side="right")

        # Set Dark mode as default
        self.toggle_dark_mode()

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

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "grey9" if self.dark_mode else "Slate Blue"
        fg_color = "#5ef75e" if self.dark_mode else "white"
        window_bg = "black" if self.dark_mode else "Dark Slate Blue"

        self.text_area.config(bg=bg_color, fg=fg_color)
        self.entry_field.config(bg=bg_color, fg=fg_color)
        self.window.config(bg=window_bg)
        self.gpl_button.config(bg=window_bg, fg=fg_color)
        self.send_button.config(bg=window_bg, fg=fg_color)
        self.dark_button.config(bg=window_bg, fg=fg_color)

    def send_message(self):
        question = self.entry_field.get("1.0", tk.END).strip()
        if not question:
            return

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


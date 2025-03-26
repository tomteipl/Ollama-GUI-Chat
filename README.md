<div align="center">
    <h1> Ollama-GUI-Chat </h1>
</div>

![OGC default colors photo](src/Ollama_default_colors2.png)

![GitHub License](https://img.shields.io/github/license/tomteipl/Ollama-GUI-Chat?style=for-the-badge&logo=apache&logoSize=auto&labelColor=%235c549f&color=orange)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/tomteipl/Ollama-GUI-Chat?style=for-the-badge&logo=githubactions&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/tomteipl/Ollama-GUI-Chat?style=for-the-badge&logo=github&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)
![GitHub Release](https://img.shields.io/github/v/release/tomteipl/Ollama-GUi-Chat?sort=date&display_name=tag&style=for-the-badge&logo=codesandbox&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)
![Static Badge Python](https://img.shields.io/badge/Python-100%25-dark?style=for-the-badge&logo=python&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)

OGC (Ollama-GUI-Chat) is a simple chat app that uses
**[Ollama](https://ollama.com/)** AI models
installed on your hardware. You can use models predefined in DropdownMenu
or simply type your custom model name in window.
The app is written in **Python** using modules like
`customtkinter`, `tkinter`, `requests` and `json`

OGC sends a `payload` to your local server with `Ollama` model.
By default its `http://localhost:11434/api/chat`.
If you want to use external server, you can change the `url`
in `OllamaGUIChat.py` file.

```python
url = "http://localhost:11434/api/chat"
```

## Table of Contents

* **[Features][1]**
* **[Installation][2]**
* **[Customization][3]**
* **[Themes][4]**
  * [Gruvbox][5]
  * [Tokyo Night][6]

[1]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#features
[2]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#installation
[3]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#customization
[4]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#themes
[5]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#gruvbox
[6]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#tokyo-night

## Features

* Talk with **Ollama** AI models with style using GUI
* Choose model from list or type your **own** model name
* Save chat history to file
* Clear chat history
* Light and Dark modes
* **Most important**, customize style of whole app with simple `JSON` file !
* Its free and open source. Use the source code to customize the app even more !

## Installation

* **Download** latest [release](https://github.com/tomteipl/Ollama-GUI-Chat/releases/latest)
* **Extract** the archive
* **Enjoy**

>[!NOTE]
>*`custom_theme.json` is located inside of `_internal/theme` folder.*

## Customization

![OGC default colors photo](src/Ollama_default_colors1.png)

You can customize style of the app by editing `custom-theme.json`.
**OGC** is searching for `json` file in `_internal/theme` folder.

Part of `custom-theme.json` file:

```json
{
  "CTk": {
    "fg_color": ["#5c549f", "#000"]
  },
  "CTkToplevel": {
    "fg_color": ["#5c549f", "#000"]
  },
  "CTkFrame": {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ["gray90", "gray13"],
    "top_fg_color": ["gray85", "gray16"],
    "border_color": ["gray65", "gray28"]
  },
  "CTkButton": {
    "corner_radius": 6,
    "border_width": 1,
    "fg_color": ["#978dfd", "#191a19"],
    "hover_color": ["#6f68bd", "#4b4d4b"],
    "border_color": ["#3a3666", "#02b508"],
    "text_color": ["#FFFFFF", "#00ff04"],
    "text_color_disabled": ["gray74", "gray60"]
  },
  "CTkLabel": {
    "corner_radius": 0,
    "fg_color": "transparent",
    "text_color": ["#FFFFFF", "#00ff04"]
```

Its pretty easy and self explanatory. Just change the values
and see the changes in the app.
You can use `HEX` colors or `names` like `"green"`.

Detailed usage of theme file you can find on
official [CustomTkinter](https://customtkinter.tomschimansky.com/documentation/)
page.

You can change the list of models directly in `OllamaGUIChat.py` file

```python
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
```

as well as the default Theme `PATH`

```python
APP_PATH: str = os.path.dirname(os.path.realpath(__file__))
THEME_PATH: str = os.path.join(APP_PATH, "theme", "custom-theme.json")
ctk.set_default_color_theme(THEME_PATH)
```

## Themes (WIP)

You can find more themes in **[themes](themes/)** folder.
Each theme has light and dark mode.

>[!TIP]
>Copy and paste whole code from any theme preset into `custom_theme.json`.

### Gruvbox

![Gruvbox Theme](src/Ollama_gruvbox.png)

### Tokyo Night

![Tokyo Night Theme](src/Ollama-tokyo_night.png)

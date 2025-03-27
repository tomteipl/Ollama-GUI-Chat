<div align="center">
    <h1> Ollama-GUI-Chat </h1>
</div>

![OGC default colors photo](assets/Ollama_default_colors5.png)

![GitHub License](https://img.shields.io/github/license/tomteipl/Ollama-GUI-Chat?style=for-the-badge&logo=apache&logoSize=auto&labelColor=%235c549f&color=orange)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/tomteipl/Ollama-GUI-Chat?style=for-the-badge&logo=githubactions&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/tomteipl/Ollama-GUI-Chat?style=for-the-badge&logo=github&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)
![GitHub Release](https://img.shields.io/github/v/release/tomteipl/Ollama-GUi-Chat?sort=date&display_name=tag&style=for-the-badge&logo=codesandbox&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)
![Static Badge Python](https://img.shields.io/badge/Python-100%25-dark?style=for-the-badge&logo=python&logoColor=black&logoSize=auto&labelColor=%235c549f&color=orange)

OGC (Ollama-GUI-Chat) is a simple chat app that uses **[Ollama](https://ollama.com/)**
AI models installed on your hardware.
You can use models predefined in the dropdown menu
or simply type your custom model name in the window.
The app is written in **Python** using modules
like `customtkinter`, `tkinter`, `requests`, and `json`.

OGC sends a `payload` to your local server with the `Ollama` model.
By default, it's `http://localhost:11434/api/chat`.
You can enter custom `URL`, when you open the app
there is inserted default URL.

## Table of Contents

* **[Features][1]**
* **[Installation][2]**
* **[Customization][3]**
* **[Themes][4]**
  * [Gruvbox][5]
  * [Tokyo Night][6]
* **[Roadmap][7]**
* **[License](LICENSE)**

[1]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#features
[2]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#installation
[3]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#customization
[4]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#themes
[5]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#gruvbox
[6]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#tokyo-night
[7]: https://github.com/tomteipl/Ollama-GUI-Chat?tab=readme-ov-file#roadmap

## 🔥 Features

* ✏️ Talk with **Ollama** AI models with style using light GUI app.
* 📂 Choose a model from the list or type your **own** model name.
* 🔖 Save and Clear chat history.
* 🍻 Load chat from a saved file and continue your conversation.
* 🌓 Light and Dark modes.
* 🗽 Auto detect your LLMs.
* 🌹 **Most important**, customize the style of the whole app with a simple `JSON` file !
* 🎁 Its free and open-source. Use the source code to customize the app even more !
* And **more** in development...

## 👷 Installation

>[!IMPORTANT]
> You are required to have installed **[Ollama](https://ollama.com/)**.
> Please refer to the official website for installation instructions.

* **Download** the latest [release](https://github.com/tomteipl/Ollama-GUI-Chat/releases/latest).
* **Extract** the archive.
* **Enjoy!**

>[!NOTE]
>*`custom_theme.json` is located inside of `_internal/theme` folder.*

## 💻 Customization

![OGC default colors photo](assets/Ollama_default_colors7.png)

You can customize the style of the app by editing `custom-theme.json`.
**OGC** searches for the `json` file in the `_internal/theme/` folder.

Part of the `custom-theme.json` file:

```json
{
  "CTk": {
    "fg_color": ["#5c549f", "#000"]
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

>[!TIP]
> Colors on the left are for **Light** theme, and on the right for **Dark** theme.

Its pretty easy and self-explanatory. Just change the values
and see the changes in the app.
You can use `HEX` colors or `names` like `"green"`.

Detailed usage of theme file can be found on
the official [CustomTkinter](https://customtkinter.tomschimansky.com/documentation/)
page.

If you wish you can modify `PATHs` to app and theme

```python
APP_PATH: str = os.path.dirname(os.path.realpath(__file__))
THEME_PATH: str = os.path.join(APP_PATH, "theme", "custom-theme.json")
```

## 🎨 Themes (WIP)

You can find more themes in **[themes](themes/)** folder.
Each theme has light and dark mode.

>[!TIP]
>Copy and paste whole code from any theme preset into `custom_theme.json`.

### Gruvbox

![Gruvbox Theme](assets/Ollama_gruvbox_2.png)

### Tokyo Night

![Tokyo Night Theme](assets/Ollama-tokyo_night_2.png)

## 📆 Roadmap

Start: **27.03.2025**

*Part 1:*

* [x] ~**Host URL input**, let user enter custom URL.~
* [x] ~**Autoscroll**~
* [x] ~**Load chat from file**~
* 📌 **Add stop button** (WIP)
* [x] ~**Add auto search for models**~
* [x] ~**Add progress bar**~
* **Improve UI**
* **Change theme handling**

## License

This project is under the [**GPL-3.0**](LICENSE) license.

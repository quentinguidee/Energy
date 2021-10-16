import webbrowser
import platform


def open_in_browser(filepath: str):
    if platform.system() == 'Darwin':
        filepath = 'file:///' + filepath

    webbrowser.open(filepath)

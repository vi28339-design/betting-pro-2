import os
import traceback


def _log(msg):
    for base in ("/storage/emulated/0/Documents/", "/sdcard/Documents/"):
        try:
            os.makedirs(base, exist_ok=True)
            p = os.path.join(base, "bettingpro_crash.txt")
            with open(p, "a") as f:
                f.write(msg + "\n")
            return
        except Exception:
            continue


_log("import: module top reached")

try:
    import toga
    _log("import: toga OK")
    from toga.style import Pack
    from toga.style.pack import COLUMN
    _log("import: styles OK")
except Exception:
    _log("import: EXCEPTION at import toga\n" + traceback.format_exc())
    raise


class BettingPro(toga.App):
    def startup(self):
        _log("startup: begin")
        try:
            main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment="center"))
            title = toga.Label("ТЕСТ УСПЕШЕН", style=Pack(font_size=24, font_weight="bold", margin_bottom=20))
            main_box.add(title)
            btn = toga.Button("Нажми меня", on_press=self.on_press, style=Pack(padding=10))
            main_box.add(btn)
            self.result = toga.Label("Ожидание нажатия...", style=Pack(font_size=16, margin_top=20))
            main_box.add(self.result)
            self.main_window = toga.MainWindow(title="Test App")
            self.main_window.content = main_box
            self.main_window.show()
            _log("startup: ok")
        except Exception:
            _log("startup: EXCEPTION\n" + traceback.format_exc())
            raise

    def on_press(self, widget):
        try:
            self.result.text = "Кнопка работает!"
        except Exception:
            _log("on_press: EXCEPTION\n" + traceback.format_exc())


def main():
    _log("main(): called")
    return BettingPro()

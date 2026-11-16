import os
import traceback

import toga
from toga.style import Pack
from toga.style.pack import COLUMN

CRASH_LOG = "crash.txt"


class BettingPro(toga.App):
    def startup(self):
        self._log("startup: begin")
        try:
            main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment="center"))

            title = toga.Label(
                "ТЕСТ УСПЕШЕН",
                style=Pack(font_size=24, font_weight="bold", margin_bottom=20),
            )
            main_box.add(title)

            btn = toga.Button("Нажми меня", on_press=self.on_press, style=Pack(padding=10))
            main_box.add(btn)

            self.result = toga.Label(
                "Ожидание нажатия...",
                style=Pack(font_size=16, margin_top=20),
            )
            main_box.add(self.result)

            self.main_window = toga.MainWindow(title="Test App")
            self.main_window.content = main_box
            self.main_window.show()
            self._log("startup: ok")
        except Exception:
            self._log("startup: EXCEPTION\n" + traceback.format_exc())
            raise

    def on_press(self, widget):
        try:
            self.result.text = "Кнопка работает!"
        except Exception:
            self._log("on_press: EXCEPTION\n" + traceback.format_exc())

    def _log(self, msg):
        try:
            path = os.path.join(str(self.paths.app), CRASH_LOG)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a") as f:
                f.write(msg + "\n")
        except Exception:
            pass


def main():
    return BettingPro()

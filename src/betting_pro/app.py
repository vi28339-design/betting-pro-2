import toga
from toga.style import Pack
from toga.style.pack import COLUMN


class BettingPro(toga.App):
    def startup(self):
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

    def on_press(self, widget):
        self.result.text = "Кнопка работает!"


def main():
    return BettingPro()

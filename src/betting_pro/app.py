import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from .model import predict_hockey, poisson_over, kelly_stake
from .database import db

class BettingPro(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        title = toga.Label("🏒 Betting PRO", style=Pack(font_size=24, font_weight="bold", margin_bottom=20))
        main_box.add(title)

        self.input_team1 = toga.TextInput(placeholder="К1: Забитые (напр. 5.2)", style=Pack(margin_bottom=10))
        self.input_team2 = toga.TextInput(placeholder="К2: Забитые (напр. 4.8)", style=Pack(margin_bottom=10))
        self.input_line = toga.TextInput(placeholder="Линия тотала (напр. 9.5)", style=Pack(margin_bottom=20))

        main_box.add(self.input_team1)
        main_box.add(self.input_team2)
        main_box.add(self.input_line)

        btn = toga.Button("Рассчитать прогноз", on_press=self.calculate, style=Pack(padding=10, margin_bottom=20))
        main_box.add(btn)

        self.result_label = toga.Label("", style=Pack(font_size=16, margin_top=10))
        main_box.add(self.result_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def calculate(self, widget):
        try:
            # Получаем значения и сразу защищаемся от пустых полей
            t1_str = self.input_team1.value or "0"
            t2_str = self.input_team2.value or "0"
            line_str = self.input_line.value or "0"
            
            t1 = float(t1_str)
            t2 = float(t2_str)
            line = float(line_str)

            if line <= 0:
                self.result_label.text = "Ошибка: линия должна быть больше 0!"
                return

            r = predict_hockey(t1, t2)
            p_over = poisson_over(r["total_exp"], line)
            p_under = 1 - p_over

            if p_over > 0.55:
                rec = f"ТБ {line} (вероятность {p_over*100:.1f}%)"
            elif p_under > 0.55:
                rec = f"ТМ {line} (вероятность {p_under*100:.1f}%)"
            else:
                rec = "Нет явного перевеса (пропуск)"

            self.result_label.text = f"Прогноз: {rec}\nОжидаемый тотал: {r['total_exp']:.2f}"
            
            db.save_prediction("Хоккей", "К1", "К2", line, rec)

        except ValueError:
            self.result_label.text = "Ошибка: введите корректные числа!"

def main():
    return BettingPro()

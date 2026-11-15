import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .model import predict_hockey, poisson_over, kelly_stake
from .database import db

class BettingPro(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Заголовок
        title = toga.Label("🏒 Betting PRO", style=Pack(font_size=24, font_weight="bold", margin_bottom=20))
        main_box.add(title)

        # Поля ввода
        self.input_team1 = toga.TextInput(placeholder="Команда 1 (забитые)", style=Pack(margin_bottom=5))
        self.input_team2 = toga.TextInput(placeholder="Команда 2 (забитые)", style=Pack(margin_bottom=5))
        self.input_line = toga.TextInput(placeholder="Линия тотала (например 9.5)", style=Pack(margin_bottom=15))

        main_box.add(self.input_team1)
        main_box.add(self.input_team2)
        main_box.add(self.input_line)

        # Кнопка
        btn = toga.Button("Рассчитать прогноз", on_press=self.calculate, style=Pack(padding=10, margin_bottom=20))
        main_box.add(btn)

        # Результат
        self.result_label = toga.Label("", style=Pack(font_size=16, margin_top=10))
        main_box.add(self.result_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def calculate(self, widget):
        try:
            t1 = float(self.input_team1.value or 0)
            t2 = float(self.input_team2.value or 0)
            line = float(self.input_line.value or 0)

            exp1 = t1
            exp2 = t2
            r = predict_hockey(exp1, exp2)
            p_ob = poisson_over(r["total_exp"], line)
            p_tm = 1 - p_ob

            if p_ob > 0.55:
                rec = f"ТБ {line} (вероятность {p_ob*100:.1f}%)"
            elif p_tm > 0.55:
                rec = f"ТМ {line} (вероятность {p_tm*100:.1f}%)"
            else:
                rec = "Нет явного перевеса (пропуск)"

            self.result_label.text = f"Прогноз: {rec}\nОжидаемый тотал: {r['total_exp']:.2f}"
            
            # Сохраняем в БД
            db.save_prediction("шорт-хоккей", "Команда 1", "Команда 2", line, rec)

        except ValueError:
            self.result_label.text = "Ошибка: введите числа!"

def main():
    return BettingPro()

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import traceback
import os
from .model import predict_hockey, poisson_over
from .database import DB

class BettingPro(toga.App):
    def startup(self):
        try:
            # ✅ Инициализируем БД с путями приложения
            self.db = DB(self.paths)

            main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            main_box.add(toga.Label("🏒 Betting PRO", style=Pack(font_size=24, font_weight="bold", margin_bottom=20)))

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

        except Exception as e:
            # ✅ Ловим ошибку и пишем в файл
            error_text = traceback.format_exc()
            path = os.path.join(self.paths.data, "crash_log.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(error_text)
            
            try:
                self.main_window = toga.MainWindow(title="Ошибка")
                self.main_window.content = toga.Label(f"Ошибка: смотрите crash_log.txt", style=Pack(padding=20))
                self.main_window.show()
            except Exception:
                pass

    def calculate(self, widget):
        try:
            t1 = float(self.input_team1.value or 0)
            t2 = float(self.input_team2.value or 0)
            line = float(self.input_line.value or 0)

            if line <= 0:
                self.result_label.text = "Ошибка: линия должна быть больше 0!"
                return

            r = predict_hockey(t1, t2)
            p_over = poisson_over(r["total_exp"], line)
            p_under = 1 - p_over

            if p_over > 0.55:
                rec = f"СТАВКА: ТБ {line}\nВероятность: {p_over*100:.1f}%"
            elif p_under > 0.55:
                rec = f"СТАВКА: ТМ {line}\nВероятность: {p_under*100:.1f}%"
            else:
                rec = "НЕТ СИГНАЛА (Пропустить)"

            self.result_label.text = f"{rec}\nОжидаемый тотал: {r['total_exp']:.2f}"
            self.db.save_prediction("Хоккей", "К1", "К2", line, rec)

        except ValueError:
            self.result_label.text = "Ошибка: введите числа!"

def main():
    return BettingPro()

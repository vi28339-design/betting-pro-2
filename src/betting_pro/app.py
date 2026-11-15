import traceback
import os

try:
    import toga
    from toga.style import Pack
    from toga.style.pack import COLUMN
except ImportError as e:
    # Если Toga не установлена, приложение упадет, но мы хотя бы попытаемся записать это
    print(f"Критическая ошибка: Toga не установлена. {e}")
    raise

from .model import predict_hockey, poisson_over
from .database import DB

class BettingPro(toga.App):
    def startup(self):
        try:
            # ✅ Инициализация БД с путями приложения
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

        except Exception:
            # ✅ Ловим ошибку и пишем в файл
            error_text = traceback.format_exc()
            # Пытаемся записать в доступную папку (Documents)
            try:
                path = os.path.join(self.paths.documents, "crash_log.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(error_text)
                error_msg = f"Ошибка: смотрите {path}"
            except Exception:
                error_msg = "Критическая ошибка при запуске."
            
            # Пытаемся показать окно с ошибкой
            try:
                self.main_window = toga.MainWindow(title="Ошибка")
                self.main_window.content = toga.Label(error_msg, style=Pack(padding=20))
                self.main_window.show()
            except Exception:
                pass

    def calculate(self, widget):
        try:
            # ✅ Безопасное получение чисел
            val1 = self.input_team1.value
            val2 = self.input_team2.value
            val_line = self.input_line.value

            t1 = float(val1) if val1 and str(val1).strip() else 0.0
            t2 = float(val2) if val2 and str(val2).strip() else 0.0
            line = float(val_line) if val_line and str(val_line).strip() else 0.0

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
            self.result_label.text = "Ошибка: введите корректные числа!"
        except Exception as e:
            self.result_label.text = f"Ошибка: {e}"

def main():
    return BettingPro()

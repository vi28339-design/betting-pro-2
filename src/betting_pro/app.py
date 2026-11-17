import os
import math
import traceback

import toga
from toga.style import Pack
from toga.style.pack import COLUMN


def poisson_pmf(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def predict_hockey(exp1, exp2, max_goals=15):
    if exp1 <= 0:
        exp1 = 0.1
    if exp2 <= 0:
        exp2 = 0.1
    p1 = px = p2 = 0.0
    for g1 in range(max_goals + 1):
        pg1 = poisson_pmf(g1, exp1)
        for g2 in range(max_goals + 1):
            p = pg1 * poisson_pmf(g2, exp2)
            if g1 > g2:
                p1 += p
            elif g1 == g2:
                px += p
            else:
                p2 += p
    return {"p1": p1, "px": px, "p2": p2, "total_exp": exp1 + exp2}


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


class BettingPro(toga.App):
    def startup(self):
        self._log("startup begin")
        try:
            self._build_ui()
            self._log("startup ok")
        except Exception:
            self._log("startup EXCEPTION\n" + traceback.format_exc())
            raise

    def _build_ui(self):
        root = toga.Box(style=Pack(direction=COLUMN, padding=24, background_color="#1a1a2e"))

        title = toga.Label(
            "Аналитика ставок",
            style=Pack(font_size=26, color="#ffffff", font_weight="bold", text_align="center", padding_bottom=12),
        )
        root.add(title)

        self.t1 = toga.TextInput(placeholder="Забитые К1 (напр. 5.2)", style=Pack(padding_bottom=8, height=44))
        self.t2 = toga.TextInput(placeholder="Забитые К2 (напр. 4.8)", style=Pack(padding_bottom=8, height=44))
        self.line = toga.TextInput(placeholder="Линия тотала (напр. 9.5)", style=Pack(padding_bottom=16, height=44))
        root.add(self.t1)
        root.add(self.t2)
        root.add(self.line)

        btn = toga.Button(
            "РАССЧИТАТЬ",
            on_press=self.on_calc,
            style=Pack(padding_bottom=16, height=48),
        )
        root.add(btn)

        self.result = toga.Label(
            "Ожидание данных...",
            style=Pack(color="#ffffff", font_size=18, text_align="center"),
        )
        root.add(self.result)

        self.main_window = toga.MainWindow(title="Betting PRO", size=(360, 640))
        self.main_window.content = root
        self.main_window.show()

    def on_calc(self, widget):
        try:
            v1 = self.t1.value.strip() or "0"
            v2 = self.t2.value.strip() or "0"
            vl = self.line.value.strip() or "0"
            exp1 = float(v1.replace(",", "."))
            exp2 = float(v2.replace(",", "."))
            line = float(vl.replace(",", "."))
            if line <= 0:
                self.result.text = "Ошибка: линия должна быть > 0"
                return
            r = predict_hockey(exp1, exp2)
            total = r["total_exp"]
            threshold = int(math.ceil(line))
            p_less = sum(poisson_pmf(k, total) for k in range(max(threshold, 1)))
            p_over = 1 - p_less
            p_under = 1 - p_over

            if p_over > 0.55:
                rec = "Ставка: ТБ {}".format(line)
                prob = p_over
            elif p_under > 0.55:
                rec = "Ставка: ТМ {}".format(line)
                prob = p_under
            else:
                rec = "Нет сигнала — пропустить"
                prob = max(p_over, p_under)

            self.result.text = "{}\nВероятность: {:.1f}%\n\nП1: {:.0f}%  X: {:.0f}%  П2: {:.0f}%\nОжидаемый тотал: {:.2f}".format(
                rec, prob * 100, r["p1"] * 100, r["px"] * 100, r["p2"] * 100, total
            )
        except Exception:
            self.result.text = "Ошибка ввода! Введите числа."
            self._log("calc EXCEPTION\n" + traceback.format_exc())

    def _log(self, msg):
        _log(msg)


def main():
    return BettingPro()

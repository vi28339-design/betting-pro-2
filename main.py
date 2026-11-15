from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from model import predict_hockey, poisson_over, kelly_stake
from database import db

Window.clearcolor = (0.06, 0.09, 0.16, 1)

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)
        
        self.add_widget(Label(text="Betting PRO", font_size=32, color=(1,1,1,1), size_hint_y=None, height=50))
        self.add_widget(Label(text="Введите данные для прогноза", color=(0.7,0.7,0.7,1), size_hint_y=None, height=30))

        self.t1 = TextInput(hint_text="Забитые К1 (например 5.2)", multiline=False, size_hint_y=None, height=50)
        self.t2 = TextInput(hint_text="Забитые К2 (например 4.8)", multiline=False, size_hint_y=None, height=50)
        self.line = TextInput(hint_text="Линия (например 9.5)", multiline=False, size_hint_y=None, height=50)
        
        self.add_widget(self.t1)
        self.add_widget(self.t2)
        self.add_widget(self.line)

        btn = Button(text="Рассчитать", size_hint_y=None, height=60, background_color=(0.2,0.5,0.9,1))
        btn.bind(on_press=self.calculate)
        self.add_widget(btn)

        self.result = Label(text="", font_size=18, color=(1,1,1,1), halign="center", valign="middle")
        self.result.bind(size=self.result.setter('text_size'))
        self.add_widget(self.result)

    def calculate(self, instance):
        try:
            t1 = float(self.t1.text)
            t2 = float(self.t2.text)
            line = float(self.line.text)
            
            r = predict_hockey(t1, t2)
            p_over = poisson_over(r["total_exp"], line)
            p_under = 1 - p_over

            if p_over > 0.55:
                rec = f"СТАВКА: ТБ {line}\nВероятность: {p_over*100:.1f}%"
            elif p_under > 0.55:
                rec = f"СТАВКА: ТМ {line}\nВероятность: {p_under*100:.1f}%"
            else:
                rec = "НЕТ СИГНАЛА (Пропустить)"

            self.result.text = f"{rec}\nОжидаемый тотал: {r['total_exp']:.2f}"
            db.save_prediction("Хоккей", "К1", "К2", line, rec)
            
        except ValueError:
            self.result.text = "Ошибка: введите числа!"

class BettingApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    BettingApp().run()

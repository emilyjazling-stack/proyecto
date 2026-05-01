import sqlite3
import os

# Optimización para gráficas AMD Radeon (como la tuya 660M)
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar

# Proporción de pantalla de móvil
Window.size = (360, 640)

def init_db():
    conn = sqlite3.connect('tequix_aprende.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY, user TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# --- DISEÑO KV CORREGIDO ---
KV = '''
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

<LessonItem>:
    padding: "15dp"
    size_hint_y: None
    height: "90dp"
    radius: [20,]
    elevation: 2
    md_bg_color: (0.9, 0.9, 0.9, 1) if self.is_locked else (1, 1, 1, 1)
    on_release: if not self.is_locked: app.open_quiz(self.lesson_index)

    MDRelativeLayout:
        MDLabel:
            text: root.text
            pos_hint: {"center_y": .5, "x": .05}
            theme_text_color: "Hint" if root.is_locked else "Primary"
            font_style: "Subtitle1"
            bold: True
        MDIcon:
            icon: "lock-outline" if root.is_locked else "chevron-right"
            pos_hint: {"center_y": .5, "right": .95}
            theme_text_color: "Custom"
            text_color: (0.6, 0.6, 0.6, 1) if root.is_locked else (0.1, 0.5, 0.3, 1)

ScreenManager:
    transition: SlideTransition(direction="left")
    LoginScreen:
    RegisterScreen:
    HomeScreen:
    LessonMenuScreen:
    QuizScreen:

<LoginScreen>:
    name: 'login'
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDFloatLayout:
            size_hint: None, None
            size: "600dp", "600dp"
            pos_hint: {"center_x": .5, "center_y": 1.1}
            canvas:
                Color:
                    rgba: (0.1, 0.5, 0.3, 1)
                Ellipse:
                    size: self.size
                    pos: self.pos
        MDLabel:
            text: "TequixAprende"
            font_style: "H4"
            pos_hint: {"center_y": .8}
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            bold: True
        MDCard:
            size_hint: .85, .5
            pos_hint: {"center_x": .5, "center_y": .45}
            padding: "25dp"
            spacing: "15dp"
            orientation: "vertical"
            radius: [30,]
            elevation: 4
            MDLabel:
                text: "Bienvenido"
                font_style: "H5"
                halign: "center"
                bold: True
            MDTextField:
                id: user
                hint_text: "Usuario"
                icon_right: "account"
                mode: "rectangle"
            MDTextField:
                id: password
                hint_text: "Contraseña"
                icon_right: "key"
                password: True
                mode: "rectangle"
            MDFillRoundFlatButton:
                text: "INICIAR SESIÓN"
                size_hint_x: 1
                on_release: root.login_user()
            MDFlatButton:
                text: "¿No tienes cuenta? Regístrate"
                pos_hint: {"center_x": .5}
                on_release: root.manager.current = 'register'

<RegisterScreen>:
    name: 'register'
    MDFloatLayout:
        md_bg_color: 0.95, 0.95, 0.95, 1
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"top": 1, "left": 1}
            on_release: root.manager.current = 'login'
        MDLabel:
            text: "Crear Cuenta"
            font_style: "H4"
            halign: "center"
            pos_hint: {"center_y": .85}
            bold: True
        MDCard:
            size_hint: .85, .5
            pos_hint: {"center_x": .5, "center_y": .5}
            padding: "25dp"
            spacing: "15dp"
            orientation: "vertical"
            radius: [30,]
            MDTextField:
                id: new_user
                hint_text: "Nuevo Usuario"
                mode: "rectangle"
            MDTextField:
                id: new_password
                hint_text: "Contraseña"
                password: True
                mode: "rectangle"
            MDFillRoundFlatButton:
                text: "REGISTRARME"
                size_hint_x: 1
                on_release: root.register_user()

<HomeScreen>:
    name: 'home'
    MDFloatLayout:
        md_bg_color: 0.98, 0.98, 0.98, 1
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: .25
            pos_hint: {"top": 1}
            padding: "20dp"
            md_bg_color: 0.1, 0.5, 0.3, 1
            radius: [0, 0, 40, 40]
            MDLabel:
                text: "¡Hola, Estudiante!"
                font_style: "H5"
                text_color: 1, 1, 1, 1
                theme_text_color: "Custom"
            MDLabel:
                text: "Continúa con tus cursos de hoy"
                font_style: "Caption"
                text_color: 0.9, 0.9, 0.9, 1
                theme_text_color: "Custom"
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: .7
            padding: "20dp"
            spacing: "20dp"
            MDCard:
                padding: "20dp"
                radius: [25,]
                elevation: 3
                orientation: "vertical"
                on_release: app.go_to_lessons("agronomia")
                MDLabel:
                    text: "Agronomía 🌿"
                    font_style: "H6"
                    bold: True
                MDProgressBar:
                    value: app.prog_agro
                    color: 0.1, 0.5, 0.3, 1
                MDLabel:
                    text: f"Progreso: {int(app.prog_agro)}%"
                    font_style: "Caption"
            MDCard:
                padding: "20dp"
                radius: [25,]
                elevation: 3
                orientation: "vertical"
                on_release: app.go_to_lessons("ingles")
                MDLabel:
                    text: "Inglés 💬"
                    font_style: "H6"
                    bold: True
                MDProgressBar:
                    value: app.prog_ingles
                    color: 0.1, 0.4, 0.6, 1
                MDLabel:
                    text: f"Progreso: {int(app.prog_ingles)}%"
                    font_style: "Caption"

<LessonMenuScreen>:
    name: 'lessons'
    MDFloatLayout:
        md_bg_color: 0.95, 0.97, 0.95, 1
        MDLabel:
            text: "Plan de Estudios"
            font_style: "H5"
            pos_hint: {"center_y": .92}
            halign: "center"
            bold: True
        MDScrollView:
            size_hint_y: .82
            MDBoxLayout:
                id: lesson_list
                orientation: "vertical"
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"
        MDIconButton:
            icon: "chevron-left"
            pos_hint: {"top": 1, "left": 1}
            on_release: 
                root.manager.transition.direction = "right"
                root.manager.current = 'home'

<QuizScreen>:
    name: 'quiz'
    MDFloatLayout:
        MDCard:
            size_hint: .9, .8
            pos_hint: {"center_x": .5, "center_y": .5}
            radius: [30,]
            padding: "20dp"
            orientation: "vertical"
            MDLabel:
                id: q_label
                text: ""
                halign: "center"
                font_style: "H6"
                size_hint_y: .3
            MDBoxLayout:
                orientation: "vertical"
                spacing: "15dp"
                padding: "10dp"
                MDRaisedButton:
                    id: b1
                    size_hint_x: 1
                    on_release: root.answer(self.text)
                MDRaisedButton:
                    id: b2
                    size_hint_x: 1
                    on_release: root.answer(self.text)
                MDRaisedButton:
                    id: b3
                    size_hint_x: 1
                    on_release: root.answer(self.text)
'''

# --- LÓGICA PYTHON ---
class LessonItem(MDCard):
    text = StringProperty("")
    is_locked = BooleanProperty(True)
    lesson_index = NumericProperty(0)

class LoginScreen(Screen):
    def login_user(self):
        user = self.ids.user.text
        password = self.ids.password.text
        conn = sqlite3.connect('tequix_aprende.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE user=? AND password=?", (user, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.manager.current = 'home'
        else:
            Snackbar(text="Usuario o contraseña incorrectos").open()

class RegisterScreen(Screen):
    def register_user(self):
        user = self.ids.new_user.text
        pwd = self.ids.new_password.text
        if user and pwd:
            try:
                conn = sqlite3.connect('tequix_aprende.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (user, password) VALUES (?, ?)", (user, pwd))
                conn.commit()
                conn.close()
                Snackbar(text="Cuenta creada. ¡Inicia sesión!").open()
                self.manager.current = 'login'
            except:
                Snackbar(text="El usuario ya existe").open()

class HomeScreen(Screen):
    pass

class LessonMenuScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids.lesson_list.clear_widgets()
        course = app.current_course
        passed = app.agro_passed if course == "agronomia" else app.ingles_passed
        data = app.course_data[course]
        for i in range(5):
            locked = i > passed
            item = LessonItem(
                text=f"L{i+1}: {data[i]['name']}",
                is_locked=locked,
                lesson_index=i
            )
            self.ids.lesson_list.add_widget(item)

class QuizScreen(Screen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        self.questions = app.course_data[app.current_course][app.current_lesson]["questions"]
        self.idx = 0
        self.correct = 0
        self.update_q()
    def update_q(self):
        if self.idx < len(self.questions):
            q = self.questions[self.idx]
            self.ids.q_label.text = q["p"]
            opts = q["o"]
            self.ids.b1.text = opts[0]
            self.ids.b2.text = opts[1]
            self.ids.b3.text = opts[2]
        else:
            self.show_result()
    def answer(self, text):
        if text == self.questions[self.idx]["r"]:
            self.correct += 1
        self.idx += 1
        self.update_q()
    def show_result(self):
        score = (self.correct / len(self.questions)) * 100
        app = MDApp.get_running_app()
        if score >= 80:
            msg = f"¡Felicidades! {score:.0f}/100."
            if app.current_course == "agronomia" and app.current_lesson == app.agro_passed:
                app.agro_passed += 1
            elif app.current_course == "ingles" and app.current_lesson == app.ingles_passed:
                app.ingles_passed += 1
        else:
            msg = f"Puntaje: {score:.0f}/100. Necesitas 80."
        self.dialog = MDDialog(
            title="Resultado",
            text=msg,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.close_dialog())]
        )
        self.dialog.open()
    def close_dialog(self):
        self.dialog.dismiss()
        self.manager.current = 'lessons'

class TequixApp(MDApp):
    prog_agro = NumericProperty(0)
    prog_ingles = NumericProperty(0)
    agro_passed = NumericProperty(0)
    ingles_passed = NumericProperty(0)
    current_course = StringProperty("")
    current_lesson = NumericProperty(0)

    course_data = {
        "agronomia": [
            {"name": "Suelo", "questions": [{"p": "¿Base de la vida vegetal?", "o": ["Suelo", "Arena", "Plástico"], "r": "Suelo"}]},
            {"name": "Riego", "questions": [{"p": "¿Más eficiente?", "o": ["Goteo", "Manguera", "Lluvia"], "r": "Goteo"}]},
            {"name": "NPK", "questions": [{"p": "¿Qué es la N?", "o": ["Nitrógeno", "Níquel", "Sodio"], "r": "Nitrógeno"}]},
            {"name": "Control", "questions": [{"p": "Uso de insectos es...", "o": ["Biológico", "Químico", "Nulo"], "r": "Biológico"}]},
            {"name": "Cosecha", "questions": [{"p": "¿Cuándo?", "o": ["Madurez", "Lunes", "Mañana"], "r": "Madurez"}]}
        ],
        "ingles": [
            {"name": "Greetings", "questions": [{"p": "'Hello' es:", "o": ["Hola", "Adiós", "Gracias"], "r": "Hola"}]},
            {"name": "To Be", "questions": [{"p": "I ___ student:", "o": ["am", "is", "are"], "r": "am"}]},
            {"name": "Objects", "questions": [{"p": "Manzana es:", "o": ["Apple", "Orange", "Grape"], "r": "Apple"}]},
            {"name": "Past", "questions": [{"p": "Past of 'See':", "o": ["Saw", "Seed", "Seen"], "r": "Saw"}]},
            {"name": "Verbs", "questions": [{"p": "I like ___:", "o": ["dancing", "dance", "danced"], "r": "dancing"}]}
        ]
    }

    def on_agro_passed(self, instance, value):
        self.prog_agro = (value / 5) * 100
    def on_ingles_passed(self, instance, value):
        self.prog_ingles = (value / 5) * 100

    def build(self):
        init_db()
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def go_to_lessons(self, course):
        self.current_course = course
        self.root.transition.direction = "left"
        self.root.current = 'lessons'

    def open_quiz(self, index):
        self.current_lesson = index
        self.root.current = 'quiz'

if __name__ == '__main__':
    TequixApp().run()
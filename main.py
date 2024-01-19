from kivymd.app import MDApp
from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.storage.jsonstore import JsonStore
from random import randint
from PIL import Image, ImageDraw, ImageFont
import textwrap, json


Window.size = (360, 640)


class Button2(MDFillRoundFlatButton):
    pass

class Button3(Button2):
    pass

class Dicas(MDScreen):
    pass        

class DesafiosProgresso(MDScreen):
    def on_pre_enter(self):
        store_desafios = JsonStore('desafios.json')
        l = len(store_desafios['desafios'])
        with open('concluidos.json', 'r') as f:
            concluidos = json.load(f)
        for i in range(0, l):
            if i in concluidos:
                button = Button3(id=str(i),text=str(i+1))
                button.bind(on_release=App.get_running_app().concluido)
            else:
                button = Button2(id=str(i),text=str(i+1))
                button.bind(on_release=App.get_running_app().desafio)
            self.ids.desafios.add_widget(button)

class DesafioExplicacao(MDScreen):
    pass    

class DesafioConcluido(MDScreen):
    pass

class Dailygreen(MDApp):
    n = NumericProperty()
    dica = StringProperty()
    titulo = StringProperty()
    descricao = StringProperty()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = "Brown"
        sm = MDScreenManager()
        sm.add_widget(Dicas(name='dicas'))
        sm.add_widget(DesafiosProgresso(name='progresso'))
        sm.add_widget(DesafioExplicacao(name='explicacao'))
        sm.add_widget(DesafioConcluido(name='concluido'))

        return sm
    
    def on_start(self):
        store_dicas = JsonStore('dicas.json')
        l = len(store_dicas['dicas'])
        rn = randint(0,l)
        valor_dicas = store_dicas['dicas'][rn]
        App.get_running_app().dica = valor_dicas['descricao']

    def concluido(self, instance):
        self.root.current = 'concluido'
        App.get_running_app().n = int(instance.text)-1
        store_desafios = JsonStore('desafios.json')
        valor_desafios = store_desafios['desafios'][App.get_running_app().n]
        App.get_running_app().titulo = valor_desafios['titulo']
        App.get_running_app().descricao = valor_desafios['descricao']

    def desafio(self, instance):
        self.root.current = 'explicacao'
        App.get_running_app().n = int(instance.text)-1
        store_desafios = JsonStore('desafios.json')
        valor_desafios = store_desafios['desafios'][App.get_running_app().n]
        App.get_running_app().titulo = valor_desafios['titulo']
        App.get_running_app().descricao = valor_desafios['descricao']
    
    def compartilhar(self, title, rawextra, rawtext):
        input_image = Image.open('images/input_image.jpeg')
        draw = ImageDraw.Draw(input_image)

        title_position = (500, 675)
        title_color = (115, 92, 69)
        title_font = ImageFont.truetype(font='fonts/karlaextrabold.ttf', size=80)

        extra_list = textwrap.wrap(rawextra, 15)
        extra = '\n'.join(extra_list)
        extra_position = (500, 900)
        extra_color = (151, 189, 112)
        extra_font = ImageFont.truetype(font='fonts/karlaextrabold.ttf', size=90)

        text_list = textwrap.wrap(rawtext, 25)
        text = '\n'.join(text_list)
        text_position = (500, 1250)
        text_color = (115, 92, 69)
        text_font = ImageFont.truetype(font='fonts/karlabold.ttf', size=60)

        draw.text(title_position, title, fill=title_color, anchor="mm", font=title_font)
        draw.multiline_text(extra_position, extra, fill=extra_color, anchor="mm", font=extra_font, align='center')
        draw.multiline_text(text_position, text, fill=text_color, anchor="mm", font=text_font, align='center')
        input_image.save('images/output_image.jpg')
        input_image.close()
        App.get_running_app().gotoprogresso()

    def concluir(self):
        App.get_running_app().gotoconcluido()
        with open('concluidos.json', 'r') as f:
            concluidos = json.load(f)
        if App.get_running_app().n not in concluidos:
            concluidos.append(App.get_running_app().n)
        concluidos.sort()
        with open('concluidos.json', 'w') as f:
            json.dump(concluidos, f)

    def gotoprogresso(self):
        self.root.current = 'progresso'

    def gotoexplicacao(self):
        self.root.current = 'explicacao'
    
    def gotodicas(self):
        self.root.current = 'dicas'

    def gotoconcluido(self):
        self.root.current = 'concluido'

if __name__ == '__main__':
    Dailygreen().run()
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

# Indiciando dois tipos de botões com base em MDFillRoundFlatButton
class Button2(MDFillRoundFlatButton):
    pass

class Button3(Button2):
    pass

# Indiciando as telas
class Dicas(MDScreen):
    pass        

class DesafiosProgresso(MDScreen):
    def on_pre_enter(self):
        # Carregando dados dos desafios e desafios concluídos
        store_desafios = App.get_running_app().open_json('desafios.json')
        l = len(store_desafios['desafios'])
        concluidos = App.get_running_app().open_json('concluidos.json')
        self.ids.desafios.clear_widgets()
        # Iterando sobre os desafios e adicionando botões de acordo com o status de conclusão
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
        # Configuração inicial do aplicativo
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = "Brown"
        # Configurando o gerenciador de tela e adicionando as telas
        sm = MDScreenManager()
        sm.add_widget(Dicas(name='dicas'))
        sm.add_widget(DesafiosProgresso(name='progresso'))
        sm.add_widget(DesafioExplicacao(name='explicacao'))
        sm.add_widget(DesafioConcluido(name='concluido'))

        return sm
    
    def on_start(self):
        # Carregando uma dica aleatória no início do aplicativo
        store_dicas = App.get_running_app().open_json('dicas.json')
        l = len(store_dicas['dicas'])
        rn = randint(0,l)
        valor_dicas = store_dicas['dicas'][rn]
        App.get_running_app().dica = valor_dicas['descricao']

    def concluido(self, instance):
        # Navegando para a tela de desafio concluído e carregando informações do desafio
        self.root.current = 'concluido'
        App.get_running_app().n = int(instance.text)-1
        store_desafios = App.get_running_app().open_json('desafios.json')
        valor_desafios = store_desafios['desafios'][App.get_running_app().n]
        App.get_running_app().titulo = valor_desafios['titulo']
        App.get_running_app().descricao = valor_desafios['descricao']

    def desafio(self, instance):
        # Navegando para a tela de explicação do desafio e carregando informações do desafio
        self.root.current = 'explicacao'
        App.get_running_app().n = int(instance.text)-1
        store_desafios = App.get_running_app().open_json('desafios.json')
        valor_desafios = store_desafios['desafios'][App.get_running_app().n]
        App.get_running_app().titulo = valor_desafios['titulo']
        App.get_running_app().descricao = valor_desafios['descricao']
    
    def compartilhar(self, title, rawextra, rawtext):
        # Criando uma imagem com informações do desafio para compartilhamento
        # (Nota: Este trecho de código depende do sistema operacional Android)
        input_image = Image.open('input_image.jpeg')
        draw = ImageDraw.Draw(input_image)

        # Configurando posições, cores e fontes para o texto na imagem
        title_position = (500, 675)
        title_color = (115, 92, 69)
        title_font = ImageFont.truetype(font='karlaextrabold.ttf', size=80)

        extra_list = textwrap.wrap(rawextra, 15)
        extra = '\n'.join(extra_list)
        extra_position = (500, 900)
        extra_color = (151, 189, 112)
        extra_font = ImageFont.truetype(font='karlaextrabold.ttf', size=90)

        text_list = textwrap.wrap(rawtext, 25)
        text = '\n'.join(text_list)
        text_position = (500, 1250)
        text_color = (115, 92, 69)
        text_font = ImageFont.truetype(font='karlabold.ttf', size=60)

        # Adicionando texto à imagem
        draw.text(title_position, title, fill=title_color, anchor="mm", font=title_font)
        draw.multiline_text(extra_position, extra, fill=extra_color, anchor="mm", font=extra_font, align='center')
        draw.multiline_text(text_position, text, fill=text_color, anchor="mm", font=text_font, align='center')
        # Salvando e fechando a imagem
        input_image.save('output_image.jpg')
        input_image.close()

        '''# Compartilhando a imagem (Android)
        from kivy import platform

        if platform == 'android':
            from jnius import autoclass
            from jnius import cast
            
            # Desabilitando verificações de exposição de URI de arquivo
            StrictMode = autoclass('android.os.StrictMode')
            StrictMode.disableDeathOnFileUriExposure()
            
            # Importando classes necessárias para o compartilhamento
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')

            # Criando um Intent para compartilhamento
            shareIntent = Intent(Intent.ACTION_SEND)
            shareIntent.setType('"image/*"')

            imageFile = File('output_image.png')
            uri = Uri.fromFile(imageFile)
            parcelable = cast('android.os.Parcelable', uri)
            shareIntent.putExtra(Intent.EXTRA_STREAM, parcelable)

            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(shareIntent)
            '''

        App.get_running_app().gotoprogresso()

    def concluir(self):
        # Navegando para a tela de desafio concluído e atualizando a lista de desafios concluídos
        App.get_running_app().gotoconcluido()
        concluidos = App.get_running_app().open_json('concluidos.json')
        if App.get_running_app().n not in concluidos:
            concluidos.append(App.get_running_app().n)
        concluidos.sort()
        with open('concluidos.json', 'w', encoding="utf8") as f:
            json.dump(concluidos, f)

    def open_json(self, json_filename):
        # Função para abrir e carregar um arquivo JSON para leitura
        with open(json_filename, 'r', encoding="utf8") as f:
            return json.load(f)

    def gotoprogresso(self):
        # Navegando para a tela de progresso
        self.root.current = 'progresso'

    def gotoexplicacao(self):
        # Navegando para a tela de explicação do desafio
        self.root.current = 'explicacao'
    
    def gotodicas(self):
        # Navegando para a tela de dicas
        self.root.current = 'dicas'

    def gotoconcluido(self):
        # Navegando para a tela de desafio concluído
        self.root.current = 'concluido'

if __name__ == '__main__':
    # Inicializando e executando o aplicativo
    Dailygreen().run()
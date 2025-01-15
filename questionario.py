import flet as ft
from flet import Colors
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from datetime import datetime 

# Configuração do Firebase
firebase_key = json.loads(os.environ['FIREBASE_KEY'])
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)
db = firestore.client()

def main(page: ft.Page):
    page.title = "Questionário de Bem-Estar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Função para enviar respostas para o Firestore
    def enviar_respostas(e):
        respostas = {
            "trabalho": esc_trabalho.value,
            "sono": esc_sono.value,
            "dor": esc_dor.value,
            "local_dor": campo_dor.value,
            "dormencia": esc_dormencia.value,
            "local_dormencia": campo_dormencia.value,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Inserir dados no Firestore
        db.collection("respostas").add(respostas)

        page.snack_bar = ft.SnackBar(content=ft.Text("Respostas enviadas com sucesso!"))
        page.snack_bar.open = True
        page.update()
        print(respostas)

    # Introdução
    introducao = ft.Column([
        ft.Text("Bem-vindo ao questionário de bem-estar!", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Responda as perguntas abaixo com base no seu dia de ontem."),
        ft.ElevatedButton("Iniciar", on_click=lambda e: exibir_perguntas())
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Função para definir cores do slider dinamicamente
    def define_cor_slider(valor):
        if valor <= 3:
            return Colors.GREEN
        elif valor <= 6:
            return Colors.YELLOW
        elif valor <= 8:
            return Colors.ORANGE
        else:
            return Colors.RED

    # Atualiza cor do slider dinamicamente
    def atualizar_cor_slider(e):
        e.control.thumb_color = define_cor_slider(e.control.value)
        e.control.update()

    # Perguntas com escala e campos de texto
    esc_trabalho = ft.Slider(min=0, max=10, divisions=10, label="{value}",
                             thumb_color=Colors.BLUE,
                             on_change=atualizar_cor_slider)
    
    esc_sono = ft.Slider(min=0, max=10, divisions=10, label="{value}",
                         thumb_color=Colors.BLUE,
                         on_change=atualizar_cor_slider)
    
    esc_dor = ft.Slider(min=0, max=10, divisions=10, label="{value}",
                        thumb_color=Colors.BLUE,
                        on_change=atualizar_cor_slider)
    
    esc_dormencia = ft.Slider(min=0, max=10, divisions=10, label="{value}",
                              thumb_color=Colors.BLUE,
                              on_change=atualizar_cor_slider)

    campo_dor = ft.TextField(label="Onde você sentiu dor?")
    campo_dormencia = ft.TextField(label="Onde você sentiu dormência?")

    perguntas = ft.Column([
        ft.Text("1. O quanto foi estressante o seu trabalho ontem?", size=18),
        esc_trabalho,
        ft.Text("2. O quão bem você dormiu ontem?", size=18),
        esc_sono,
        ft.Text("3. O quanto você sentiu de dor ontem?", size=18),
        esc_dor,
        campo_dor,
        ft.Text("4. Você sentiu dormência hoje?", size=18),
        esc_dormencia,
        campo_dormencia,
        ft.ElevatedButton("Enviar", on_click=enviar_respostas)
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Controla a troca de telas
    def exibir_perguntas():
        page.clean()
        page.add(perguntas)

    # Exibir introdução na tela inicial
    page.add(introducao)

ft.app(target=main, view=ft.WEB_BROWSER)

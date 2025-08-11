import customtkinter as ctk

# configurando a aparência

ctk.set_appearance_mode('light')

# criando a janela principal
app = ctk.CTk()
app.title('Jokenpô')
app.geometry('300x300')

# criando os campos

campo_instrucao = ctk.CTkLabel(app,text='Escolha uma das opções')

#define o espaçamento do campo
campo_instrucao.pack(pady=10)

#criando botões 
botao_pedra = ctk.CTkButton(app,text='Pedra')
botao_papel = ctk.CTkButton(app,text='Papel')
botao_tesoura = ctk.CTkButton(app,text='Tesoura')


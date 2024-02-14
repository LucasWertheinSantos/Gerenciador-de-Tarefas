import os
import sys
import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as msg
from pathlib import Path

from main import Prioridade, Status, dicionarioPrioridade, dicionarioStatus
from tarefa import Tarefa


def assets(path: str, frame: str) -> Path:
    path = Path("assets") / Path(frame) / Path(path)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)


def relative_to_assets(path: str, frame: str) -> Path:
    return assets(path, frame)


# Criando a janela
window = tk.Tk()

# Configurando a janela
window.title("Minha Agenda - v1.0")
width = 1060
height = 640
window.geometry("%dx%d+0+0" % (width, height))
window.configure(bg="#FFFFFF")
window.resizable(False, False)

# Telas
frame = tk.Frame(window)
frame_inicio = tk.Frame(window)
frame_new = tk.Frame(window)
frame_tasks = tk.Frame(window)


# Classe para armazenar informações da tela
class screenInfo:
    def __init__(self):
        self.screen = 0
        self.taskType = Status.CONCLUIDA
        self.taskSelected = (-1, self.taskType)
        self.scroll = 0


info = screenInfo()


# Trocando de telas
def startScreen():
    info.screen = 0
    frame.place_forget()
    frame_new.place_forget()
    frame_tasks.place_forget()
    frame_inicio.place(x=0, y=0, width=width, height=height)


def break_text_by_length(text, font: tkfont, task_width):
    words = text.split()
    lines = []
    current_line = ""

    espaco_restante = task_width - 10
    for word in words:
        if font.measure(word) < espaco_restante:
            current_line += word + " "
            espaco_restante -= font.measure(word) + font.measure(" ")
        else:
            lines.append(current_line.rstrip())
            current_line = word + " "
            espaco_restante = task_width - 10 - font.measure(word) - font.measure(" ")

    if current_line:
        lines.append(current_line.rstrip())

    return "\n".join(lines)


canvas_tasks = tk.Canvas(
    frame_tasks,
    bg="#FFFFFF",
    height=height,
    width=0.73 * width,
    bd=1.75,
    highlightthickness=0,
    relief="ridge",
)
canvas_tasks.place(x=14, y=0)


def drawTasks(agenda):
    wid = 0.73 * width
    hei = height

    taskWid = 0.2 * width
    taskHei = 0.3 * height

    offset_x = 20
    offset_y = 20
    space_between_tasks = 30
    max_tasks_per_row = 1

    tasks_lists = [
        agenda.tarefas_para_executar,
        agenda.tarefas_executando,
        agenda.tarefas_concluidas,
    ]
    canvas_tasks.create_rectangle(0, 0, 0.73 * width, height, fill="#FFFFFF")

    for j, task_list in enumerate(tasks_lists):
        # Calcular a posição de cada tarefa na tela
        for i, task in enumerate(task_list):
            row = i // max_tasks_per_row
            col = j
            x = offset_x + col * (taskWid + space_between_tasks)
            y = info.scroll * 10 + offset_y + row * (taskHei + space_between_tasks / 2)

            # Desenhar o retangula de cada tarefa
            color = "lightblue"
            if j == info.taskSelected[1]:
                if i == info.taskSelected[0]:
                    color = "white"
            status_cor = "red"
            if j == 1:
                status_cor = "yellow"
            elif j == 2:
                status_cor = "green"

            canvas_tasks.create_rectangle(
                x, y, x + taskWid, y + taskHei, fill=color, outline="black"
            )
            canvas_tasks.create_rectangle(
                x,
                y + taskHei,
                x + taskWid,
                y + taskHei + 10,
                fill=status_cor,
                outline="black",
            )

            # Desenhar as informações das tarefas
            prioridade = "Nenhuma"
            if task.prioridade != None:
                prioridade = task.prioridade.name
            font = tkfont.Font(family="Calibri", weight="normal", size=12)

            text = f"{break_text_by_length('NOME: '+ task.nome, font, taskWid)}\n"
            text += f"DATA: {task.data_hora.strftime('%d/%m/%Y')}\n"
            text += f"HORÁRIO: {task.data_hora.strftime('%H:%M')}\n"
            text += f"PRIORIDADE: {prioridade[:1].upper() + prioridade[1:].lower()}\n"
            text += f"CATEGORIA: {task.categoria}\n"
            text += (
                f"{break_text_by_length('DESCRIÇÃO: ' + task.descricao, font, taskWid)}"
            )
            canvas_tasks.create_text(
                x + 10, y + 10, anchor="nw", text=text, font=("Calibri", 12)
            )


def fecharJanela():
    window.destroy()


def mainScreen():
    resetData()
    info.screen = 1
    frame_inicio.place_forget()
    frame_new.place_forget()
    frame.place(x=0, y=0, width=width, height=height)
    frame_tasks.place(
        x=0.24 * width, y=0.105 * height, width=0.75 * width, height=height
    )


def novaTarefaScreen():
    info.screen = 2
    frame_inicio.place_forget()
    frame.place_forget()
    frame_tasks.place_forget()
    frame_new.place(x=0, y=0, width=width, height=height)


def click():
    if info.screen == 0:
        mainScreen()


def deleteTask(agenda):
    if info.taskSelected[0] != -1:
        agenda.excluir_tarefa(info.taskSelected[0], info.taskSelected[1])

    info.taskSelected = (-1, info.taskType)
    drawTasks(agenda)


def scrollTasks(scroll, agenda):
    if info.scroll + scroll <= 0:
        info.scroll += scroll
        drawTasks(agenda)


def resetData():
    for i in range(5):
        telaNewTask.entries[i].delete(0, tk.END)
    telaNewTask.setStatus(None)
    telaNewTask.setPrioridade(None)


def editTask(agenda):
    if info.taskSelected[0] != -1:
        telaNewTask.editing = True
        telaNewTask.editingIndex = info.taskSelected[0]
        telaNewTask.editingStatus = info.taskSelected[1]
        task = agenda.pegar_tarefa(info.taskSelected[0], info.taskSelected[1])

        # Resetando os valores das caixas de texto
        resetData()

        # Preenchendo as caixas de texto com os valores da tarefa que esta sendo editada
        telaNewTask.entries[0].insert(0, task.nome)
        telaNewTask.entries[1].insert(0, task.data_hora.strftime("%d/%m/%Y"))
        telaNewTask.entries[2].insert(0, task.data_hora.strftime("%H:%M"))
        telaNewTask.entries[3].insert(0, task.descricao)
        telaNewTask.entries[4].insert(0, task.categoria)

        telaNewTask.setStatus(dicionarioStatus.get(info.taskSelected[1]))
        telaNewTask.setPrioridade(dicionarioPrioridade.get(task.prioridade.value - 1))

        novaTarefaScreen()


def selectTask(event, agenda):
    wid = 0.73 * width
    hei = height

    taskWid = 0.2 * width
    taskHei = 0.3 * height

    offset_x = 20
    offset_y = 20
    space_between_tasks = 30
    max_tasks_per_row = 1

    tasks_lists = [
        agenda.tarefas_para_executar,
        agenda.tarefas_executando,
        agenda.tarefas_concluidas,
    ]

    for j, task_list in enumerate(tasks_lists):
        # Calculate the position of the current task
        for i, task in enumerate(task_list):
            row = i // max_tasks_per_row
            col = j
            x = offset_x + col * (taskWid + space_between_tasks)
            y = info.scroll * 10 + offset_y + row * (taskHei + space_between_tasks / 2)

            if x <= event.x <= x + taskWid and y <= event.y <= y + taskHei:
                status = Status.PARA_EXECUTAR
                if j == 1:
                    status = Status.EXECUTANDO
                elif j == 2:
                    status = Status.CONCLUIDA
                info.taskSelected = (i, j)
                drawTasks(agenda)
                return

    info.taskSelected = (-1, info.taskType)
    drawTasks(agenda)


# Chama a tela de inicio
startScreen()


### Tela Principal
canvas = tk.Canvas(
    frame,
    bg="#FFFFFF",
    height=height,
    width=width,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, 0.24 * width, height, fill="#05ACF5", outline="")


start_logo = tk.PhotoImage(file=assets("image_1.png", "frame1"))
start_logo_img = canvas.create_image(0.95 * width, 0.05 * height, image=start_logo)

start_logo_2 = tk.PhotoImage(file=assets("image_2.png", "frame1"))
start_logo_img_2 = canvas.create_image(0.634 * width, 0.0, image=start_logo_2)


# Criando os botões da tela principal
main_frame_buttons = []

for i in range(0, 6):
    if i == 3 or i == 4:
        main_frame_buttons.append(None)
        continue
    photo = tk.PhotoImage(file=assets("button_" + str((i + 1)) + ".png", "frame1"))

    button_1 = tk.Button(frame, image=photo)
    button_1.image = photo
    button_1.place(
        x=0.045 * width,
        y=(0.136 * height + 100.0 * i),
        width=0.15 * width,
        height=0.073 * height,
    )

    main_frame_buttons.append(button_1)


### Tela de início
canvas_inicio = tk.Canvas(
    frame_inicio,
    bg="#FFFFFF",
    height=height,
    width=width,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas_inicio.place(x=0, y=0)

start_image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png", "frame2"))
st_image_1 = canvas_inicio.create_image(width / 2.0, height / 2.0, image=start_image_1)

start_image_2 = tk.PhotoImage(file=relative_to_assets("image_2.png", "frame2"))
st_image_2 = canvas_inicio.create_image(width / 2.0, height / 2.0, image=start_image_2)


### Tela nova tarefa
class TelaNewTask:
    def __init__(self, parent_frame):

        self.prioridade = 0
        self.status = 0
        self.name = ""
        self.data = ""
        self.horario = ""
        self.descricao = ""
        self.categoria = ""

        self.concluido = False
        self.editing = False
        self.editingIndex = -1
        self.editingStatus = 0

        self.canvas = tk.Canvas(
            parent_frame,
            bg="#FFFFFF",
            height=height,
            width=width,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            0.0, 0.0, width, height, fill="#05ACF5", outline=""
        )

        self.image_2 = tk.PhotoImage(file=relative_to_assets("image_2.png", "frame3"))

        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets("button_1.png", "frame3")
        )
        self.button_image_2 = tk.PhotoImage(
            file=relative_to_assets("button_2.png", "frame3")
        )
        self.button_image_3 = tk.PhotoImage(
            file=relative_to_assets("button_3.png", "frame3")
        )
        self.button_image_4 = tk.PhotoImage(
            file=relative_to_assets("button_4.png", "frame3")
        )
        self.button_image_5 = tk.PhotoImage(
            file=relative_to_assets("button_5.png", "frame3")
        )
        self.button_image_6 = tk.PhotoImage(
            file=relative_to_assets("button_6.png", "frame3")
        )
        self.button_image_7 = tk.PhotoImage(
            file=relative_to_assets("button_7.png", "frame3")
        )
        self.button_image_8 = tk.PhotoImage(
            file=relative_to_assets("button_8.png", "frame3")
        )

        self.image_2_id = self.canvas.create_image(width / 2.0, 0.0, image=self.image_2)

        texts_info = [
            (0.169 * height, "Nome da tarefa:"),
            (0.254 * height, "Data da tarefa (dd/mm/aaaa):"),
            (0.338 * height, "Horário da tarefa (hh:mm):"),
            (0.423 * height, "Descrição:"),
            (0.508 * height, "Status da tarefa:"),
            (0.604 * height, "Prioridade da tarefa:"),
            (0.701 * height, "Categoria da tarefa (Ex.: Estudos, Trabalho...):"),
        ]

        for i, text in enumerate(texts_info):
            tk.Label(
                self.canvas, text=text[1], bg="#05ACF5", font=("Calibri Bold", 13)
            ).place(x=0.27 * width, y=text[0])

        entry_y = [
            texts_info[0][0],
            texts_info[1][0],
            texts_info[2][0],
            texts_info[3][0],
            texts_info[6][0],
        ]
        tamanhos = []
        font = tkfont.Font(family="Calibri", weight="bold", size=13)
        for i, j in enumerate(texts_info):
            if i != 4 and i != 5:
                size = font.measure(j[1])
                tamanhos.append(size)

        largura_caixas = [300, 100, 100, 300, 200]
        self.entries = []
        for i in range(0, 5):
            entry = tk.Entry(
                parent_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
            )
            x = tamanhos[i] + 10 + 0.27 * width
            entry.place(x=x, y=entry_y[i] + 3, height=24, width=largura_caixas[i])
            self.entries.append(entry)

        self.entry_dicionario = {
            "nome": 0,
            "data": 1,
            "horario": 2,
            "descricao": 3,
            "categoria": 4,
        }

        self.button_1 = tk.Button(
            parent_frame,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setStatus(Status.PARA_EXECUTAR),
            relief="flat",
        )
        self.button_1.place(x=0.40 * width, y=0.50 * height, width=94.0, height=38.0)
        self.button_2 = tk.Button(
            parent_frame,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setStatus(Status.EXECUTANDO),
            relief="flat",
        )
        self.button_2.place(x=0.52 * width, y=0.50 * height, width=94.0, height=38.0)
        self.button_3 = tk.Button(
            parent_frame,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setStatus(Status.CONCLUIDA),
            relief="flat",
        )
        self.button_3.place(x=0.64 * width, y=0.50 * height, width=94.0, height=38.0)

        self.canvas.create_rectangle(
            0.76 * width,
            0.50 * height,
            0.76 * width + 38,
            0.50 * height + 38,
            fill="#333333",
        )

        self.button_4 = tk.Button(
            parent_frame,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setPrioridade(Prioridade.BAIXA),
            relief="flat",
        )
        self.button_4.place(x=0.43 * width, y=0.60 * height, width=94.0, height=38.0)
        self.button_5 = tk.Button(
            parent_frame,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setPrioridade(Prioridade.MEDIA),
            relief="flat",
        )
        self.button_5.place(x=0.55 * width, y=0.60 * height, width=94.0, height=38.0)
        self.button_6 = tk.Button(
            parent_frame,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setPrioridade(Prioridade.ALTA),
            relief="flat",
        )
        self.button_6.place(x=0.67 * width, y=0.60 * height, width=94.0, height=38.0)

        self.canvas.create_rectangle(
            0.79 * width,
            0.60 * height,
            0.79 * width + 38,
            0.60 * height + 38,
            fill="#333333",
        )

        self.button_image_concluir = tk.PhotoImage(
            file=assets("button_7.png", "frame3")
        )
        self.button_concluir = tk.Button(
            parent_frame,
            image=self.button_image_concluir,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
        )
        self.button_concluir.place(x=0.273 * width, y=0.78 * height)

        self.button_image_8 = tk.PhotoImage(file=assets("button_8.png", "frame3"))
        self.button_8 = tk.Button(
            parent_frame,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: mainScreen(),
            relief="flat",
        )
        self.button_8.place(x=0.55 * width, y=0.78 * height)

    def setPrioridade(self, num):
        self.prioridade = num
        color = "#333333"
        if self.prioridade == Prioridade.BAIXA:
            color = "#FF0000"
        elif self.prioridade == Prioridade.MEDIA:
            color = "#FFFF00"
        elif self.prioridade == Prioridade.ALTA:
            color = "#00FF00"
        self.canvas.create_rectangle(
            0.79 * width,
            0.60 * height,
            0.79 * width + 38,
            0.60 * height + 38,
            fill=color,
        )

    def setStatus(self, num):
        self.status = num
        color = "#333333"
        if self.status == Status.PARA_EXECUTAR:
            color = "#FF0000"
        elif self.status == Status.EXECUTANDO:
            color = "#FFFF00"
        elif self.status == Status.CONCLUIDA:
            color = "#00FF00"
        self.canvas.create_rectangle(
            0.76 * width,
            0.50 * height,
            0.76 * width + 38,
            0.50 * height + 38,
            fill=color,
        )

    def concluir(self, agenda):
        self.name = self.entries[self.entry_dicionario.get("nome")].get()
        self.data = self.entries[self.entry_dicionario.get("data")].get()
        self.horario = self.entries[self.entry_dicionario.get("horario")].get()
        self.descricao = self.entries[self.entry_dicionario.get("descricao")].get()
        self.categoria = self.entries[self.entry_dicionario.get("categoria")].get()
        self.concluido = True

        if (
            (not self.name.strip())
            or (not self.data.strip())
            or (not self.horario.strip())
        ):
            msg.showwarning(
                "Dados inválidos",
                "Preencha os campos 'Nome', 'Data' e 'Horário' corretamente!",
            )
            return
        try:
            data_horario = agenda.str_data_horario(self.data, self.horario)
        except:
            msg.showwarning(
                "Data/horário inválido",
                "Preencha os campos 'Data' e 'Horário' no formato designado\n"
                + "e com valores permitidos!",
            )
            return

        if self.status == None:
            self.status = Status.PARA_EXECUTAR
        if self.prioridade == None:
            self.prioridade = Prioridade.BAIXA

        tarefa = Tarefa(
            self.name,
            data_horario,
            self.descricao,
            self.status,
            self.prioridade,
            self.categoria,
        )
        if self.editing and self.editingIndex != -1:
            agenda.excluir_tarefa(self.editingIndex, self.editingStatus)
        agenda.adicionar_tarefa(tarefa)
        drawTasks(agenda)
        self.editing = False
        mainScreen()


telaNewTask = TelaNewTask(frame_new)

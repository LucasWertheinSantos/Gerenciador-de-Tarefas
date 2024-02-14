import tkinter as tk
import tkinter.messagebox as msg
from datetime import datetime
from pathlib import Path

from main import Prioridade, Status, dicionarioPrioridade, dicionarioStatus
from tarefa import Tarefa

# Funções para associar o caminho de imagens
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")


def assets(path: str, frame: str) -> Path:
    return ASSETS_PATH / Path(frame) / Path(path)


def relative_to_assets(path: str, frame: str) -> Path:
    return assets(path, frame)


# Criando a janela
window = tk.Tk()

# Configurando a janela
window.title("Minha Agenda - v1.0")
width, height = window.winfo_screenwidth(), window.winfo_screenheight()
width -= 100
height -= 80
window.geometry("%dx%d+0+0" % (width, height))
# window.geometry("1440x800")
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
    frame_inicio.place(x=0, y=0, width=1440, height=950)


def break_text_by_length(text, max_length):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) <= max_length:
            current_line += word + " "
        else:
            lines.append(current_line.rstrip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.rstrip())

    return "\n".join(lines)


canvas_tasks = tk.Canvas(
    frame_tasks,
    bg="#FFFFFF",
    height=950,
    width=1052,
    bd=1.75,
    highlightthickness=0,
    relief="ridge",
)
canvas_tasks.place(x=14, y=0)


def drawTasks(agenda):
    wid = 1052
    hei = 950

    taskWid = 290
    taskHei = 280

    offset_x = 50
    offset_y = 50
    space_between_tasks = 45
    max_tasks_per_row = 1

    tasks_lists = [
        agenda.tarefas_para_executar,
        agenda.tarefas_executando,
        agenda.tarefas_concluidas,
    ]
    canvas_tasks.create_rectangle(0, 0, 1060, 950, fill="#FFFFFF")

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
            prioridade = "Nennhuma"
            if task.prioridade != None:
                prioridade = task.prioridade.name
            char_limite = 34
            text = f"{break_text_by_length('NOME:'+task.nome, char_limite)}\n"
            text += f"DATA: {task.data_hora.strftime('%d/%m/%Y')}\n"
            text += f"HORÁRIO: {task.data_hora.strftime('%H:%M')}\n"
            text += f"PRIORIDADE: {prioridade[:1].upper() + prioridade[1:].lower()}\n"
            text += f"CATEGORIA: {task.categoria}\n"
            text += (
                f"{break_text_by_length('DESCRIÇÃO:' + task.descricao, char_limite)}"
            )
            canvas_tasks.create_text(
                x + 10, y + 10, anchor="nw", text=text, font=("Arial", 12)
            )


def fecharJanela():
    window.destroy()


def mainScreen():
    resetData()
    info.screen = 1
    frame_inicio.place_forget()
    frame_new.place_forget()
    frame.place(x=0, y=0, width=1440, height=950)
    frame_tasks.place(x=348, y=100, width=1092, height=950)


def novaTarefaScreen():
    info.screen = 2
    frame_inicio.place_forget()
    frame.place_forget()
    frame_tasks.place_forget()
    frame_new.place(x=0, y=0, width=1440, height=950)


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
    wid = 1052
    hei = 950

    taskWid = 290
    taskHei = 280

    offset_x = 50
    offset_y = 50
    space_between_tasks = 45
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
    height=950,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, 348, 950, fill="#05ACF5", outline="")


start_logo = tk.PhotoImage(file=assets("image_1.png", "frame1"))
start_logo_img = canvas.create_image(1369.0, 50, image=start_logo)

start_logo_2 = tk.PhotoImage(file=assets("image_2.png", "frame1"))
start_logo_img_2 = canvas.create_image(914.0, 0.0, image=start_logo_2)


# Criando os botões da tela principal
main_frame_buttons = []

for i in range(0, 6):
    if i == 3 or i == 4:
        main_frame_buttons.append(None)
        continue
    photo = tk.PhotoImage(file=assets("button_" + str((i + 1)) + ".png", "frame1"))

    button_1 = tk.Button(frame, image=photo)
    button_1.image = photo
    button_1.place(x=65.0, y=(130.0 + 100.0 * i), width=219.0, height=70.0)

    main_frame_buttons.append(button_1)


### Tela de início
canvas_inicio = tk.Canvas(
    frame_inicio,
    bg="#FFFFFF",
    height=950,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas_inicio.place(x=0, y=0)

start_image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png", "frame2"))
st_image_1 = canvas_inicio.create_image(720.0, 475.0, image=start_image_1)

start_image_2 = tk.PhotoImage(file=relative_to_assets("image_2.png", "frame2"))
st_image_2 = canvas_inicio.create_image(width / 2, height / 2, image=start_image_2)

start_image_3 = tk.PhotoImage(file=relative_to_assets("image_3.png", "frame2"))
# st_image_3 = canvas_inicio.create_image(1304.0, 906.0, image=start_image_3)

start_image_4 = tk.PhotoImage(file=relative_to_assets("image_4.png", "frame2"))
# image_4 = canvas_inicio.create_image(1405.0, 891.0, image=start_image_4)

image_image_5 = tk.PhotoImage(file=relative_to_assets("image_5.png", "frame2"))
# image_5 = canvas_inicio.create_image(1293.0, 915.0, image=image_image_5)

image_image_6 = tk.PhotoImage(file=relative_to_assets("image_6.png", "frame2"))
# image_6 = canvas_inicio.create_image(1319.0, 915.0, image=image_image_6)


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
            height=950,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            0.0, 0.0, width, height, fill="#05ACF5", outline=""
        )

        self.image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png", "frame3"))
        self.image_2 = tk.PhotoImage(file=relative_to_assets("image_2.png", "frame3"))

        # self.entry_image_1 = tk.PhotoImage(
        #     file=relative_to_assets("entry_1.png", "frame3")
        # )
        # self.entry_image_2 = tk.PhotoImage(
        #     file=relative_to_assets("entry_2.png", "frame3")
        # )
        # self.entry_image_3 = tk.PhotoImage(
        #     file=relative_to_assets("entry_4.png", "frame3")
        # )
        # self.entry_image_4 = tk.PhotoImage(
        #     file=relative_to_assets("entry_5.png", "frame3")
        # )
        # self.entry_image_5 = tk.PhotoImage(
        #     file=relative_to_assets("entry_6.png", "frame3")
        # )

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

        # self.image_1_id = self.canvas.create_image(1000.0, 500.0, image=self.image_1)
        self.image_2_id = self.canvas.create_image(720.0, 0.0, image=self.image_2)

        texts_info = [
            (140.0, "Nome da tarefa:"),
            (210.0, "Data da tarefa (dd/mm/aaaa):"),
            (280.0, "Horário da tarefa (hh:mm):"),
            (350.0, "Descrição:"),
            (420.0, "Status da tarefa:"),
            (500.0, "Prioridade da tarefa:"),
            (580.0, "Categoria da tarefa (Ex.: Estudos, Trabalho...):"),
        ]

        for y, text in texts_info:
            self.canvas.create_text(
                548.0,
                y,
                anchor="nw",
                text=text,
                fill="#FFFFFF",
                font=("Inter SemiBold", 14),
            )

        # self.entry_bg_1 = self.canvas.create_image(
        #     719.0, 272.5, image=self.entry_image_1
        # )
        # self.entry_bg_2 = self.canvas.create_image(
        #     719.0, 189.5, image=self.entry_image_2
        # )
        # self.entry_bg_3 = self.canvas.create_image(
        #     719.0, 373.5, image=self.entry_image_3
        # )
        # self.entry_bg_4 = self.canvas.create_image(
        #     719.0, 475.5, image=self.entry_image_4
        # )
        # self.entry_bg_5 = self.canvas.create_image(
        #     717.5, 783.5, image=self.entry_image_5
        # )

        # Criando as caixas de texto
        entry_y = [170, 240, 310, 380, 610]
        self.entries = []
        for i in range(0, 5):
            entry = tk.Entry(
                parent_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
            )
            entry.place(x=548.0, y=entry_y[i], height=24, width=350)
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
        self.button_1.place(x=548.0, y=450.0, width=94.0, height=38.0)
        self.button_2 = tk.Button(
            parent_frame,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setStatus(Status.EXECUTANDO),
            relief="flat",
        )
        self.button_2.place(x=673.0, y=450.0, width=94.0, height=38.0)
        self.button_3 = tk.Button(
            parent_frame,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setStatus(Status.CONCLUIDA),
            relief="flat",
        )
        self.button_3.place(x=798.0, y=450.0, width=94.0, height=38.0)

        self.canvas.create_rectangle(920, 450, 958, 488, fill="#333333")

        self.button_4 = tk.Button(
            parent_frame,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setPrioridade(Prioridade.BAIXA),
            relief="flat",
        )
        self.button_4.place(x=548.0, y=530.0, width=94.0, height=38.0)
        self.button_5 = tk.Button(
            parent_frame,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setPrioridade(Prioridade.MEDIA),
            relief="flat",
        )
        self.button_5.place(x=672.0, y=530.0, width=94.0, height=38.0)
        self.button_6 = tk.Button(
            parent_frame,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setPrioridade(Prioridade.ALTA),
            relief="flat",
        )
        self.button_6.place(x=798.0, y=530.0, width=94.0, height=38.0)

        self.canvas.create_rectangle(920, 530, 958, 568, fill="#333333")

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
        self.button_concluir.place(x=548.0, y=650.0)

        self.button_image_8 = tk.PhotoImage(file=assets("button_8.png", "frame3"))
        self.button_8 = tk.Button(
            parent_frame,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: mainScreen(),
            relief="flat",
        )
        self.button_8.place(x=758.0, y=650.0)

    def setPrioridade(self, num):
        self.prioridade = num
        color = "#333333"
        if self.prioridade == Prioridade.BAIXA:
            color = "#FF0000"
        elif self.prioridade == Prioridade.MEDIA:
            color = "#FFFF00"
        elif self.prioridade == Prioridade.ALTA:
            color = "#00FF00"
        self.canvas.create_rectangle(920, 530, 958, 568, fill=color)

    def setStatus(self, num):
        self.status = num
        color = "#333333"
        if self.status == Status.PARA_EXECUTAR:
            color = "#FF0000"
        elif self.status == Status.EXECUTANDO:
            color = "#FFFF00"
        elif self.status == Status.CONCLUIDA:
            color = "#00FF00"
        self.canvas.create_rectangle(920, 450, 958, 488, fill=color)

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
        except ValueError:
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

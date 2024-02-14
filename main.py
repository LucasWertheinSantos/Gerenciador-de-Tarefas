from datetime import datetime
from enum import Enum

Status = Enum("Status", ["PARA_EXECUTAR", "EXECUTANDO", "CONCLUIDA"])
Prioridade = Enum("Prioridade", ["ALTA", "MEDIA", "BAIXA"])

# Dicionarios
dicionarioStatus = {0: Status.PARA_EXECUTAR, 1: Status.EXECUTANDO, 2: Status.CONCLUIDA}
dicionarioPrioridade = {0: Prioridade.ALTA, 1: Prioridade.MEDIA, 2: Prioridade.BAIXA}

DATE_FORMAT = "%d/%m/%y, %H:%M"

import gui as gui
from agenda import *

if __name__ == "__main__":
    agenda = Agenda()
    agenda.load_tasks("agenda.dat")
    gui.drawTasks(agenda)

    # Arrumando os eventos de botões
    gui.telaNewTask.button_concluir.config(
        command=lambda: gui.telaNewTask.concluir(agenda)
    )
    gui.main_frame_buttons[0].config(command=gui.novaTarefaScreen)
    gui.main_frame_buttons[1].config(command=lambda: gui.deleteTask(agenda))
    gui.main_frame_buttons[2].config(command=lambda: gui.editTask(agenda))
    gui.main_frame_buttons[5].config(command=gui.fecharJanela)
    gui.window.bind("<Button-1>", lambda event: gui.click())
    gui.canvas_tasks.bind(
        "<MouseWheel>", lambda event: gui.scrollTasks(event.delta / 10, agenda)
    )
    gui.canvas_tasks.bind("<Button-1>", lambda event: gui.selectTask(event, agenda))

    gui.window.mainloop()
    agenda.save_tasks("agenda.dat")

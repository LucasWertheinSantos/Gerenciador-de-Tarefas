from datetime import datetime
from enum import Enum

Status = Enum("Status", ["PARA_EXECUTAR", "EXECUTANDO", "CONCLUIDA"])
Prioridade = Enum("Prioridade", ["ALTA", "MEDIA", "BAIXA"])

DATE_FORMAT = "%d/%m/%y, %H:%M"

from agenda import *

if __name__ == "__main__":
    task = Tarefa(
        "Estudar para TEP",
        datetime(2024, 2, 10, 14, 00),
        "Ler conteúdo para a prova",
        status=Status.EXECUTANDO,
        prioridade=Prioridade.MEDIA,
    )
    agenda = Agenda()
    agenda.criar_tarefa()
    agenda.adicionar_tarefa(task)
    agenda.listar_tarefas_por_status(Status.PARA_EXECUTAR)
    agenda.adicionar_feedback_tarefa()

from datetime import datetime
from enum import Enum

Status = Enum("Status", ["PARA_EXECUTAR", "EXECUTANDO", "CONCLUIDA"])

Prioridade = Enum("Prioridade", ["ALTA", "MEDIA", "BAIXA"])

DATE_FORMAT = "%d/%m/%y, %H:%M"


class Agenda:
    def __init__(self):
        self.tarefas_para_executar = []
        self.tarefas_executando = []
        self.tarefas_concluidas = []

    def adicionar_tarefa(self, tarefa):
        print()
        print(">> Criação de nova tarefa <<")
        nome = input("Nome da tarefa: ")
        data_str = ""
        data_str += input("Data da tarefa")


class Tarefa:
    def __init__(
        self,
        nome,
        data_hora,
        descricao=None,
        status=Status.PARA_EXECUTAR,
        prioridade=None,
    ):
        self.nome = nome
        self.data_criacao = datetime.now()
        self.data_hora = data_hora
        self.data_conclusao = None
        self.descricao = descricao
        self.status = status
        self.prioridade = prioridade

    def __str__(self) -> str:
        s = f">> Tarefa: {self.nome}\n"
        if self.descricao:
            s += f"Descrição: {self.descricao}\n"
        s += f"Status: {self.status.name}\n"
        if self.prioridade:
            s += f"Prioridade: {self.prioridade.name}\n"
        # s += f"Data de criação: {self.data_criacao.strftime(DATE_FORMAT)}\n"
        if self.data_hora:
            s += f"Data e hora da tarefa: {self.data_hora.strftime(DATE_FORMAT)}\n"
        if self.data_conclusao:
            s += f"Data de conclusão: {self.data_conclusao.strftime(DATE_FORMAT)}\n"
        return s

    def renomear_tarefa(self, nome):
        self.nome = nome
        print(f"Tarefa renomeada para: {self.nome}\n")

    def alterar_data_hora_tarefa(self, dia, mes, hora, minuto):
        data = datetime(datetime.now().year, mes, dia, hora, minuto)
        self.data_hora = data
        print(f"Data final alterada para: {self.data_hora.ctime()}\n")

    def alterar_status(self, novo_status):
        if novo_status == Status.CONCLUIDA:
            self.data_conclusao = datetime.now()
        elif self.status == Status.CONCLUIDA and novo_status != Status.CONCLUIDA:
            self.data_conclusao = None
        self.status = novo_status

        print(f"Status alterado para: {self.status.name}\n")

    def alterar_prioridade(self, prioridade):
        self.prioridade = prioridade
        print(f"Prioridade alterada para: {self.prioridade.name}\n")

    def alterar_descricao(self, descricao):
        self.descricao = descricao
        print(f"Descrição alterada para: {self.descricao}\n")


if __name__ == "__main__":
    task = Tarefa(
        "Estudar para TEP",
        datetime(2024, 2, 8, 14, 00),
        "Ler conteúdo para a prova",
        status=Status.EXECUTANDO,
        prioridade=Prioridade.MEDIA,
    )
    print(task)

from datetime import datetime

from Main import Prioridade, Status

from tarefa import Tarefa


class Agenda:
    def __init__(self):
        self.tarefas_para_executar = []
        self.tarefas_executando = []
        self.tarefas_concluidas = []

    def criar_tarefa(self):
        print()
        print(">> Criação de nova tarefa <<")
        nome = input("Nome da tarefa: ")
        data_str = ""
        data_str += input("Data da tarefa (dd/mm/aaaa): ")
        data_str += " " + input("Horário da tarefa (hh:mm): ")
        data_str = data_str.split(" ")
        data = [int(i) for i in data_str[0].split("/")]
        horario = [int(i) for i in data_str[1].split(":")]
        data_horario = datetime(data[2], data[1], data[0], horario[0], horario[1])

        descricao = None
        resp = input("Deseja adicionar descrição? (s/n): ")
        if resp == "s":
            descricao = input("Descrição da tarefa: ")

        status = Status.PARA_EXECUTAR
        resp = input("Deseja adicionar status? (s/n): ")
        if resp == "s":
            print("Status da tarefa:")
            print("1 - Para executar")
            print("2 - Executando")
            print("3 - Concluída")
            op = int(input("Opção: "))
            status = Status(op)

        prioridade = None
        resp = input("Deseja adicionar prioridade? (s/n): ")
        if resp == "s":
            print("Prioridade da tarefa:")
            print("1 - Alta")
            print("2 - Média")
            print("3 - Baixa")
            op = int(input("Opção: "))
            prioridade = Prioridade(op)

        categoria = None
        resp = input("Deseja adicionar categoria? (s/n): ")
        if resp == "s":
            categoria = input(
                "Digite o nome da categoria que deseja adicionar esta atividade: "
            )

        tarefa = Tarefa(nome, data_horario, descricao, status, prioridade, categoria)
        self.associar_tarefa(tarefa)

        print("Tarefa criada com sucesso!")

    def adicionar_tarefa(self, tarefa):
        self.associar_tarefa(tarefa)

    def associar_tarefa(self, tarefa):
        status = tarefa.status
        if status == Status.PARA_EXECUTAR:
            self.tarefas_para_executar.append(tarefa)
        elif status == Status.EXECUTANDO:
            self.tarefas_executando.append(tarefa)
        else:
            self.tarefas_concluidas.append(tarefa)

    def listar_tarefas_por_status(self, status):
        if status == Status.PARA_EXECUTAR:
            self.listar_tarefas(self.tarefas_para_executar, status)
        elif status == Status.EXECUTANDO:
            self.listar_tarefas(self.tarefas_executando, status)
        elif status == Status.CONCLUIDA:
            self.listar_tarefas(self.tarefas_concluidas, status)

    def listar_tarefas(self, tarefas, status):
        print()
        print(f">>> Lista de tarefas - Status: {status.name} <<<\n")
        for tarefa in tarefas:
            print(tarefa)

    def feedback(self):
        task = Tarefa(input("Digite o nome da tarefa: "), "")
        status = int(
            input(
                "1- Para executar \n2- Executando \n3- Concluida \nDigite o novo status da sua atividade: "
            )
        )
        if status == 3:
            comentario = input(
                "Deseja deixar algum comentário sobre a tarefa? sim/nao: "
            )
            if comentario == "sim":
                comentario = input("Deixe seu comentário: ")
                print(comentario)
                task.alterar_status(Status.CONCLUIDA)
            else:
                task.alterar_status(Status.CONCLUIDA)

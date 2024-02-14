from datetime import datetime

from main import Prioridade, Status, dicionarioStatus, dicionarioPrioridade
from tarefa import Tarefa
import pickle

class Agenda:
    def __init__(self):
        self.tarefas_para_executar = []
        self.tarefas_executando = []
        self.tarefas_concluidas = []

    def str_data_horario(self, data, horario):
        data_str = ""
        data_str += data
        data_str += " " + horario
        data_str = data_str.split(" ")
        data = [int(i) for i in data_str[0].split("/")]
        horario = [int(i) for i in data_str[1].split(":")]
        data_horario = datetime(data[2], data[1], data[0], horario[0], horario[1])
        return data_horario

    def criar_tarefa(self):
        print()
        print(">> Criação de nova tarefa <<")
        nome = input("Nome da tarefa: ")
        data = input("Data da tarefa (dd/mm/aaaa): ")
        horario = input("Horário da tarefa (hh:mm): ")
        data_horario = self.str_data_horario(data, horario)

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

    def excluir_tarefa(self, tarefa_index, tarefa_status):
        if tarefa_status == 0:
            self.tarefas_para_executar.pop(tarefa_index)
        elif tarefa_status == 1:
            self.tarefas_executando.pop(tarefa_index)
        elif tarefa_status == 2:
            self.tarefas_concluidas.pop(tarefa_index)

    def pegar_tarefa(self, tarefa_index, tarefa_status):
        if tarefa_index == -1:
            return None
        if tarefa_status == 0:
            return self.tarefas_para_executar[tarefa_index]
        elif tarefa_status == 1:
            return self.tarefas_executando[tarefa_index]
        elif tarefa_status == 2:
            return self.tarefas_concluidas[tarefa_index]
        
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
            self.imprimir_tarefas_status(self.tarefas_para_executar, status)
        elif status == Status.EXECUTANDO:
            self.imprimir_tarefas_status(self.tarefas_executando, status)
        elif status == Status.CONCLUIDA:
            self.imprimir_tarefas_status(self.tarefas_concluidas, status)

    def imprimir_tarefas_status(self, tarefas, status):
        print()
        print(f">>> Lista de tarefas - Status: {status.name} <<<\n")
        for tarefa in tarefas:
            print(tarefa)

    def pesquisar_tarefas_por_data(self, data):
        tarefas_data = []
        tarefas_data = list(
            filter(lambda t: t.data_hora.date() == data, self.tarefas_para_executar)
        )
        tarefas_data += list(
            filter(lambda t: t.data_hora.date() == data, self.tarefas_executando)
        )
        tarefas_data += list(
            filter(lambda t: t.data_hora.date() == data, self.tarefas_concluidas)
        )
        return tarefas_data

    # Uso interno
    def imprimir_tarefas_data(self, tarefas):
        data = tarefas[0].data_hora
        formato = "%d/%m/%y"
        print()
        print(f">>> Lista de tarefas - Data: {data.strftime(formato)} <<<\n")
        for i, tarefa in enumerate(tarefas):
            print(f">> {i+1}:")
            print(tarefa)

    # Por enquanto permite adicionar feedback a qualquer tarefa
    def adicionar_feedback_tarefa(self):
        print()
        data_str = input(
            "Digite a data da tarefa que deseja dar feedback (dd/mm/aaaa): "
        )
        data = [int(i) for i in data_str.split("/")]
        tarefas = self.pesquisar_tarefas_por_data(
            datetime(data[2], data[1], data[0]).date()
        )
        if len(tarefas) == 0:
            print(">>> Não existem tarefas criadas na data escolhida!")
            return

        self.imprimir_tarefas_data(tarefas)
        num_tarefa = int(input("Digite o número da tarefa desejada: "))
        if num_tarefa > len(tarefas) or num_tarefa < 1:
            print("Número inválido!")
            return

        tarefa = tarefas[num_tarefa - 1]
        print(tarefa)
        print(">>> Feedback <<<")
        comentario = input("> Digite seu comentário sobre a tarefa: ")
        tarefa.alterar_feedback(comentario)

    def save_tasks(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump([self.tarefas_para_executar, self.tarefas_executando, self.tarefas_concluidas], file)

    def load_tasks(self, filename):
        with open(filename, 'rb') as file:
            task_lists = pickle.load(file)
        self.tarefas_para_executar, self.tarefas_executando, self.tarefas_concluidas = task_lists

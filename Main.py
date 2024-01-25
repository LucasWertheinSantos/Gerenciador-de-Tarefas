class Tarefa:
    def __init__(self, nome, descricao, hora_inicio, hora_fim, prioridade, categoria, etiquetas=[]):
        self.nome = nome
        self.descricao = descricao
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.prioridade = prioridade
        self.categoria = categoria
        self.etiquetas = etiquetas
        self.concluida = False

class OrganizadorTarefas:
    def __init__(self):
        self.tarefas = []

    def cadastrar_tarefa(self, tarefa):
        # Adicionar lógica para cadastrar tarefa
        pass

    def exibir_rotina_diaria(self):
        # Adicionar lógica para exibir tarefas diárias
        pass

    def exibir_rotina_semanal(self):
        # Adicionar lógica para exibir tarefas semanais
        pass

    def exibir_rotina_mensal(self):
        # Adicionar lógica para exibir tarefas mensais
        pass

    def priorizar_tarefa(self, nome_tarefa, nova_prioridade):
        # Adicionar lógica para priorizar tarefa
        pass

    def categorizar_tarefa(self, nome_tarefa, nova_categoria):
        # Adicionar lógica para categorizar tarefa
        pass

    def editar_tarefa(self, nome_tarefa, nova_descricao, nova_hora_inicio, nova_hora_fim):
        # Adicionar lógica para editar tarefa
        pass

    def excluir_tarefa(self, nome_tarefa):
        # Adicionar lógica para excluir tarefa
        pass

    def gerar_relatorio_desempenho(self):
        # Adicionar lógica para gerar relatório de desempenho
        pass

    def marcar_tarefa_concluida(self, nome_tarefa):
        # Adicionar lógica para marcar tarefa como concluída
        pass
        
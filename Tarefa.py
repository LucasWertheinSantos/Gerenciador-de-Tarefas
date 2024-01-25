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
        
from datetime import datetime
from enum import Enum
from typing import cast  # Usado para teste por enquanto

import dill as pickle

Status = Enum("Status", ["PARA_EXECUTAR", "EXECUTANDO", "CONCLUIDA"])
Prioridade = Enum("Prioridade", ["ALTA", "MEDIA", "BAIXA"])

DATE_FORMAT = "%d/%m/%y, %H:%M"

FILE_NAME = "data.pkl"

from agenda import *


def salvar_dados_arquivo(dados):
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump(dados, f, protocol=pickle.HIGHEST_PROTOCOL)
            print("Dados salvos no arquivo com sucesso!\n")
    except Exception as ex:
        print("Error during pickling object: ", ex)


def carregar_dados_arquivo(arquivo):
    with open(arquivo, "rb") as f:
        try:
            dados = pickle.load(f)
            return dados
        except pickle.UnpicklingError:
            print("Error: Cannot unpickling object")


if __name__ == "__main__":
    task1 = Tarefa(
        "Estudar para TEP",
        datetime(2024, 2, 10, 14, 00),
        "Ler conteúdo para a prova",
        status=Status.EXECUTANDO,
        prioridade=Prioridade.MEDIA,
    )
    task2 = Tarefa(
        "Ir ao mercado",
        datetime(2024, 2, 10, 15, 00),
        "Fazer compras do mês",
        status=Status.PARA_EXECUTAR,
        prioridade=Prioridade.MEDIA,
    )
    agenda = Agenda()
    agenda.adicionar_tarefa(task1)
    agenda.adicionar_tarefa(task2)

    #############
    dados_para_arquivo = []
    dados_para_arquivo.append(agenda)

    salvar_dados_arquivo(dados_para_arquivo)

    # Testes
    reload = carregar_dados_arquivo(FILE_NAME)
    for i in reload:
        # i = cast(Agenda, i)
        if isinstance(i, Agenda):
            print("É agenda!")
    print()

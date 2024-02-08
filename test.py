from enum import Enum

Prioridade = Enum("Prioridade", ["ALTA", "MEDIA", "BAIXA"])


var = Prioridade(1)
print(var)
print(Prioridade.ALTA)

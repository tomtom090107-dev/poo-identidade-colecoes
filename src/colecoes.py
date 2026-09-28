from dataclasses import dataclass
from typing import Generic, TypeVar
from identidade import IdSensor


@dataclass(frozen=True)
class Medicao:
    valor: float
    unidade: str


T = TypeVar("T")


class Catalogo(Generic[T]):
    def __init__(self):
        self._itens: dict[IdSensor, T] = {}

    def inserir(self, id: IdSensor, item: T) -> bool:
        if id in self._itens:
            return False
        self._itens[id] = item
        return True

    def buscar(self, id: IdSensor) -> T | None:
        return self._itens.get(id)

    def remover(self, id: IdSensor) -> bool:
        if id in self._itens:
            del self._itens[id]
            return True
        return False

    def quantidade(self):
        return len(self._itens)

    def ids(self):
        return set(self._itens)
from colecoes import Medicao


class Historico:
    """Histórico de um sensor; preserva cada ocorrência, inclusive repetida."""

    def __init__(self):
        self._leituras: list[Medicao] = []

    def registrar(self, leitura: Medicao):
        self._leituras.append(leitura)

    def quantidade(self):
        return len(self._leituras)

    def ultimas(self, limite: int) -> list[Medicao]:
        # Fornecido: C++ usa size_t; Python precisa rejeitar negativos.
        if limite < 0:
            raise ValueError("limite deve ser nao negativo")
        if limite == 0:
            return []
        if limite >= len(self._leituras):
            return list(self._leituras)
        return list(self._leituras[-limite:])
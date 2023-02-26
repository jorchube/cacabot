from src.caca import Caca
from src.persistence.repository import Repository


def do(cacas: list[Caca]) -> None:
    repository = Repository.get()

    for caca in cacas:
        repository.store_caca(caca)

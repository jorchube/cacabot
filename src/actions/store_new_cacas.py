import logging
from caca import Caca
from persistence.repository import Repository


def do(cacas: list[Caca]) -> None:
    repository = Repository.get()

    for caca in cacas:
        repository.store_or_update_caca(caca)

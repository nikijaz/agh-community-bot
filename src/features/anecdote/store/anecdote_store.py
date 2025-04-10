import hashlib
from typing import Final, Required, TypedDict


class Anecdote(TypedDict):
    text: Required[str]
    hash: Required[str]


def get_anecdote_list() -> list[Anecdote]:
    result: list[Anecdote] = []

    with open("anecdotes.txt", "r", encoding="utf-8") as file:
        anecdote_list = [line.strip() for line in file if line.strip()]

        hasher = hashlib.blake2s(digest_size=8)
        for anecdote in anecdote_list:
            text = anecdote.strip()
            hasher.update(text.encode())
            hash = hasher.hexdigest()
            result.append({"text": text, "hash": hash})

    return result


ANECDOTE_STORE: Final = get_anecdote_list()

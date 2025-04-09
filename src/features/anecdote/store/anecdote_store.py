from typing import Final, Required, TypedDict


class Anecdote(TypedDict):
    text: Required[str]
    hash: Required[int]  # This will be used to check if the anecdote was already sent


def get_anecdote_list() -> list[Anecdote]:
    result: list[Anecdote] = []

    with open("anecdotes.txt", "r") as file:
        anecdote_list = filter(lambda x: x != "", file.readlines())
        for anecdote in anecdote_list:
            text = anecdote.strip()
            hash_value = hash(text)
            result.append({"text": text, "hash": hash_value})

    return result


ANECDOTE_STORE: Final = get_anecdote_list()

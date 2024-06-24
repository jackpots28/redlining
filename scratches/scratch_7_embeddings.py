import os
import sys
import pathlib

import ollama
from loguru import logger

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, os.path.abspath(project_root))

# logger.remove(0)
# logger.add(sys.stderr, format="{level} : {time} : {message} - proc({process})")
#
# logger.remove()


def retrieve_file(filename: str) -> pathlib.Path:
    temp_file_path = pathlib.Path(f"{project_root}/files/{filename}")
    logger.info(f"Retrieving file {temp_file_path.resolve()}")
    logger.info(f"{filename} exists: {temp_file_path.exists()}")

    return temp_file_path.resolve()


test_1 = retrieve_file("test_1.txt")
test_ipsum = retrieve_file("test_ipsum.txt")


def file_to_list(file: pathlib.Path) -> list[str]:
    logger.info(f"Reading file {file}")
    output_list = [sentence for sentence in (file.read_text()).split(".")]

    return output_list


test_ipsum_list = file_to_list(test_ipsum)
print(test_ipsum_list)

print(ollama.embeddings.__code__.co_varnames)


def list_to_embeddings(input_list: list[str], model="nomic-embed-text", keep_alive=0) -> list[float]:
    embeddings_list = []
    for sentence in input_list:
        print(f"Sentence: {sentence}")
        temp_embed = ollama.embeddings(model=model, prompt=sentence, keep_alive=keep_alive,
                                       options={"embedding_only": True})

        print(f"Embedding: {temp_embed}\n\n")
        embeddings_list.append(temp_embed)

    return embeddings_list


print(list_to_embeddings(test_ipsum_list))

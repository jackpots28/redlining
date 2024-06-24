import os
import string
import sys
import pathlib

# from dataclasses import dataclass
# import psycopg2
# from dotenv import load_dotenv, dotenv_values

import ollama
from loguru import logger
from src.utils.exec_time_deco import exec_time

import numpy as np
from numpy.linalg import norm

import pandas as pd

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.abspath(project_root))

# from src.utils.exec_time_deco import exec_time

# Started to use loguru, seems nice
logger.remove(0)
logger.add(sys.stderr, format="{level} : {time} : {message} - proc({process})")
logger.remove()


# load_dotenv()

@exec_time
def retrieve_file(filename: str) -> pathlib.Path:
    temp_file_path = pathlib.Path(f"{project_root}/{filename}")
    logger.info(f"Retrieving file {temp_file_path.resolve()}")
    logger.info(f"{filename} exists: {temp_file_path.exists()}")
    return temp_file_path.resolve()


@exec_time
def file_to_list(file: pathlib.Path) -> list[str]:
    logger.info(f"Reading file {file}")
    output_list = [sentence for sentence in (file.read_text()).split("\n")]
    output_list = list(filter(None, output_list))
    return output_list


test_ipsum = retrieve_file("test_ipsum.txt")
test_ipsum_list = file_to_list(test_ipsum)

test_dds_scratch = retrieve_file("dds_scratch_commands.txt")
test_dds_list = file_to_list(test_dds_scratch)

# print(test_ipsum_list)
# print(ollama.embeddings.__code__.co_varnames)

# Utility class for psql db connector and methods for insertion / selection based on cosine similarity
'''
@dataclass
class db_connector:
    db_connection = None
    db_user: str = os.getenv("DB_USER")
    db_passwd: str = os.getenv("DB_PASSWD")
    db_host: str = os.getenv("DB_HOST")
    db_port: int = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")

    def __init__(self):
        if db_connector.db_connection is None:
            try:
                db_connector.db_connection = psycopg2.connect(
                    user=self.db_user,
                    password=self.db_passwd,
                    host=self.db_host,
                    port=self.db_port,
                    database=self.db_name
                )
            except Exception as e:
                print(f"Exception while connecting to database: {str(e)}")

    @staticmethod
    @exec_time
    def db_execute_insert(insert_sentence: str, insert_embedding: list) -> None:
        try:
            db_cursor = db_connector.db_connection.cursor()
            db_cursor.execute("INSERT INTO items (content, embedding) VALUES (%s, %s)",
                              (insert_sentence, insert_embedding))
            db_connector.db_connection.commit()
            # db_cursor.close()
        except Exception as e:
            db_connector.db_connection.close()
            print(f"Error executing insert statement: {str(e)}")

    @staticmethod
    @exec_time
    def db_execute_retrieve(search_sentence_embed: list) -> list:
        output_list = []
        try:
            db_cursor = db_connector.db_connection.cursor()
            db_cursor.execute("""SELECT * FROM items ORDER BY embedding <=> %s::vector LIMIT 5""",
                              (search_sentence_embed,))
            for row in db_cursor.fetchall():
                # print(f"ID: {row[0]}, CONTENT: {row[1]}, Cosine Similarity: {row[2]}")
                output_list.append(row[1])
            # db_cursor.close()
        except Exception as e:
            db_connector.db_connection.close()
            print(f"Error executing retrieve statement: {str(e)}")
        return output_list

    @staticmethod
    @exec_time
    def db_drop_table(table_name: str) -> None:
        try:
            db_cursor = db_connector.db_connection.cursor()
            db_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            db_connector.db_connection.commit()
            # db_cursor.close()
        except Exception as e:
            db_connector.db_connection.close()
            print(f"Error dropping table: {str(e)}")

        return None

    @staticmethod
    @exec_time
    def db_create_table(table_name: str) -> None:
        try:
            db_cursor = db_connector.db_connection.cursor()
            db_cursor.execute(
                f"CREATE TABLE {table_name} (id bigserial PRIMARY KEY, content TEXT, embedding vector(768))")
            db_connector.db_connection.commit()
            # db_cursor.close()
        except Exception as e:
            db_connector.db_connection.close()
            print(f"Error creating table: {str(e)}")
'''

''''''
''''''


@exec_time
def list_to_embeddings(input_list: list[str],
                       model="nomic-embed-text",
                       keep_alive=0,
                       dimensions: int = 768) -> list[float]:
    embeddings_list = []
    for ingest_sentence in input_list:
        temp_embed = ollama.embeddings(model=model,
                                       prompt=ingest_sentence,
                                       keep_alive=keep_alive,
                                       options={"embedding_only": True})
        if len(temp_embed["embedding"]) == dimensions:
            embeddings_list.append(temp_embed["embedding"])

    return embeddings_list


@exec_time
def string_to_embedding(input_string: string, model="nomic-embed-text", keep_alive=0) -> float:
    return ollama.embeddings(model=model,
                             prompt=input_string,
                             keep_alive=keep_alive,
                             options={"embedding_only": True})["embedding"]


# produces float output of cosine similarity between two embedding values
@exec_time
def get_cosine_between_two_embeddings(embed_1: list[float], embed_2: list[float]) -> float:
    return np.dot(embed_1, embed_2) / (norm(embed_1) * norm(embed_2))


@exec_time
def ingest_embeddings_into_dataframe(input_content_list: list[str]) -> pd.DataFrame:
    return pd.DataFrame({'Content': input_content_list, 'Embedding': list_to_embeddings(input_content_list)})


if __name__ == "__main__":

    test_string = "This is a test string for embedding purposes"
    test_embedding = string_to_embedding(test_string)
    print(test_embedding)

    print(test_dds_list)

    for i in range(0, len(test_dds_list)):
        print(i)
        print(string_to_embedding(test_dds_list[i]))

    # ''''''
    # ''' Testing Pandas and Numpy for Cosine Similarity vs using vector db '''
    # df = pd.DataFrame({'Content': test_ipsum_list, 'Embedding': list_to_embeddings(test_ipsum_list)})
    #
    # # print(type(df.Embedding[1][0]))
    #
    # for i in range(0, df.Embedding.size):
    #     temp_cosine_value = get_cosine_between_two_embeddings(df.Embedding[0], df.Embedding[i])
    #     print(f"Index 0 similarity to Index {i}: {temp_cosine_value}")
    #     if temp_cosine_value >= 0.70:
    #         print(f"Content at match: {df.Content[i]}")
    #
    # print(f"{'-' * 40}")
    # print(df.to_markdown(index=True))
    #
    # ''''''
    #
    # print(f"{'-' * 40}")

    '''
    sentence = "quis nostrum exercitationem ullam corporis"
    search_embed = ollama.embeddings(model="nomic-embed-text", prompt=sentence, keep_alive=0,
                                     options={"embedding_only": True})

    test_db = db_connector()

    test_db.db_drop_table("items")
    test_db.db_create_table("items")

    for ingest_sentence in test_ipsum_list:
        temp_embed = ollama.embeddings(model="nomic-embed-text", prompt=ingest_sentence, keep_alive=0,
                                       options={"embedding_only": True})
        if len(temp_embed["embedding"]) == 768:
            test_db.db_execute_insert(ingest_sentence, temp_embed["embedding"])

    test_list = test_db.db_execute_retrieve(search_embed["embedding"])
    print(test_list)
    '''

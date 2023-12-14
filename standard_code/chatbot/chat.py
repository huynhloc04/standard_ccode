import os
import logging 
import argparse
import pandas as pd
from pprint import pprint
from typing import Dict, List
import openai, json, chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm


openai.api_key = open("key.txt", "r").read()
os.environ["OPENAI_API_KEY"] = openai.api_key


class ChromaDB():
    def __init__(self, collection_name: str = "start3D_DB", 
                 data_path: str = "data/start3D_DB.txt", 
                 chromadb_path: str = "./chroma_db",
                 chunk_size: int = 1024,    #   1024 
                 chunk_overlap: int = 64) -> None:  #   64
        """
        Prepare class for creating and populating a document database.

        Args:
            db_name: The name of the document database.
            data_path: The path to the input data file.
            chromadb_path: The path to the ChromaDB directory.
            chunk_size: The size of each document chunk.
            chunk_overlap: The overlap between adjacent document chunks.
        """
        self.collection_name = collection_name
        self.data_path = data_path
        self.chromadb_path = chromadb_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def __call__(self, dis_func: str = "cosine") -> None:
        #   Text chunking
        self.docs_chunks = self.prep_docs(self.data_path)

        # Create an OpenAIEmbeddingFunction instance
        embed_func = embedding_functions.OpenAIEmbeddingFunction(
                            api_key=os.environ["OPENAI_API_KEY"],
                            model_name="text-embedding-ada-002"
                )
        
        # Create a PersistentClient and get or create the collection
        client = chromadb.PersistentClient(self.chromadb_path)
        self.collection = client.get_or_create_collection(name=self.collection_name, 
                                                    embedding_function=embed_func, 
                                                    metadata={"hnsw:space": dis_func})

        # Add documents to the collection
        self.collection.add(
            documents=self.docs_chunks,
            ids = [str(i) for i in range(len(self.docs_chunks))]
        )
    
    def prep_docs(self, data_path) -> List[str]:
        """
        Args:
            data_path: text file to update
        """
        with open(data_path, 'r') as file:
            text = file.read()        
        # Split the corpus into documents
        text_splitter = split_docs(self.chunk_size, self.chunk_overlap)
        chunks = list(set(text_splitter.split_text(text)))
        return chunks

    def update_db(self, new_docs: str) -> None:
        #   Text chunking of the updated docs
        updated_chunks = self.prep_docs(new_docs)
        prev_id = len(self.docs_chunks)
        #   Update new data through "upsert" method
        self.collection.upsert(
                ids=[str(prev_id+i) for i in range(len(updated_chunks))],
                documents=updated_chunks,
        )
    
    def get_context(self, query, top_k=5) -> str:
        #   Get embedding vector
        embed_vec = text_embedding(query)
        results = self.collection.query(
                    query_embeddings=[embed_vec],
                    n_results=top_k)
        result_text = "\n".join(str(item) for item in results['documents'][0])
        return result_text


def split_docs(chunk_size: int, chunk_overlap: int) -> str:
    """
    Split document into chunks
    Args: 
        chunk_size: controls the max size (in terms of number of characters) of the final chunk
        chunk_overlap: the maximum overlap between chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap  = chunk_overlap,
        length_function = len,
        add_start_index = True,
    )
    return text_splitter


def text_embedding(text: str):
    """
    Generates embedding vector for the given text.
    Args:
        text (str): The input text for which the embedding needs to be generated.
    Returns:
        embedding (list): A list representing the embedding of the input text.
    """ 
    response = openai.Embedding.create(model="text-embedding-ada-002", input=text)
    return response["data"][0]["embedding"]


def chat_with_context(context: str, query: str) -> Dict:
    """
    Chat with context and answer the given question.
    Args:
        context (str): The context text.
        query (str): The question to be answered.
    Returns:
        The response JSON containing the answer.
    """

    prompt_template = '''
    Context section:
        {context}

    Question:
        {query}

    Based on the above context section, please answer the question using only the given context. The response must follow strictly JSON format with two keys listed below: 
        - answer:
        - similar_questions:
    If the context does not provide any related information to the question, the 'answer' key must be 'Not relevant'. 
    Besides, please suggest three similar questions to the current question in the 'similar_questions' key. 
    Important: All of the answers must be in Vietnamese.
    '''
    prompt_context = prompt_template.format(context=context, query=query)    

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
                    {"role": "system", "content": "You are a useful chatbot as a tour guide. Please answer all information about tourist attractions in Vietnam."},
                    {"role": "user", "content": prompt_context}
                 ],
        temperature=0
    )
    response_message = response["choices"][0]["message"]["content"]

    return json.loads(response_message)


def get_response(chromadb: ChromaDB, query: str, top_k: int) -> Dict:
    context = chromadb.get_context(query, top_k)
    try:
        final_res = chat_with_context(context, query)
        return final_res
    except:
        return None


# Initialize the parser
parser = argparse.ArgumentParser(description='Optional app description!!!')
if __name__ == "__main__":
    parser.add_argument("--top_k", type=int, default=5, help="Top k documents to join in context.")
    parser.add_argument("--dis_func", type=str, default='cosine', help="Distance function in ChromaDB embedding search: cosine, l1, l2")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s %(message)s", 
        datefmt = "%Y-%m-%d %H:%M:%S",
        filename="start3D_log.log"
    )

    my_db = ChromaDB()
    my_db(dis_func=args.dis_func)

    #   Update ChromaDB collection?
    content = input("Do you want to update ChromaDB collection? Type (y/n): ") 
    if content.lower() == "y":
        data_path = input("Type the file path: ")
        my_db.update_db(data_path)

    #   Get response
    query = "Ở khu thiếu nhi của Công viên Văn hóa Đầm Sen, sân khấu Dế Mèn hoạt động vào những ngày nào trong tuần?"
    response = get_response(my_db, query, args.top_k)
    pprint(response)



#   Ve distribution cua moi chunk >>> top_k. Gop n chunks < 12k token
#   top_k: 1-> 15, Ve bieu do, 50 cau hoi, lay dinh k cuar normal dis### cot ngang: K, cot doc: so TH chinh xac
#   chunk_size, top_k bao nhieu de context token <= 12K va max acc cua search embedding
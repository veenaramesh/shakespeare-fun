import argparse 
from langchain_community.document_loaders import GutenbergLoader

from shakespeare.character import ShakespeareCharacter
from shakespeare.db import DialogueSplitter, ChromaDB

import warnings
warnings.filterwarnings("ignore")

def load_text_to_chroma(chunk_size, chunk_overlap, cache_dir): 
    all_shakespeare = GutenbergLoader("https://www.gutenberg.org/cache/epub/100/pg100.txt").load()
    
    splitter = DialogueSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator="\n\n\n")
    documents = splitter.split_documents(all_shakespeare)
    
    vector_database = ChromaDB()
    vector_database.load_documents(documents)   
    return vector_database

def initialize_conversation(character_a, character_b, model, token,  vector_database): 
    a = ShakespeareCharacter(character_a, character_b, model, token, vector_database)
    b = ShakespeareCharacter(character_b, character_a, model, token, vector_database)
    return a, b

def converse(character_a, character_b, starting_query, num_conversations): 
    memory = {}
    current_character = character_a
    response = character_a.get_response(starting_query)
    memory[f"0. {character_a.character}"] = response

    for i in range(1, num_conversations):
        current_character = character_b if current_character == character_a else character_a
        response = current_character.get_response(response)
        memory[f"{i}. {current_character.character}"] = response
    return memory

def main(args): 
    vector_database = load_text_to_chroma(args.chunk_size, args.chunk_overlap, args.cache_dir)
    character_a, character_b = initialize_conversation(args.character_a, args.character_b, args.model, args.token, vector_database)
    memory = converse(character_a, character_b, args.starting_query, args.num_conversations)
    return memory


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Creating conversations between different Shakespeare characters.")
    parser.add_argument("--model", type=str, default="meta-llama/Meta-Llama-3-70B-Instruct")
    parser.add_argument("--embedding-model", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--cache_dir", type=str, default="./data")
    parser.add_argument("--token", type=str, default="")
    parser.add_argument("--chunk_size", type=int, default=512)
    parser.add_argument("--chunk_overlap", type=int, default=128)
    parser.add_argument("--character-a", type=str, default="Romeo")
    parser.add_argument("--character-b", type=str, default="Hamlet")
    parser.add_argument("--starting-query", type=str, default="Hello! How are you?")
    parser.add_argument("--num_conversations", type=int, default=3)
    parser.add_argument("--load_from_disk", type=bool, default=True)
    args = parser.parse_args()

    main(args)
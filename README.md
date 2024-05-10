# Shakespeare Character Dialogue Generator

This project utilizes two Large Language Models (LLMs) to generate a conversation between two characters from Shakespeare's plays. Users can input the names of any two Shakespeare characters, and the LLMs will create a dialogue based on their personalities, traits, and the context of the plays they appear in.

A fun little project. 

### Features

- Generates a realistic conversation between two Shakespeare characters
- Allows users to input any characters from Shakespeare's works

### Installation and Prerequisites 

1. Clone the repository
```git clone <repo link>.git```

2. Install the required dependencies (as specified in the `pyproject.toml`). 
```poetry install```

3. Obtain tokens necessary from Hugging Face. [Link to Hugging Face documentation](https://huggingface.co/docs/hub/en/security-tokens). 

### Usage

```
python main.py [--model MODEL] [--embedding-model EMBEDDING_MODEL] [--cache_dir CACHE_DIR] [--token TOKEN]
               [--chunk_size CHUNK_SIZE] [--chunk_overlap CHUNK_OVERLAP] [--character-a CHARACTER_A]
               [--character-b CHARACTER_B] [--starting-query STARTING_QUERY] [--num_conversations NUM_CONVERSATIONS]
```

Optional arguments:

`--model`: The LLM to use for generating responses (default: "meta-llama/Meta-Llama-3-70B-Instruct").
`--embedding-model`: The embedding model to use for text similarity (default: "sentence-transformers/all-MiniLM-L6-v2").
`--cache_dir`: The directory to cache the downloaded Shakespeare texts (default: "./data").
`--token`: The API token for the LLM (default: "").
`--chunk_size`: The size of the text chunks to process (default: 512).
`--chunk_overlap`: The overlap between text chunks (default: 128).
`--character-a`: The name of the first Shakespeare character (default: "Romeo").
`--character-b`: The name of the second Shakespeare character (default: "Hamlet").
`--starting-query`: The initial query to start the conversation (default: "Hello! How are you?").
`--num_conversations`: The number of conversation turns to generate (default: 10).

### Example

Here is an example of how to run this generator: 
```
python converse.py --character-a "Othello" --character-b "Desdemona" --starting-query "My love, how fare thee on this fine day?" --num_conversations 5
```
This command will generate a conversation between Othello and Desdemona, starting with the query "My love, how fare thee on this fine day?" and generating 5 conversation turns.

### Contributing
Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

### License
This project is licensed under the MIT License.
Acknowledgements

Langchain for providing the document loaders and utilities.
Gutenberg Project for providing the Shakespeare texts.
The works of William Shakespeare for providing the inspiration and characters for this project.
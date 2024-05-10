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
`--load_from_disk`: Whether to load from cache_dir (default: True)

### Example

Here is an example of how to run this generator: 
```
python converse.py --character-a "Othello" --character-b "Desdemona" --starting-query "My love, how fare thee on this fine day?" --num_conversations 3
```
This command will generate a conversation between Othello and Desdemona. This is the result from a run (note: you are not guaranteed this exact result due to the nature of LLMs). 

```
Othello: 
O, my fair Desdemona, thou dost ask how I fare on this fine day? Verily, I fare most wretchedly, for my mind is beset with dark thoughts and my heart doth ache with jealousy. The Moor's blood in me doth boil with passion, and I fear that I am not master of my own emotions. Forgive me, my love, for I am but a man, and a man consumed by love and doubt. Howbeit, thy presence doth bring me solace, and in thine eyes, I see a love that doth calm the tempests of my soul. Pray, tell me, how doth thy day fare? Doth thy love for me still burn bright, or hath it waned, like the fleeting sun that doth set in the west?


Desdemona: 
My dear Othello, I am deeply troubled by thy words, for they bespeak a darkness in thy heart that doth frighten me. Thou dost speak of jealousy and doubt, and thy words do cut me to the quick. I do confess, my love, that I am perplexed by thy behavior of late, for thou hast been distant and cold towards me. But I do implore thee, my lord, to banish these dark thoughts from thy mind, for they doth consume thee, and I fear for thy well-being. Thou dost ask if my love for thee hath waned, and I do assure thee, my love, that it hath not. I do love thee dearly, and I shall ever love thee, till my dying breath. But I do beseech thee, my lord, to tell me what doth trouble thee, that we may confront it together, and emerge stronger and more in love than ever.

Othello: 
O, fair Desdemona, thou dost speak words of love and devotion, but I fear they come too late. My heart is consumed by the fire of jealousy, and I am convinced that thou hast betrayed me with Cassio. Iago, my trusted friend and advisor, hath shown me proof of thy infidelity, and I am resolved to take revenge upon thee. Thou dost protest thy innocence, but I will not be swayed. Thou art false, Desdemona, and thou shalt pay the price for thy deceit.
```

### Contributing
Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

### License
This project is licensed under the MIT License.
Acknowledgements

Langchain for providing the document loaders and utilities.
Gutenberg Project for providing the Shakespeare texts.
The works of William Shakespeare for providing the inspiration and characters for this project.
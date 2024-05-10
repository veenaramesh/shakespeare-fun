from langchain.text_splitter import TextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


class DialogueSplitter(TextSplitter): 
    def __init__(self, separator="\n\n", is_separator_regex=False, **kwargs): 
        super().__init__(**kwargs)
        self._separator = separator
        self._is_separator_regex = is_separator_regex

    def split_text(self, text):
        separator = self._separator
        per_scene = []
        dialogues = []
        current_character = None
        current_dialogue = ""
        current_chars = 0
        max_chars = 1024

        def append_dialogue(dialogue):
            nonlocal current_chars
            if current_chars + len(dialogue) + 1 <= max_chars:
                dialogues.append(dialogue)
                current_chars += len(dialogue) + 1
            else:
                per_scene.append('\n '.join(dialogues))
                dialogues.clear()
                current_chars = 0
                dialogues.append(dialogue)
                current_chars = len(dialogue) + 1

        for line in text.split(separator):
            line = line.strip()
            if line.isupper() and line.endswith("."):
                # character
                if current_character and current_dialogue:
                    # Remove scene setting description from the end of the dialogue
                    current_dialogue = current_dialogue.strip()
                    if current_dialogue.endswith("]"):
                        current_dialogue = current_dialogue[:current_dialogue.rfind("[")].strip()
                    append_dialogue(current_character + ": " + current_dialogue)
                current_character = line[:-1]
                current_dialogue = ""
            elif line == "":
                if current_character and current_dialogue:
                    # Remove scene setting description from the end of the dialogue
                    current_dialogue = current_dialogue.strip()
                    if current_dialogue.endswith("]"):
                        current_dialogue = current_dialogue[:current_dialogue.rfind("[")].strip()
                    append_dialogue(current_character + ": " + current_dialogue)
                current_character = None
                current_dialogue = ""
            elif 'SCENE' in line:
                if dialogues:
                    per_scene.append('\n '.join(dialogues))
                    dialogues.clear()
                    current_chars = 0
            else:
                current_dialogue += line + " "

        if current_character and current_dialogue:
            # Remove scene setting description from the end of the dialogue
            current_dialogue = current_dialogue.strip()
            if current_dialogue.endswith("]"):
                current_dialogue = current_dialogue[:current_dialogue.rfind("[")].strip()
            append_dialogue(current_character + ": " + current_dialogue)

        if dialogues:
            per_scene.append('\n '.join(dialogues))

        return per_scene


class ChromaDB: 
    def __init__(self, model="sentence-transformers/all-MiniLM-L6-v2", cache_dir="./data"): 
        self.model = model 
        self.cache_dir = cache_dir
        self.vectordb = None 

    def get_embeddings(self): 
        embedding = HuggingFaceEmbeddings(
            model_name=self.model, 
            cache_folder=self.cache_dir
        )
        return embedding
    
    def load_documents(self, documents):
        # create the vector database using chroma and cache
        embedding = self.get_embeddings()

        vectordb = Chroma.from_documents(
            documents, 
            embedding, 
            persist_directory=self.cache_dir
        )
        # persist vector database to make retrieval later on quicker
        vectordb.persist()
        self.vectordb = vectordb

    def get_top_k_documents(self, query, k=10): 
        if self.vectordb: 
            # perform similarity search and get 3 best dialogue options
            docs = self.vectordb.similarity_search(query, k=k)
            return docs 
        else: 
            return None



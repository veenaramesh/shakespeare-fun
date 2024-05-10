from langchain.text_splitter import TextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


class DialogueSplitter(TextSplitter): 
    """
    A custom text splitter for splitting dialogues into separate scenes and dialogues.

    Args:
    separator (str, optional): The separator used to split the text. Defaults to "\n\n".
    is_separator_regex (bool, optional): Whether the separator is a regex pattern. Defaults to False.
    **kwargs: Additional keyword arguments for the TextSplitter class.

    Attributes:
    _separator (str): The separator used to split the text.
    _is_separator_regex (bool): Whether the separator is a regex pattern.

    Methods:
    split_text(text):
        Splits the input text into separate scenes and dialogues based on the specified separator.

    Returns:
    list: A list of strings, where each string represents a separate scene or dialogue.
    """

    def __init__(self, separator="\n\n", is_separator_regex=False, **kwargs): 
        """
        Initializes a DialogueSplitter object with the specified separator and optional regex flag.

        Args:
        separator (str, optional): The separator used to split the text. Defaults to "\n\n".
        is_separator_regex (bool, optional): Whether the separator is a regex pattern. Defaults to False.
        **kwargs: Additional keyword arguments for the TextSplitter class.

        Attributes:
        _separator (str): The separator used to split the text.
        _is_separator_regex (bool): Whether the separator is a regex pattern.
        """
        super().__init__(**kwargs)
        self._separator = separator
        self._is_separator_regex = is_separator_regex

    def split_text(self, text):
        """
        Splits the input text into separate scenes and dialogues based on the specified separator.

        Args:
        text (str): The input text to be split into separate scenes and dialogues.

        Returns:
        list: A list of strings, where each string represents a separate scene or dialogue.
        """
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
        """
        Initializes a ChromaDB object with the specified model and cache directory.

        Args:
        model (str, optional): The HuggingFace model to use for embeddings. Defaults to "sentence-transformers/all-MiniLM-L6-v2".
        cache_dir (str, optional): The directory to cache the embeddings. Defaults to "./data".

        Attributes:
        model (str): The HuggingFace model to use for embeddings.
        cache_dir (str): The directory to cache the embeddings.
        vectordb (Chroma, optional): The vector database object, if it has been loaded.
        """
        self.model = model 
        self.cache_dir = cache_dir
        self.vectordb = None 

    def get_embeddings(self): 
        """
        Returns the HuggingFace embeddings object used for vector database.

        Returns:
        HuggingFaceEmbeddings: The HuggingFace embeddings object used for vector database.
        """
        embedding = HuggingFaceEmbeddings(
            model_name=self.model, 
            cache_folder=self.cache_dir
        )
        return embedding

    def load_documents(self, documents):
        """
        Loads the provided documents into a vector database using Chroma and caches it.

        Args:
        documents (list): A list of documents to be loaded into the vector database.

        Returns:
        None: This method does not return any value. It only loads the documents into the vector database.

        Raises:
        None: This method does not raise any exceptions.

        Usage:
        db = ChromaDB()
        db.load_documents(["document1", "document2", "document3"])
        """

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
        """
        Performs a similarity search in the vector database and returns the top k documents.

        Args:
        query (str): The query string for the similarity search.
        k (int, optional): The number of top documents to return. Defaults to 10.

        Returns:
        list: A list of the top k documents based on similarity to the query.

        Raises:
        None: This method does not raise any exceptions.

        Usage:
        db = ChromaDB()
        db.load_documents(["document1", "document2", "document3"])
        top_k_docs = db.get_top_k_documents("example query", 5)
        """

        if self.vectordb: 
            # perform similarity search and get 3 best dialogue options
            docs = self.vectordb.similarity_search(query, k=k)
            return docs 
        else: 
            return None

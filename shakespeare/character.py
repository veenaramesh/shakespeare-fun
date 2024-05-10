from huggingface_hub import InferenceClient

class ShakespeareCharacter: 
    def __init__(self,character, other_character, model, token, vectordb): 
        self.character = character
        self.other_character = other_character
        self.vectordb = vectordb
        self.client = InferenceClient(model=model, token=token) # meta-llama/Meta-Llama-3-70B-Instruct
 
    def get_retrieved_documents(self, query): 
        retrieved_docs = self.vectordb.get_top_k_documents(query, k=3)
        docs = ""
        for i in range(0, len(retrieved_docs)): 
            docs += f"Dialogue Snippet {i + 1}: \n" + retrieved_docs[i].page_content + "\n"
        return docs
    
    def get_response_helper(self, query, context): 
        template = f"""
        ### Instruction ###
        Answer the question pretending to be {self.character} and that I am pretending to be {self.other_character} from the Shakespeare play. Please use the context, which contains three snippets of dialogue from Shakespeare's plays about {self.character}, to answer the question. Answer only as {self.character}.

        ### Question ###
        {query}
        
        ### Context ###
        {context}
        """
        return template 
    
    def get_response(self, query="Hello. "): 
        context = self.get_retrieved_documents(query)
        prompt = self.get_response_helper(query, context)
        response = self.client.text_generation(prompt, max_new_tokens=200)
        print(f"{self.character}: {response}")
        return response


           

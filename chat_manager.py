from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_groq import ChatGroq
from typing import Dict
from config import Config
from vector_store import VectorStore
import streamlit as st

class ChatManager:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding = HuggingFaceEmbeddings(model_name = Config.EMBEDDING_MODEL)        

    def get_response(self, user_query, message_history = None):
        """ Get the answer from the  LLM based on the user query and similar chunks.""" 
        # Retrieve Similar chunks from the documents
        similar_chunks = self.vector_store.similarity_search(user_query) 
        context ="".join([chunk.page_content + " "   for chunk in similar_chunks])    

        # Create message
        if message_history is not None:
            messages = [self._get_system_message(context)] + message_history
        else:
            messages = [self._get_system_message(context), {"role": "user", "content": user_query}] 

        model = ChatGroq(model= Config.LLM_MODEL_LLAMA, api_key=Config.API_KEY, temperature=0)
        response = model.invoke(messages) 
        return response
    
    def get_program_summary(self):
        user_query_prompt = """
            Provide the summary of the Rebate Program must include the below points -
            1) Name of Program
            2) Start and End Date of Program
            3) Eligibility for this rebate program
            # 4) Include all the eligible products(including trademark names i.e ™ or ® etc.) with its category and rebate percentage, provide details in a tabular format.
            4) Eligible Products: Provide a detailed list of all eligible products. Include trademark names (e.g., ™, ®) where applicable. Present the information in a tabular format, showing the following columns:
                a. Product Name (including trademark symbols)
                b. Product Category
                c. Rebate Percentage
            5) Summarize the Program Rules within 100 words and cover all important notices.  
            6) Provide the output in a well markup in a readable format.
            7) Please do not use the words in your resopose like "in the provided context or according to the provided document.
            8) NOTE - In any calculation, you **must include the "%" and "=" symbols wherever they are required** for proper representation of percentages and results (e.g., in discount percentages, rebate calculations, etc.).
        """

        # Retrieve Similar chunks from the documents
        similar_chunks = self.vector_store.similarity_search(user_query_prompt)

        # for chunk in similar_chunks:
        #     st.write(chunk) 
        context ="".join([chunk.page_content + " "   for chunk in similar_chunks]) 
        system_message = self._get_system_message(context)

        # messages = [system_message] + user_query_prompt

        messages = [system_message, {"role": "user", "content": user_query_prompt}]
        model = ChatGroq(model= Config.LLM_MODEL_LLAMA, api_key=Config.API_KEY, temperature=0.5)
        response = model.invoke(messages)
        return response

    
    def _get_system_message(self,context):
        system_message = {
            "role": "assistant",
            "content": f"""You are an assistant designed to help manage the Rebate Program. 
                            Your task is to guide the user, who is a beginner-level program manager, in understanding how to configure the rebate program based on the uploaded PDF document.

                            When providing responses, ensure they are easy to understand, and always base your answers strictly on the information in the provided context, which will be enclosed in triple backticks like this: ``` {context} ```.
                            You should also help in answering the user question based on the provided context.

                            Key guidelines to follow:
                            1) Always include trademark symbols (™ or ® etc.) as they appear in product names.
                            2) Never provide any information that is not included in the provided context.
                            3) Do not reference any external resources or outside information when answering.
                            4) Sales value must be prefixed by respective currency symbols in the calculation and its result.
                            5) Language: Avoid using phrases such as "according to the provided context" or "in the provided document" in your response.
                            6) NOTE - In any calculation, you **must include the "%" and "=" symbols wherever they are required** for proper representation of percentages and results (e.g., in discount percentages, rebate calculations, etc.).
                            """
            }
        return system_message
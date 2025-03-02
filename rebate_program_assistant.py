import streamlit as st
import torch

from chat_manager import ChatManager

st.header("Smart Rebate Program Assistant")
st.markdown("*A smart way to get details about rebate program and configure it.*")
st.write("---")

class RebateProgramAssistant:
    def __init__(self):
        self.chat_manager = ChatManager()
        self.user_query = None
        self.rebate_program_summary = None

        if "messages" not in st.session_state:
            st.session_state.messages = [] 

    def display_chats(self):
        """Display chat messages from session state."""
        with st.spinner("Loading chat history.."):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    def load_program_summary(self):
        """Load the rebate program summary only once after the file is uploaded."""
        if self.rebate_program_summary is None:
            with st.spinner("Preparing Rebate Program Summary.."):
                self.rebate_program_summary = self.chat_manager.get_program_summary()
                return self.rebate_program_summary
        return self.rebate_program_summary

    def main(self):  
        # Check if a file has been uploaded and processed
        if "file_upload" not in st.session_state or st.session_state.file_upload is None:
            st.info("Please upload a PDF file in the sidebar to begin the Rebate Program.")
            return
        
        if not st.session_state.saved_vector_embedding:
            st.warning("Your file is still being processed. Please wait...")
            return

        # File is uploaded and processed, now show the assistant
        # Load the rebate summary
        summary_button = st.button("Load Program Summary")
        if summary_button:
            summary = self.load_program_summary()
            if summary:
                st.markdown(summary.content)
                st.markdown("---")
        
        # Always show the chat interface if the file is processed
        st.subheader("Chat with Rebate Program Assistant")
        self.display_chats()

        # Perform similarity search
        self.user_query = st.chat_input("Enter your query")
        
        if self.user_query is not None:
            with st.spinner("Processing your query.."):
                user_message = {"role": "user", "content": self.user_query}
                st.session_state.messages.append(user_message)

                with st.chat_message("user"):
                    st.markdown(self.user_query)
                
                # messages
                message_history = [{"role": message["role"], "content": message["content"]} for message in st.session_state.messages]
                
                result = self.chat_manager.get_response(self.user_query, message_history)

                with st.chat_message("assistant"):
                    st.write(result.content)
                    assistantMessage = {"role": "assistant", "content": result.content}
                    st.session_state.messages.append(assistantMessage) 

# When this page is loaded through navigation, run the assistant
if __name__ == "__main__":
    torch.classes.__path__ = [] 

# Always instantiate and run the assistant when this file is loaded through navigation
rebate_assistant = RebateProgramAssistant()
rebate_assistant.main()
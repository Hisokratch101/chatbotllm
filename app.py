import streamlit as st
import os
from typing import List

from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv

# Import the custom agricultural chatbot class
from chatbot import MoroccanAgricultureAssistant

class MoroccanFarmAssistantApp:
    """
    Streamlit application for Moroccan Agricultural Support.
    
    Provides an interactive web interface for farmers, agricultural 
    professionals, and agricultural development stakeholders.
    """
    
    def __init__(self):
        """
        Initialize Streamlit application configuration and state.
        """
        # Load environment variables
        load_dotenv()
        
        # Configure page settings
        st.set_page_config(
            page_title="مساعد الفلاحة المغربية",
            page_icon="🌾",
            layout="wide"
        )
        
        # Initialize agricultural assistant
        self.initialize_agricultural_assistant()
        
        # Initialize session state for conversation
        self.initialize_session_state()
    
    def initialize_agricultural_assistant(self):
        """
        Create specialized agricultural assistant instance.
        """
        try:
            self.agricultural_assistant = MoroccanAgricultureAssistant(
                api_key=os.getenv('GROQ_API_KEY'),
                temperature=st.session_state.get('temperature', 0.7),
                max_tokens=st.session_state.get('max_tokens', 256)
            )
        except ValueError as e:
            st.error(f"Assistant Initialization Error: {e}")
            st.stop()
    
    def initialize_session_state(self):
        """
        Set up initial session state for conversation tracking.
        """
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "temperature" not in st.session_state:
            st.session_state.temperature = 0.7
        
        if "max_tokens" not in st.session_state:
            st.session_state.max_tokens = 256
    
    def render_sidebar(self):
        """
        Create configuration sidebar with agricultural-specific parameters.
        """
        st.sidebar.title("🚜 إعدادات المساعد الفلاحي")
        
        # Agricultural region selection
        st.session_state.region = st.sidebar.selectbox(
            "المنطقة الفلاحية:",
            [
                "سوس ماسة",
                "الغرب",
                "الدوكالة",
                "الشاوية ورديغة",
                "بني أحسن",
                "أخرى"
            ]
        )
        
        # Crop type selection
        st.session_state.crop_type = st.sidebar.selectbox(
            "نوع المحصول:",
            [
                "الحبوب",
                "الزيتون",
                "الحمضيات",
                "الطماطم",
                "الأرغان",
                "التمور",
                "الزعفران"
            ]
        )
        
        # Temperature and creativity slider
        st.session_state.temperature = st.sidebar.slider(
            "مستوى الإبداع (الحرارة):", 
            0.0, 1.0, 
            st.session_state.temperature
        )
        
        # File upload for specific agricultural data
        uploaded_file = st.sidebar.file_uploader(
            "تحميل ملف البيانات الزراعية:", 
            type=["txt", "csv", "xlsx"]
        )
        
        return uploaded_file
    
    def display_chat_history(self):
        """
        Render conversation messages in the chat interface.
        """
        for msg in st.session_state.messages:
            if isinstance(msg, HumanMessage):
                st.chat_message("user", avatar="🌱").write(msg.content)
            elif isinstance(msg, AIMessage):
                st.chat_message("assistant", avatar="🚜").write(msg.content)
    
    def process_user_input(self, user_input: str, context_file=None):
        """
        Process user input and generate agricultural response.
        
        Args:
            user_input (str): User's message
            context_file (UploadedFile, optional): Uploaded context file
        """
        if not user_input.strip():
            st.warning("أدخل رسالة من فضلك (Please enter a message)")
            return
        
        # Prepare context from file if uploaded
        context = None
        if context_file:
            try:
                context = context_file.getvalue().decode("utf-8")
            except Exception as e:
                st.error(f"خطأ في قراءة الملف: {e}")
        
        # Enhance input with regional and crop context
        enhanced_input = (
            f"أنا فلاح من منطقة {st.session_state.region}, "
            f"أزرع {st.session_state.crop_type}. "
            f"{user_input}"
        )
        
        # Translate and prepare messages
        translated_input = self.agricultural_assistant.translate_prompt(
            "Darija", 
            enhanced_input
        )
        
        # Prepare messages for response generation
        messages = st.session_state.messages + [
            HumanMessage(content=translated_input)
        ]
        
        # Manage conversation context
        messages = self.agricultural_assistant.manage_conversation_context(messages)
        
        # Generate response
        with st.spinner("جاري توليد الجواب... (Generating response...)"):
            try:
                response = self.agricultural_assistant.generate_response(
                    messages, 
                    context
                )
                
                # Add messages to conversation history
                st.session_state.messages.extend([
                    HumanMessage(content=translated_input),
                    AIMessage(content=response)
                ])
                
                # Display response
                st.chat_message("assistant", avatar="🚜").write(response)
            
            except Exception as e:
                st.error(f"فشل توليد الرد: {e}")
    
    def run(self):
        """
        Main application runner.
        """
        st.title("🌾 مساعد الفلاحة المغربية")
        st.subheader("مساعدك الذكي في عالم الفلاحة")
        
        # Render sidebar and get context file
        context_file = self.render_sidebar()
        
        # Display conversation history
        self.display_chat_history()
        
        # User input
        user_input = st.chat_input("اكتب سؤالك هنا...")
        
        # Process user input
        if user_input:
            self.process_user_input(user_input, context_file)

def main():
    """
    Entry point for the Moroccan Agricultural Assistant application.
    """
    app = MoroccanFarmAssistantApp()
    app.run()

if __name__ == "__main__":
    main()
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from langchain.memory import ConversationBufferMemory

class MoroccanAgricultureAssistant:
    """
    Specialized AI Assistant for Moroccan Agricultural Support
    
    Provides expert guidance on:
    - Crop management
    - Sustainable farming practices
    - Local agricultural challenges
    - Regional crop optimization
    """
    
    def __init__(self, 
                 api_key: str = None, 
                 model_name: str = "llama-3.1-70b-versatile",
                 temperature: float = 0.7,
                 max_tokens: int = 256):
        """
        Initialize the agricultural assistant with specialized configuration.
        
        Args:
            api_key (str): Groq API key for authentication
            model_name (str): Name of the language model
            temperature (float): Creativity level of responses
            max_tokens (int): Maximum token limit for responses
        """
        # Load environment variables
        load_dotenv()
        
        # Prioritize passed API key, then environment variable
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("No API key provided. Set GROQ_API_KEY in .env or pass directly.")
        
        # Initialize language model with agricultural context
        self.llm = ChatGroq(
            model_name=model_name,
            groq_api_key=self.api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Specialized agricultural knowledge base
        self.agricultural_context = self._load_agricultural_knowledge()
    
    def _load_agricultural_knowledge(self) -> str:
        """
        Load contextual knowledge about Moroccan agriculture.
        
        Returns:
            str: Comprehensive context about Moroccan agricultural practices
        """
        return """
        Moroccan Agricultural Context:
        - Primary agricultural regions: Souss-Massa, Gharb, Doukkala
        - Key crops: Wheat, barley, citrus, olives, tomatoes
        - Challenges: Water scarcity, climate change, soil degradation
        - Sustainable practices: Drip irrigation, crop rotation, organic farming
        - Traditional crops: Argan, date palms, saffron
        - Livestock: Sheep, goats, camels in pastoral regions
        """
    
    def generate_response(self, 
                          messages: List[BaseMessage], 
                          context: str = None) -> str:
        """
        Generate an intelligent agricultural response.
        
        Args:
            messages (List[BaseMessage]): Conversation history
            context (str, optional): Additional context for the response
        
        Returns:
            str: Generated AI response with agricultural expertise
        """
        try:
            # Combine agricultural context with user messages
            enhanced_context = f"{self.agricultural_context}\n\n"
            if context:
                enhanced_context += f"User-provided context: {context}\n\n"
            
            # Prepare messages with enhanced context
            enhanced_messages = messages + [
                HumanMessage(content=enhanced_context)
            ]
            
            # Generate response
            response = self.llm.invoke(enhanced_messages)
            return self._format_agricultural_response(response.content)
        
        except Exception as e:
            return f"Khata fi l-internet: {str(e)} (Error in processing)"
    
    def _format_agricultural_response(self, response: str) -> str:
        """
        Format response with Moroccan Darija agricultural terminology.
        
        Args:
            response (str): Original AI-generated response
        
        Returns:
            str: Localized response in Darija-influenced language
        """
        darija_translations = {
            "crop": "zra3a",
            "farm": "mzra3a",
            "water": "l-ma",
            "soil": "trab",
            "harvest": "l-hassad",
            "fertilizer": "l-khmad",
            "irrigation": "s-saqaya"
        }
        
        # Simple localization of key terms
        for english, darija in darija_translations.items():
            response = response.replace(english, darija)
        
        return f"📡 Marhaba, hada l-jawab dyalk:\n\n{response}"
    
    def manage_conversation_context(self, 
                                    messages: List[BaseMessage], 
                                    max_context_tokens: int = 1000) -> List[BaseMessage]:
        """
        Manage conversation context with agricultural specificity.
        
        Args:
            messages (List[BaseMessage]): Current conversation messages
            max_context_tokens (int): Maximum tokens to retain
        
        Returns:
            List[BaseMessage]: Trimmed conversation context
        """
        def count_tokens(msg: BaseMessage) -> int:
            return len(msg.content.split())
        
        total_tokens = sum(count_tokens(msg) for msg in messages)
        
        while total_tokens > max_context_tokens and messages:
            removed_message = messages.pop(0)
            total_tokens -= count_tokens(removed_message)
        
        return messages
    
    def translate_prompt(self, language: str, prompt: str) -> str:
        """
        Translate and adapt prompts for agricultural context.
        
        Args:
            language (str): Target language
            prompt (str): Original prompt
        
        Returns:
            str: Language-specific agricultural prompt
        """
        language_prefixes = {
            "Darija": "Shkun 3awn l-fellah: ",  # Agricultural helper
            "Français": "Aide agricole au Maroc : ",
            "العربية": "مساعد زراعي: ",
            "Anglais": "Moroccan Agricultural Advisor: "
        }
        
        return language_prefixes.get(language, "Agricultural Advice: ") + prompt
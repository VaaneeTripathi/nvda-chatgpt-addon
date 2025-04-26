import json
import os
import config
from logHandler import log

# Path for storing user settings
CONFIG_PATH = os.path.join(config.getUserConfigPath(), "addons", "chatGPTAddon")

class ChatGPTInterface:
    """
    Handles communication with the ChatGPT API.
    """
    
    def __init__(self):
        # Create config directory if it doesn't exist
        if not os.path.exists(CONFIG_PATH):
            try:
                os.makedirs(CONFIG_PATH)
            except Exception as e:
                log.error(f"Error creating config directory: {e}")
        
        # Default settings
        self.api_key = "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"
        self.model = "gpt-4.1"
        self.max_tokens = 1000
        
        # Load settings if they exist
        self.load_settings()

    def load_settings(self):
        """
        Load settings from a config file
        """

        config_file = os.path.join(CONFIG_PATH, "settings.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    settings = json.load(f)
                    self.api_key = settings.get("api_key", "")
                    self.model = settings.get("model", "gpt-3.5-turbo")
                    self.max_tokens = settings.get("max_tokens", 1000)
            except Exception as e:
                log.error(f"Error loading settings: {e}")

    def save_settings(self):
        """
        Save settings to config file
        """

        config_file = os.path.join(CONFIG_PATH, "settings.json")
        try:
            with open(config_file, "w") as f:
                settings = {
                    "api_key": self.api_key,
                    "model": self.model,
                    "max_tokens": self.max_tokens
                }
                json.dump(settings, f)
        except Exception as e:
            log.error(f"Error saving settings: {e}")

    def send_query(self, query):
        """
        Send query to chatgpt API (right now, dummy application)

         Args:
            query (str): The user's query
        
        Returns:
            str: The response from ChatGPT
        """

        # Check if API key is set
        if not self.api_key:
            return "API key not set. Please set your API key in the settings."
        
        # TODO: Implement actual API communication
        # For now, just return a mock response
        return f"This is a mock response to your query: '{query}'"    
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
        Send query to ChatGPT API and return the response.
        
        Args:
            query (str): The user's query
            
        Returns:
            str: The response from ChatGPT
        """
        import urllib.request
        import urllib.error
        import json
        
        # Check if API key is set
        if not self.api_key:
            return _("API key not set. Please set your API key in the settings.")
        
        # OpenAI API endpoint for chat completions
        url = "https://api.openai.com/v1/chat/completions"
        
        # Prepare the request data
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": query}],
            "max_tokens": self.max_tokens,
            "temperature": 0.7
        }
        
        # Convert data to JSON
        json_data = json.dumps(data).encode('utf-8')
        
        # Set up the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            # Create the request
            req = urllib.request.Request(url, data=json_data, headers=headers)
            
            # Send the request and get the response
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = response.read()
                response_json = json.loads(response_data)
                
                # Extract the response text
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    message = response_json["choices"][0]["message"]
                    if "content" in message:
                        return message["content"].strip()
                    else:
                        return _("Received empty response from ChatGPT.")
                else:
                    return _("Unexpected response format from ChatGPT.")
        
        except urllib.error.HTTPError as e:
            # Handle HTTP errors
            try:
                error_data = json.loads(e.read())
                if "error" in error_data and "message" in error_data["error"]:
                    error_message = error_data["error"]["message"]
                else:
                    error_message = str(e)
            except:
                error_message = str(e)
            
            log.error(f"HTTP error when calling ChatGPT API: {error_message}")
            return _("Error communicating with ChatGPT: {error}").format(error=error_message)
        
        except Exception as e:
            # Handle other errors
            log.error(f"Error when calling ChatGPT API: {str(e)}")
            return _("Error: {error}").format(error=str(e))
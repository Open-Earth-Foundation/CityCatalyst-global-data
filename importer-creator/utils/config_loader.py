import yaml
import os
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Configuration loader for model and API settings."""
    
    _config = None
    _config_path = Path(__file__).parent.parent / "config.yaml"
    
    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if cls._config is None:
            try:
                with open(cls._config_path, 'r', encoding='utf-8') as file:
                    cls._config = yaml.safe_load(file)
            except FileNotFoundError:
                raise FileNotFoundError(f"Configuration file not found at {cls._config_path}")
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing configuration file: {e}")
        return cls._config
    
    @classmethod
    def get_model_config(cls, model_key: str) -> str:
        """Get model configuration by key (e.g., 'BIG_MODEL', 'SMALL_MODEL')."""
        config = cls.load_config()
        
        if model_key in config['models']:
            return config['models'][model_key]
        
        raise ValueError(f"Model key '{model_key}' not found in configuration")
    
    @classmethod
    def get_base_url(cls) -> str:
        """Get the OpenRouter base URL."""
        config = cls.load_config()
        return config['models']['base_url']
    
    @classmethod
    def get_temperature(cls) -> float:
        """Get the model temperature setting."""
        config = cls.load_config()
        return config['models']['temperature']
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API configuration settings."""
        config = cls.load_config()
        return config.get('api', {})
    
    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        """Get OpenRouter headers for site rankings."""
        config = cls.load_config()
        headers = config.get('headers', {})
        
        # Convert to the format expected by OpenRouter
        openrouter_headers = {}
        if headers.get('http_referer'):
            openrouter_headers['HTTP-Referer'] = headers['http_referer']
        if headers.get('x_title'):
            openrouter_headers['X-Title'] = headers['x_title']
            
        return openrouter_headers
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get OpenRouter API key from environment variable."""
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable not set. "
                "Please set it to your OpenRouter API key."
            )
        return api_key
    
    @classmethod
    def get_big_model(cls) -> str:
        """Get the BIG_MODEL for complex data analysis and coding tasks."""
        return cls.get_model_config('BIG_MODEL')
    
    @classmethod
    def get_small_model(cls) -> str:
        """Get the SMALL_MODEL for structured output and simple tasks."""
        return cls.get_model_config('SMALL_MODEL')
    
    @classmethod
    def get_embeddings_model(cls) -> str:
        """Get the model to use for embeddings."""
        return cls.get_model_config('EMBEDDINGS_MODEL') 
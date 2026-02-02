"""
Configuration Management for Health Chatbot
Loads environment variables and provides centralized config access
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # API Keys (Never hardcoded!)
    USDA_API_KEY = os.getenv('USDA_API_KEY')
    RAPID_API_KEY = os.getenv('RAPID_API_KEY')
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/chatbot.db')
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    STATIC_DIR = BASE_DIR / 'static'
    TEMPLATES_DIR = BASE_DIR / 'templates'
    
    # Data Files
    INTENTS_FILE = DATA_DIR / 'intents.json'
    DISEASES_FILE = DATA_DIR / 'diseases.json'
    MENTAL_HEALTH_FILE = DATA_DIR / 'mental_health_qa.json'
    FITNESS_FILE = DATA_DIR / 'fitness_qa.json'
    NUTRITION_FILE = DATA_DIR / 'nutrition_tips.json'
    
    # API Endpoints
    USDA_API_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    EXERCISE_API_URL = 'https://exercisedb.p.rapidapi.com/exercises'
    QUOTES_API_URL = 'https://type.fit/api/quotes'
    
    # Chatbot Settings
    FUZZY_MATCH_THRESHOLD = 0.6  # Minimum similarity score for intent matching
    MAX_CHAT_HISTORY = 100  # Maximum messages to store per user
    
    # Session Configuration
    SESSION_COOKIE_SECURE = FLASK_ENV == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 60 * 60  # 7 days in seconds
    
    @staticmethod
    def validate_api_keys():
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not Config.USDA_API_KEY:
            missing_keys.append('USDA_API_KEY')
        if not Config.RAPID_API_KEY:
            missing_keys.append('RAPID_API_KEY')
        
        if missing_keys:
            print(f"⚠️  Warning: Missing API keys: {', '.join(missing_keys)}")
            print("   Some features may not work. Please add them to your .env file.")
            return False
        return True
    
    @staticmethod
    def check_data_files():
        """Check if all required data files exist"""
        required_files = [
            Config.INTENTS_FILE,
            Config.DISEASES_FILE,
            Config.MENTAL_HEALTH_FILE,
            Config.FITNESS_FILE,
            Config.NUTRITION_FILE
        ]
        
        missing_files = [f for f in required_files if not f.exists()]
        
        if missing_files:
            print(f"⚠️  Warning: Missing data files: {[str(f.name) for f in missing_files]}")
            return False
        return True


# Validate configuration on import
if __name__ != '__main__':
    Config.validate_api_keys()
    Config.check_data_files()

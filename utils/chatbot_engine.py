"""
Chatbot Engine - Core NLP and Response Logic
Handles intent matching, pattern recognition, and response generation
"""

import json
import random
import difflib
from pathlib import Path
from config.settings import Config


class ChatbotEngine:
    """Main chatbot logic engine"""
    
    def __init__(self):
        """Initialize chatbot with all data sources"""
        self.intents = self._load_json(Config.INTENTS_FILE)
        self.diseases = self._load_json(Config.DISEASES_FILE)
        self.mental_health = self._load_json(Config.MENTAL_HEALTH_FILE)
        self.fitness_qa = self._load_json(Config.FITNESS_FILE)
        self.nutrition_tips = self._load_json(Config.NUTRITION_FILE)
    
    @staticmethod
    def _load_json(file_path):
        """Safely load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Warning: {file_path} not found")
            return {}
        except json.JSONDecodeError:
            print(f"⚠️  Warning: Invalid JSON in {file_path}")
            return {}
    
    def get_response(self, user_input):
        """
        Main response generation method
        
        Args:
            user_input (str): User's message
            
        Returns:
            str: Bot's response
        """
        user_input_lower = user_input.lower().strip()
        
        if not user_input_lower:
            return "I didn't catch that. Could you please say something? 😊"
        
        # 1. Check for disease information
        disease_response = self._check_disease_info(user_input_lower)
        if disease_response:
            return disease_response
        
        # 2. Check intent patterns (from intents.json)
        intent_response = self._match_intent(user_input_lower)
        if intent_response:
            return intent_response
        
        # 3. Check mental health Q&A
        mental_health_response = self._check_mental_health(user_input_lower)
        if mental_health_response:
            return mental_health_response
        
        # 4. Check fitness Q&A
        fitness_response = self._check_fitness_qa(user_input_lower)
        if fitness_response:
            return fitness_response
        
        # 5. Check nutrition tips
        nutrition_response = self._check_nutrition_tips(user_input_lower)
        if nutrition_response:
            return nutrition_response
        
        # 6. Default fallback
        return self._get_fallback_response()
    
    def _check_disease_info(self, user_input):
        """Check if user is asking about a disease"""
        if not self.diseases:
            return None
        
        diseases_list = self.diseases.get('diseases', [])
        
        for disease in diseases_list:
            disease_name = disease.get('name', '').lower()
            
            # Check if disease name is in user input
            if disease_name in user_input:
                description = disease.get('description', 'No description available.')
                symptoms = disease.get('symptoms', [])
                treatments = disease.get('treatments', [])
                
                response = f"🩺 **{disease['name']}**\n\n"
                response += f"**Description:** {description}\n\n"
                
                if symptoms:
                    response += f"**Common Symptoms:**\n"
                    for symptom in symptoms[:5]:  # Limit to 5 symptoms
                        response += f"• {symptom}\n"
                    response += "\n"
                
                if treatments:
                    response += f"**Treatments:**\n"
                    for treatment in treatments[:5]:  # Limit to 5 treatments
                        response += f"• {treatment}\n"
                
                response += "\n⚠️ **Important:** This information is for educational purposes only. Please consult a healthcare professional for proper diagnosis and treatment."
                
                return response
        
        return None
    
    def _match_intent(self, user_input):
        """Match user input to intent patterns using fuzzy matching"""
        if not self.intents:
            return None
        
        intents_list = self.intents.get('intents', [])
        
        best_match = None
        best_score = 0
        
        for intent in intents_list:
            patterns = intent.get('patterns', [])
            
            for pattern in patterns:
                # Use difflib for fuzzy string matching
                similarity = difflib.SequenceMatcher(
                    None,
                    pattern.lower(),
                    user_input
                ).ratio()
                
                # Also check if pattern is substring
                if pattern.lower() in user_input:
                    similarity = max(similarity, 0.8)
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = intent
        
        # Return response if confidence is high enough
        if best_match and best_score >= Config.FUZZY_MATCH_THRESHOLD:
            responses = best_match.get('responses', [])
            if responses:
                return random.choice(responses)
        
        return None
    
    def _check_mental_health(self, user_input):
        """Check mental health Q&A database"""
        if not self.mental_health:
            return None
        
        intents_list = self.mental_health.get('intents', [])
        
        best_match = None
        best_score = 0
        
        for intent in intents_list:
            patterns = intent.get('patterns', [])
            
            for pattern in patterns:
                similarity = difflib.SequenceMatcher(
                    None,
                    pattern.lower(),
                    user_input
                ).ratio()
                
                if pattern.lower() in user_input:
                    similarity = max(similarity, 0.8)
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = intent
        
        if best_match and best_score >= 0.5:  # Lowered threshold
            responses = best_match.get('responses', [])
            if responses:
                response = random.choice(responses)
                # Only add crisis info for actual mental health emergencies
                crisis_keywords = ['suicide', 'kill myself', 'end my life', 'want to die']
                if any(keyword in user_input.lower() for keyword in crisis_keywords):
                    response += "\n\n⚠️ **Mental Health Resources:**\n"
                    response += "• National Suicide Prevention Lifeline: 988 (US)\n"
                    response += "• Crisis Text Line: Text HOME to 741741\n"
                    response += "• If this is an emergency, please call emergency services immediately."
                return response
        
            return None

    def _check_fitness_qa(self, user_input):
        """Check fitness Q&A database"""
        if not self.fitness_qa:
            return None
        
        fitness_list = self.fitness_qa.get('fitness_qa', [])
        
        best_match = None
        best_score = 0
        
        for item in fitness_list:
            question = item.get('question', '').lower()
            category = item.get('category', '').lower()
            
            # Check question similarity
            q_similarity = difflib.SequenceMatcher(None, question, user_input).ratio()
            
            # Check if category keywords are in input
            if category.replace('_', ' ') in user_input:
                q_similarity = max(q_similarity, 0.7)
            
            if q_similarity > best_score:
                best_score = q_similarity
                best_match = item
        
        if best_match and best_score >= 0.5:
            answer = best_match.get('answer', '')
            return f"💪 {answer}"
        
        return None
    
    def _check_nutrition_tips(self, user_input):
        """Check nutrition tips database"""
        if not self.nutrition_tips:
            return None
        
        tips_list = self.nutrition_tips.get('nutrition_tips', [])
        
        best_match = None
        best_score = 0
        
        for tip in tips_list:
            topic = tip.get('topic', '').lower()
            category = tip.get('category', '').lower()
            
            # Check topic similarity
            t_similarity = difflib.SequenceMatcher(None, topic, user_input).ratio()
            
            # Check if category keywords are in input
            if category.replace('_', ' ') in user_input:
                t_similarity = max(t_similarity, 0.7)
            
            if t_similarity > best_score:
                best_score = t_similarity
                best_match = tip
        
        if best_match and best_score >= 0.5:
            guidance = best_match.get('guidance', '')
            return f"🥗 {guidance}"
        
        return None
    
    def _get_fallback_response(self):
        """Return a helpful fallback response"""
        fallback_responses = [
            "I'm not sure I understood that. Could you rephrase your question? 🤔",
            "Hmm, I didn't quite catch that. Try asking about:\n• Disease information (e.g., 'tell me about diabetes')\n• Nutrition (e.g., 'calories in apple')\n• Fitness advice\n• Mental health support\n• Health tools (BMI, water intake, calories)",
            "I'm still learning! Could you try asking in a different way? I'm great at answering questions about health, fitness, nutrition, and wellness! 💪",
            "Oops! 😅 I didn't quite understand. I can help with:\n✅ Disease info\n✅ Nutrition facts\n✅ Fitness tips\n✅ Mental health support\n✅ Health calculators\n\nWhat would you like to know?"
        ]
        
        return random.choice(fallback_responses)


# Testing
if __name__ == "__main__":
    engine = ChatbotEngine()
    
    # Test queries
    test_queries = [
        "hello",
        "tell me about diabetes",
        "how do I start working out",
        "what should I eat",
        "I feel anxious"
    ]
    
    print("=== Chatbot Engine Test ===\n")
    for query in test_queries:
        print(f"User: {query}")
        print(f"Bot: {engine.get_response(query)}")
        print("-" * 50)

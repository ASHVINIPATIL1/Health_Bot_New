"""
External API Services
Handles communication with external APIs (USDA, ExerciseDB, Quotes)
"""

import requests
import random
from config.settings import Config


class APIService:
    """Wrapper for external API calls"""
    
    @staticmethod
    def get_nutrition_info(food_name):
        """
        Get nutrition information from USDA FoodData Central API
        Using simplified approach for better compatibility
        """
        if not Config.USDA_API_KEY:
            return "⚠️ Nutrition service is currently unavailable. Please configure USDA_API_KEY in your .env file."
        
        try:
            # Simplified API call
            url = f"{Config.USDA_API_URL}?api_key={Config.USDA_API_KEY}&query={food_name}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                # Try fallback for common foods
                return get_nutrition_fallback(food_name)
            
            data = response.json()
            foods = data.get('foods', [])
            
            if not foods:
                return f"🔍 Sorry, I couldn't find nutrition details for '{food_name}'. Try: apple, banana, chicken, rice, etc."
            
            food = foods[0]
            nutrients = food.get('foodNutrients', [])
            
            if not nutrients:
                return get_nutrition_fallback(food_name)
            
            # Map ALL nutrients like old version
            nutrient_mapping = {
                "Energy": "Calories",
                "Carbohydrate, by difference": "Carbohydrates",
                "Protein": "Protein",
                "Total lipid (fat)": "Fat",
                "Fiber, total dietary": "Fiber",
                "Sugars, total including NLEA": "Sugars",
                "Vitamin C, total ascorbic acid": "Vitamin C",
                "Vitamin A, IU": "Vitamin A",
                "Calcium, Ca": "Calcium",
                "Iron, Fe": "Iron",
                "Sodium, Na": "Sodium",
                "Alcohol, ethyl": "Alcohol"
            }
            
            # Extract nutrients
            found_nutrients = {}
            for nutrient in nutrients:
                nutrient_name = nutrient.get("nutrientName", "")
                
                # Check if this nutrient matches our mapping
                for api_name, display_name in nutrient_mapping.items():
                    if api_name.lower() in nutrient_name.lower():
                        value = round(nutrient.get("value", 0), 1)
                        unit = nutrient.get("unitName", "")
                        found_nutrients[display_name] = f"{value} {unit}"
                        break
            
            # If we found nutrients, format response
            if found_nutrients:
                food_description = food.get('description', food_name).title()
                result = f"📋 Nutritional Information for {food_description} (per 100g):\n\n"
                
                # Display in preferred order
                priority_order = [
                    "Calories", "Carbohydrates", "Protein", "Fat",
                    "Fiber", "Sugars", "Sodium", "Vitamin C", 
                    "Vitamin A", "Calcium", "Iron", "Alcohol"
                ]
                
                for nutrient in priority_order:
                    if nutrient in found_nutrients:
                        value = found_nutrients[nutrient]
                        # Add note for alcohol if it's 0
                        if nutrient == "Alcohol" and "0" in value:
                            value += " (none)"
                        result += f"• {nutrient}: {value}\n"
                
                result += "\n💡 Values may vary by brand and preparation method"
                return result
            else:
                return get_nutrition_fallback(food_name)
            
        except Exception as e:
            print(f"USDA API Error: {e}")
            return get_nutrition_fallback(food_name)


    def get_nutrition_fallback(food_name):
        """Fallback nutrition data for common foods"""
        common_foods = {
            "apple": "📋 **Apple** (per 100g)\n\n• Calories: 52kcal\n• Carbs: 14g\n• Fiber: 2.4g\n• Sugar: 10g\n• Protein: 0.3g\n• Fat: 0.2g",
            "banana": "📋 **Banana** (per 100g)\n\n• Calories: 89kcal\n• Carbs: 23g\n• Fiber: 2.6g\n• Sugar: 12g\n• Protein: 1.1g\n• Fat: 0.3g",
            "chicken": "📋 **Chicken Breast** (per 100g)\n\n• Calories: 165kcal\n• Protein: 31g\n• Fat: 3.6g\n• Carbs: 0g",
            "rice": "📋 **White Rice** (per 100g, cooked)\n\n• Calories: 130kcal\n• Carbs: 28g\n• Protein: 2.7g\n• Fat: 0.3g",
            "egg": "📋 **Egg** (per 100g)\n\n• Calories: 155kcal\n• Protein: 13g\n• Fat: 11g\n• Carbs: 1.1g",
        }
        
        food_lower = food_name.lower()
        for key, value in common_foods.items():
            if key in food_lower:
                return value + "\n\n💡 USDA API unavailable - showing approximate values"
        
        return f"⚠️ Unable to fetch nutrition data for '{food_name}'. Try: apple, banana, chicken, rice, egg"
        
    @staticmethod
    def get_exercises(body_part='chest', limit=5):
        """
        Get exercise suggestions from ExerciseDB API
        
        Args:
            body_part (str): Target body part (chest, back, legs, shoulders, arms, etc.)
            limit (int): Number of exercises to return
            
        Returns:
            str: Formatted list of exercises or error message
        """
        if not Config.RAPID_API_KEY:
            return "⚠️ Exercise service is currently unavailable. Please configure RAPID_API_KEY in your .env file."
        
        try:
            # Normalize body part name
            body_part_mapping = {
                'chest': 'chest',
                'back': 'back',
                'legs': 'upper legs',
                'leg': 'upper legs',
                'shoulders': 'shoulders',
                'shoulder': 'shoulders',
                'arms': 'upper arms',
                'arm': 'upper arms',
                'biceps': 'upper arms',
                'triceps': 'upper arms',
                'abs': 'waist',
                'core': 'waist',
                'cardio': 'cardio'
            }
            
            target = body_part_mapping.get(body_part.lower(), body_part.lower())
            url = f"{Config.EXERCISE_API_URL}/bodyPart/{target}"
            
            headers = {
                'X-RapidAPI-Key': Config.RAPID_API_KEY,
                'X-RapidAPI-Host': 'exercisedb.p.rapidapi.com'
            }
            
            params = {'limit': limit * 2}  # Get more to have variety
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code != 200:
                return f"⚠️ Unable to fetch exercises right now. Status code: {response.status_code}"
            
            exercises = response.json()
            
            if not exercises:
                return f"🔍 No exercises found for '{body_part}'. Try: chest, back, legs, shoulders, arms, or abs."
            
            # Select random exercises if we got more than needed
            if len(exercises) > limit:
                exercises = random.sample(exercises, limit)
            
            # Format output
            result = f"💪 Top {len(exercises)} Exercises for {body_part.title()}:\n\n"
            
            for i, exercise in enumerate(exercises, 1):
                name = exercise.get('name', 'Unknown').title()
                equipment = exercise.get('equipment', 'bodyweight').title()
                target = exercise.get('target', '').title()
                
                result += f"{i}. **{name}**\n"
                result += f"   Equipment: {equipment}\n"
                result += f"   Target: {target}\n\n"
            
            result += "💡 Tips:\n"
            result += "• Warm up before exercising\n"
            result += "• Focus on proper form over speed\n"
            result += "• Start with lighter weights and progress gradually\n"
            result += "• Rest 48 hours between training the same muscle group"
            
            return result
        
        except requests.exceptions.Timeout:
            return "⏱️ Request timed out. Please try again."
        except requests.exceptions.RequestException:
            return "⚠️ Network error: Unable to connect to exercise service. Please check your internet connection."
        except Exception as e:
            return f"⚠️ An unexpected error occurred: {str(e)}"
    
    @staticmethod
    def get_motivational_quote():
        """
        Get a random motivational quote
        
        Returns:
            str: Motivational quote
        """
        # Fallback quotes if API fails
        fallback_quotes = [
            "💪 'The only bad workout is the one that didn't happen.'",
            "🌟 'Take care of your body. It's the only place you have to live.' - Jim Rohn",
            "🔥 'Your health is an investment, not an expense.'",
            "⚡ 'Progress over perfection. Every small step counts!'",
            "🧠 'Physical fitness is the first requisite of happiness.' - Joseph Pilates",
            "💚 'Health is wealth.'",
            "🎯 'The groundwork for all happiness is good health.' - Leigh Hunt",
            "🌱 'A healthy outside starts from the inside.'",
            "💫 'You don't have to be extreme, just consistent.'",
            "🏃 'The body achieves what the mind believes.'"
        ]
        
        try:
            response = requests.get(Config.QUOTES_API_URL, timeout=5)
            
            if response.status_code == 200:
                quotes = response.json()
                if quotes:
                    quote_obj = random.choice(quotes)
                    quote_text = quote_obj.get('text', '')
                    author = quote_obj.get('author', 'Unknown')
                    
                    if author and author != 'type.fit':
                        return f"💭 \"{quote_text}\" - {author}"
                    else:
                        return f"💭 \"{quote_text}\""
            
            # If API fails, use fallback
            return random.choice(fallback_quotes)
        
        except:
            # If anything fails, use fallback quotes
            return random.choice(fallback_quotes)
    
    @staticmethod
    def get_wellness_tip():
        """
        Get a random wellness tip
        
        Returns:
            str: Wellness tip
        """
        tips = [
            "💧 Stay hydrated! Aim for 8 glasses of water daily.",
            "😴 Get 7-9 hours of sleep for optimal health and recovery.",
            "🥗 Fill half your plate with vegetables at each meal.",
            "🏃 Take a 10-minute walk after meals to aid digestion.",
            "🧘 Practice deep breathing for 5 minutes to reduce stress.",
            "📱 Take regular breaks from screens to rest your eyes.",
            "🌞 Get 15-30 minutes of sunlight daily for vitamin D.",
            "🥜 Include protein in every meal to stay satiated.",
            "🎵 Listen to music you enjoy - it's good for mental health!",
            "👥 Connect with friends and family regularly for emotional wellbeing.",
            "📚 Learn something new every day to keep your mind sharp.",
            "🧴 Wash your hands regularly to prevent illness.",
            "🚶 Stand up and stretch every hour if you sit a lot.",
            "🥤 Limit sugary drinks - choose water or unsweetened tea.",
            "🌿 Add herbs and spices to meals for extra nutrients and flavor."
        ]
        
        return random.choice(tips)


# Example usage and testing
if __name__ == "__main__":
    api = APIService()
    
    print("=== Testing USDA API ===")
    print(api.get_nutrition_info("apple"))
    
    print("\n=== Testing ExerciseDB API ===")
    print(api.get_exercises("chest", 3))
    
    print("\n=== Testing Quotes API ===")
    print(api.get_motivational_quote())
    
    print("\n=== Testing Wellness Tips ===")
    print(api.get_wellness_tip())

"""
Health Calculation Tools
Provides BMI, water intake, and calorie calculators
"""

import re


class HealthTools:
    """Collection of health calculation tools"""
    
    @staticmethod
    def calculate_bmi(weight_kg, height_cm):
        """
        Calculate Body Mass Index (BMI)
        
        Args:
            weight_kg (float): Weight in kilograms
            height_cm (float): Height in centimeters
            
        Returns:
            dict: BMI value, category, and health information
        """
        try:
            weight = float(weight_kg)
            height = float(height_cm) / 100  # Convert cm to meters
            
            if weight <= 0 or height <= 0:
                return {"error": "Weight and height must be positive numbers."}
            
            if height < 0.5 or height > 2.5:  # Sanity check
                return {"error": "Height seems incorrect. Please enter height in centimeters (e.g., 170 cm)."}
            
            if weight < 20 or weight > 300:  # Sanity check
                return {"error": "Weight seems incorrect. Please enter weight in kilograms (e.g., 70 kg)."}
            
            bmi = round(weight / (height ** 2), 1)
            
            # Determine BMI category
            if bmi < 18.5:
                category = "Underweight"
                advice = "You may need to gain weight. Consult a healthcare provider for guidance."
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
                advice = "Great! You're in the healthy weight range. Keep up the good habits! 💪"
            elif 25 <= bmi < 30:
                category = "Overweight"
                advice = "Consider a balanced diet and regular exercise. Consult a healthcare provider."
            else:  # bmi >= 30
                category = "Obese"
                advice = "It's recommended to speak with a healthcare provider about weight management strategies."
            
            return {
                "bmi": bmi,
                "category": category,
                "advice": advice,
                "message": f"📊 Your BMI is {bmi} ({category})\n\n{advice}\n\n⚠️ Note: BMI doesn't account for muscle mass, bone density, or body composition. It's just one health indicator among many."
            }
        
        except ValueError:
            return {"error": "Please provide valid numbers for weight and height."}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
    
    @staticmethod
    def calculate_water_intake(weight_kg, activity_level="moderate"):
        """
        Calculate daily water intake recommendation
        
        Args:
            weight_kg (float): Weight in kilograms
            activity_level (str): Activity level (sedentary, light, moderate, active, very_active)
            
        Returns:
            dict: Water intake recommendation in liters and glasses
        """
        try:
            weight = float(weight_kg)
            
            if weight <= 0:
                return {"error": "Weight must be a positive number."}
            
            if weight < 20 or weight > 300:
                return {"error": "Weight seems incorrect. Please enter weight in kilograms (e.g., 70 kg)."}
            
            # Base calculation: 30-35 ml per kg body weight
            base_ml = weight * 33  # Middle value
            
            # Adjust for activity level
            activity_multipliers = {
                "sedentary": 1.0,
                "light": 1.1,
                "moderate": 1.2,
                "active": 1.3,
                "very_active": 1.4
            }
            
            multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
            total_ml = base_ml * multiplier
            
            # Convert to liters and glasses
            liters = round(total_ml / 1000, 1)
            glasses = round(total_ml / 250)  # 250ml per glass
            
            return {
                "water_liters": liters,
                "water_glasses": glasses,
                "message": f"💧 Daily Water Recommendation\n\nFor a {weight} kg person with {activity_level} activity level:\n\n• {liters} liters ({glasses} glasses of 250ml)\n\n💡 Tips:\n• Drink more in hot weather or during intense exercise\n• Pale yellow urine indicates good hydration\n• Spread intake throughout the day\n• Eat water-rich foods (fruits, vegetables)"
            }
        
        except ValueError:
            return {"error": "Please provide a valid number for weight."}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
    
    @staticmethod
    def calculate_daily_calories(age, weight_kg, height_cm, gender, activity_level):
        """
        Calculate daily calorie needs using Mifflin-St Jeor Equation
        
        Args:
            age (int): Age in years
            weight_kg (float): Weight in kilograms
            height_cm (float): Height in centimeters
            gender (str): 'male' or 'female'
            activity_level (str): Activity level
            
        Returns:
            dict: Daily calorie recommendation with breakdown
        """
        try:
            age = int(age)
            weight = float(weight_kg)
            height = float(height_cm)
            
            if age < 15 or age > 100:
                return {"error": "Please provide a valid age between 15 and 100."}
            
            if weight <= 0 or height <= 0:
                return {"error": "Weight and height must be positive numbers."}
            
            # Calculate BMR using Mifflin-St Jeor Equation
            if gender.lower() == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            elif gender.lower() == 'female':
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
            else:
                return {"error": "Please specify gender as 'male' or 'female'."}
            
            # Activity level multipliers
            activity_multipliers = {
                "sedentary": 1.2,        # Little or no exercise
                "light": 1.375,          # Light exercise 1-3 days/week
                "moderate": 1.55,        # Moderate exercise 3-5 days/week
                "active": 1.725,         # Hard exercise 6-7 days/week
                "very_active": 1.9       # Very hard exercise, physical job
            }
            
            multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
            
            # Calculate Total Daily Energy Expenditure (TDEE)
            tdee = round(bmr * multiplier)
            
            # Calculate for different goals
            maintenance = tdee
            weight_loss = round(tdee - 500)  # 500 calorie deficit
            weight_gain = round(tdee + 300)  # 300 calorie surplus
            
            return {
                "maintenance_calories": maintenance,
                "weight_loss_calories": weight_loss,
                "weight_gain_calories": weight_gain,
                "bmr": round(bmr),
                "message": f"🔥 Daily Calorie Needs ({gender.capitalize()}, {age} years, {activity_level} activity)\n\n"
                          f"• Maintain weight: {maintenance} kcal/day\n"
                          f"• Lose weight (safe): {weight_loss} kcal/day\n"
                          f"• Gain weight (muscle): {weight_gain} kcal/day\n"
                          f"• BMR (at rest): {round(bmr)} kcal/day\n\n"
                          f"💡 Tips:\n"
                          f"• These are estimates; adjust based on results\n"
                          f"• Focus on nutrient-dense whole foods\n"
                          f"• Combine with strength training for best results\n"
                          f"• Don't go below 1200 (women) or 1500 (men) kcal/day"
            }
        
        except ValueError:
            return {"error": "Please provide valid numbers for age, weight, and height."}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
    
    @staticmethod
    def parse_user_input_for_bmi(text):
        """Extract weight and height from user input"""
        # Pattern: "My weight is 70 kg and height is 175 cm"
        weight_pattern = r'(\d+(?:\.\d+)?)\s*kg'
        height_pattern = r'(\d+(?:\.\d+)?)\s*cm'
        
        weight_match = re.search(weight_pattern, text, re.IGNORECASE)
        height_match = re.search(height_pattern, text, re.IGNORECASE)
        
        if weight_match and height_match:
            return {
                'weight': weight_match.group(1),
                'height': height_match.group(1)
            }
        return None
    
    @staticmethod
    def parse_user_input_for_water(text):
        """Extract weight from user input"""
        # Pattern: "I weigh 70 kg"
        pattern = r'(\d+(?:\.\d+)?)\s*kg'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return {'weight': match.group(1)}
        return None
    
    @staticmethod
    def parse_user_input_for_calories(text):
        """Extract age, weight, height, gender, activity from user input"""
        # This is complex - better to guide user through a form
        # For now, just detect if they're trying to use the calculator
        keywords = ['age', 'weight', 'height', 'gender', 'activity']
        return any(keyword in text.lower() for keyword in keywords)


# Example usage and testing
if __name__ == "__main__":
    tools = HealthTools()
    
    # Test BMI
    print("=== BMI Calculator Test ===")
    result = tools.calculate_bmi(70, 175)
    print(result['message'] if 'message' in result else result)
    
    print("\n=== Water Intake Test ===")
    result = tools.calculate_water_intake(70, "moderate")
    print(result['message'] if 'message' in result else result)
    
    print("\n=== Calorie Calculator Test ===")
    result = tools.calculate_daily_calories(25, 70, 175, "male", "moderate")
    print(result['message'] if 'message' in result else result)

"""
Main Flask Application - Health & Fitness Chatbot
Professional chatbot with authentication, chat history, and health tools
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import os
import re

# Import our custom modules
from config.settings import Config
from utils.database import Database
from utils.chatbot_engine import ChatbotEngine
from utils.api_services import APIService
from utils.health_tools import HealthTools

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = Config.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = Config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE

# Initialize services
db = Database()
chatbot = ChatbotEngine()
api_service = APIService()
health_tools = HealthTools()

print("=" * 60)
print("🩺 HEALTH & FITNESS CHATBOT - Starting...")
print("=" * 60)

# Validate configuration
Config.validate_api_keys()
Config.check_data_files()

print("✅ Server initialized successfully!")
print("=" * 60)


# ========== AUTHENTICATION DECORATOR ==========

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ========== ROUTES ==========

@app.route('/')
def index():
    """Home page - redirect to chat if logged in, otherwise to login"""
    if 'user_id' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Please provide both username and password'})
        
        # Authenticate user
        result = db.authenticate_user(username, password)
        
        if result['success']:
            # Set session
            session['user_id'] = result['user_id']
            session['username'] = result['username']
            session.permanent = True
            
            return jsonify({
                'success': True,
                'message': 'Login successful! 🎉',
                'redirect': url_for('chat')
            })
        else:
            return jsonify(result)
    
    # GET request - show login page
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Create user
        result = db.create_user(username, email, password)
        
        if result['success']:
            # Auto-login after signup
            session['user_id'] = result['user_id']
            session['username'] = username
            session.permanent = True
            
            return jsonify({
                'success': True,
                'message': 'Account created successfully! 🎉',
                'redirect': url_for('chat')
            })
        else:
            return jsonify(result)
    
    # GET request - show signup page
    return render_template('signup.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/chat')
@login_required
def chat():
    """Main chat interface"""
    username = session.get('username', 'User')
    return render_template('index.html', username=username)


@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    Main chat API endpoint
    Processes user message and returns bot response
    """
    data = request.get_json()
    user_message = data.get('message', '').strip()
    user_id = session.get('user_id')
    
    if not user_message:
        return jsonify({'reply': 'Please say something! 😊'})
    
    # Save user message to history
    db.save_message(user_id, user_message, is_user_message=True)
    
    # Process message and generate response
    bot_reply = process_message(user_message)
    
    # Save bot response to history
    db.save_message(user_id, bot_reply, is_user_message=False)
    
    return jsonify({'reply': bot_reply})


def process_message(user_message):
    """
    Process user message through various handlers
    Returns appropriate response
    """
    user_input_lower = user_message.lower()
    
    # 1. Check for nutrition queries
    nutrition_keywords = ['calories in', 'nutrition of', 'nutrition in', 'nutritional value of']
    for keyword in nutrition_keywords:
        if keyword in user_input_lower:
            food = user_input_lower.replace(keyword, '').strip()
            if food:
                return api_service.get_nutrition_info(food)
    
    # 2. Check for exercise suggestions
    exercise_keywords = ['exercises for', 'workout for', 'show me exercises', 'exercise suggestions']
    for keyword in exercise_keywords:
        if keyword in user_input_lower:
            body_part = user_input_lower.replace(keyword, '').strip()
            body_part = body_part.replace('my', '').strip()
            if body_part:
                return api_service.get_exercises(body_part, 5)
    
    # 3. Check for motivational quote request
    if any(word in user_input_lower for word in ['quote', 'inspire me', 'motivation']):
        return api_service.get_motivational_quote()
    
    # 4. Check for wellness tip request
    if any(word in user_input_lower for word in ['wellness tip', 'health tip', 'daily tip']):
        return api_service.get_wellness_tip()
    
    # 5. Check for BMI calculator
    if 'bmi' in user_input_lower or 'body mass index' in user_input_lower:
        bmi_data = health_tools.parse_user_input_for_bmi(user_message)
        if bmi_data:
            result = health_tools.calculate_bmi(bmi_data['weight'], bmi_data['height'])
            return result.get('message', result.get('error', 'Unable to calculate BMI'))
        else:
            return "To calculate your BMI, please tell me:\n\n'My weight is [X] kg and height is [Y] cm'\n\nFor example: 'My weight is 70 kg and height is 175 cm'"
    
    # 6. Check for water intake calculator
    if any(word in user_input_lower for word in ['water intake', 'how much water', 'daily water']):
        water_data = health_tools.parse_user_input_for_water(user_message)
        if water_data:
            result = health_tools.calculate_water_intake(water_data['weight'])
            return result.get('message', result.get('error', 'Unable to calculate water intake'))
        else:
            return "To calculate your daily water needs, please tell me:\n\n'I weigh [X] kg'\n\nFor example: 'I weigh 70 kg'"
    
    # 7. Check for calorie calculator
    if any(word in user_input_lower for word in ['calculate calories', 'daily calories', 'calorie needs']):
        return "To calculate your daily calorie needs, I'll need:\n\n• Age\n• Weight (kg)\n• Height (cm)\n• Gender (male/female)\n• Activity level\n\nPlease use the calorie calculator button or visit the help page for a detailed form! 📊"
    
    # 8. Use chatbot engine for general queries
    return chatbot.get_response(user_message)


@app.route('/api/history')
@login_required
def get_history():
    """Get chat history for current user"""
    user_id = session.get('user_id')
    history = db.get_chat_history(user_id, limit=50)
    return jsonify({'history': history})


@app.route('/api/clear-history', methods=['POST'])
@login_required
def clear_history():
    """Clear chat history for current user"""
    user_id = session.get('user_id')
    success = db.clear_chat_history(user_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Chat history cleared! 🗑️'})
    else:
        return jsonify({'success': False, 'message': 'Failed to clear history'})


@app.route('/api/health-tool', methods=['POST'])
@login_required
def health_tool():
    """
    API endpoint for health tools (BMI, Water, Calories)
    """
    data = request.get_json()
    tool_type = data.get('tool')
    
    if tool_type == 'bmi':
        weight = data.get('weight')
        height = data.get('height')
        result = health_tools.calculate_bmi(weight, height)
        return jsonify(result)
    
    elif tool_type == 'water':
        weight = data.get('weight')
        activity = data.get('activity', 'moderate')
        result = health_tools.calculate_water_intake(weight, activity)
        return jsonify(result)
    
    elif tool_type == 'calories':
        age = data.get('age')
        weight = data.get('weight')
        height = data.get('height')
        gender = data.get('gender')
        activity = data.get('activity')
        result = health_tools.calculate_daily_calories(age, weight, height, gender, activity)
        return jsonify(result)
    
    return jsonify({'error': 'Invalid tool type'})


@app.route('/help')
@login_required
def help_page():
    """Help and user guide page"""
    return render_template('help.html')


@app.route('/api/user-stats')
@login_required
def user_stats():
    """Get user statistics"""
    user_id = session.get('user_id')
    stats = db.get_user_stats(user_id)
    user_info = db.get_user_by_id(user_id)
    
    return jsonify({
        'user': user_info,
        'stats': stats
    })


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


# ========== MAIN ==========

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting Flask server...")
    print("📍 Visit: http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(
        debug=Config.FLASK_DEBUG,
        host='0.0.0.0',
        port=5000
    )

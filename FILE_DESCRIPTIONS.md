# 📁 FILE DESCRIPTIONS

Complete guide to every file in your refactored Health Chatbot project.

---

## 📖 Documentation Files

### START_HERE.md ⭐ **READ THIS FIRST!**
Your entry point to the project. Provides:
- Quick 5-minute setup guide
- Overview of what's included
- Troubleshooting tips
- Next steps

### QUICK_START.md
Fast-track guide for getting the chatbot running:
- Installation steps
- API key acquisition
- Configuration
- Testing checklist

### README.md
Comprehensive project documentation:
- Feature list
- Detailed setup instructions
- API documentation
- Usage examples
- Best practices

### PROJECT_SUMMARY.md
High-level overview of the refactoring:
- What was changed and why
- Statistics and metrics
- Interview talking points
- Achievement highlights

### IMPLEMENTATION_GUIDE.md
Technical deep-dive:
- Architecture decisions
- Data migration details
- Security implementations
- Code organization

### FILE_DESCRIPTIONS.md (this file)
Description of every file in the project.

---

## 🐍 Core Python Files

### app.py (Main Application)
**Lines:** ~350
**Purpose:** Main Flask application entry point
**Contains:**
- Flask app initialization
- All route handlers (@app.route)
- Authentication decorators
- API endpoints (/api/chat, /api/history, etc.)
- Error handlers (404, 500)
- Session management

**Key Functions:**
- `login()` - Handle user authentication
- `signup()` - Register new users
- `api_chat()` - Main chat API endpoint
- `process_message()` - Message routing logic
- `health_tool()` - Health calculator API

---

## ⚙️ Configuration

### config/settings.py
**Purpose:** Centralized configuration management
**Contains:**
- Environment variable loading
- API configuration
- File paths
- Flask settings
- Session configuration
- Validation functions

**Key Class:**
- `Config` - All configuration in one place

**Features:**
- Auto-validation of API keys
- Data file existence checks
- Environment-specific settings

---

## 🛠️ Utility Modules

### utils/database.py
**Lines:** ~280
**Purpose:** Database operations and user management
**Contains:**
- SQLite database connection
- User authentication (signup/login)
- Chat history storage
- Password hashing (bcrypt)
- User statistics

**Key Class:**
- `Database` - Complete database wrapper

**Tables Created:**
- `users` - User accounts
- `chat_history` - Message storage

**Key Methods:**
- `create_user()` - Register new user
- `authenticate_user()` - Login verification
- `save_message()` - Store chat message
- `get_chat_history()` - Retrieve messages
- `get_user_stats()` - User statistics

### utils/chatbot_engine.py
**Lines:** ~250
**Purpose:** Core NLP and response generation
**Contains:**
- Intent matching (fuzzy logic)
- Disease information lookup
- Mental health Q&A
- Fitness Q&A
- Nutrition tips
- Fallback responses

**Key Class:**
- `ChatbotEngine` - Main chatbot logic

**Key Methods:**
- `get_response()` - Main entry point
- `_match_intent()` - Pattern matching
- `_check_disease_info()` - Disease lookup
- `_check_mental_health()` - Mental health support
- `_check_fitness_qa()` - Fitness advice
- `_check_nutrition_tips()` - Nutrition guidance

**Uses:**
- difflib for fuzzy matching
- JSON data files
- Threshold-based matching (0.6)

### utils/api_services.py
**Lines:** ~230
**Purpose:** External API integrations
**Contains:**
- USDA nutrition API wrapper
- ExerciseDB API wrapper
- Quotes API wrapper
- Wellness tips generator
- Error handling

**Key Class:**
- `APIService` - API wrapper methods

**Key Methods:**
- `get_nutrition_info()` - USDA API call
- `get_exercises()` - ExerciseDB API call
- `get_motivational_quote()` - Quotes API
- `get_wellness_tip()` - Random tips

**APIs Used:**
1. USDA FoodData Central (nutrition)
2. ExerciseDB via RapidAPI (exercises)
3. Type.fit Quotes API (motivation)

### utils/health_tools.py
**Lines:** ~270
**Purpose:** Health calculation tools
**Contains:**
- BMI calculator
- Water intake calculator
- Calorie calculator (Mifflin-St Jeor)
- Input parsers
- Result formatters

**Key Class:**
- `HealthTools` - Calculator methods

**Key Methods:**
- `calculate_bmi()` - BMI calculation
- `calculate_water_intake()` - Water needs
- `calculate_daily_calories()` - TDEE calculation
- `parse_user_input_for_bmi()` - Extract data
- `parse_user_input_for_water()` - Extract data

**Formulas:**
- BMI: weight(kg) / height(m)²
- Water: 33ml per kg × activity multiplier
- Calories: Mifflin-St Jeor equation × activity

---

## 📊 Data Files

### data/intents.json
**Size:** ~50 intents
**Purpose:** Chat patterns moved from Python
**Contains:**
- Greeting patterns
- Bot identity
- Health tool triggers
- General conversation
- Farewell patterns

**Structure:**
```json
{
  "intents": [
    {
      "tag": "intent_name",
      "patterns": ["pattern1", "pattern2"],
      "responses": ["response1", "response2"]
    }
  ]
}
```

**Source:** Migrated from Python chat_patterns

### data/diseases.json
**Size:** 300+ diseases
**Purpose:** Disease information database
**Contains:**
- Disease names
- Descriptions
- Symptoms lists
- Treatment options

**Structure:**
```json
{
  "diseases": [
    {
      "name": "Disease Name",
      "description": "Description",
      "symptoms": ["symptom1", ...],
      "treatments": ["treatment1", ...]
    }
  ]
}
```

**Source:** Original health-data.json

### data/mental_health_qa.json
**Size:** 12,000+ intents
**Purpose:** Comprehensive mental health support
**Contains:**
- Mental health questions
- Coping strategies
- Professional resources
- Crisis information

**Structure:** Same as intents.json

**Source:** Original KB.json

### data/fitness_qa.json ✨ **NEW!**
**Size:** 25 fitness topics
**Purpose:** Fitness and exercise guidance
**Contains:**
- Beginner fitness advice
- Workout planning
- Exercise frequency
- Recovery tips
- Common fitness questions

**Structure:**
```json
{
  "fitness_qa": [
    {
      "category": "category_name",
      "question": "Question?",
      "answer": "Answer"
    }
  ]
}
```

**Source:** Compiled from CDC, WHO, ACSM, NASM guidelines

### data/nutrition_tips.json ✨ **NEW!**
**Size:** 30 nutrition topics
**Purpose:** Comprehensive nutrition guidance
**Contains:**
- Balanced diet principles
- Macronutrient information
- Meal planning tips
- Specific nutrient guidance
- Healthy eating habits

**Structure:**
```json
{
  "nutrition_tips": [
    {
      "category": "category_name",
      "topic": "Topic",
      "guidance": "Detailed guidance"
    }
  ]
}
```

**Source:** USDA Dietary Guidelines, WHO, AHA, Harvard

---

## 🎨 Templates (HTML)

### templates/index.html
**Purpose:** Main chat interface
**Features:**
- Modern ChatGPT-inspired design
- Message display area
- Input form
- Header with user info
- Chat history loading
- Real-time messaging
- Responsive design

**JavaScript:**
- Message sending (AJAX)
- History loading
- Auto-scroll
- Error handling

### templates/login.html
**Purpose:** User login page
**Features:**
- Username/password form
- Error message display
- Link to signup
- Modern gradient design
- Form validation

**JavaScript:**
- Login API call
- Error display
- Redirect on success

### templates/signup.html
**Purpose:** User registration page
**Features:**
- Username/email/password form
- Validation messages
- Link to login
- Matching design with login
- Auto-login after signup

**JavaScript:**
- Signup API call
- Validation
- Error handling

### templates/help.html
**Purpose:** User guide and documentation
**Features:**
- Command examples
- Health disclaimer
- Feature descriptions
- Crisis resources
- Tips for best results

---

## 📦 Configuration Files

### requirements.txt
**Purpose:** Python dependencies
**Contains:**
- Flask==3.0.0
- nltk==3.8.1
- requests==2.31.0
- bcrypt==4.1.2
- python-dotenv==1.0.0
- bleach==6.1.0
- python-dateutil==2.8.2

### .env.example
**Purpose:** Environment variable template
**Contains:**
- API key placeholders
- Flask configuration
- Database settings
- Comments and instructions

**Copy to:** `.env` (ignored by git)

---

## 📁 Directory Structure

### config/
Configuration management module
- settings.py

### data/
All JSON datasets
- intents.json
- diseases.json
- mental_health_qa.json
- fitness_qa.json
- nutrition_tips.json
- chatbot.db (auto-created)

### utils/
Core utility modules
- database.py
- chatbot_engine.py
- api_services.py
- health_tools.py

### templates/
HTML templates
- index.html
- login.html
- signup.html
- help.html

### static/
Static assets
- img/bot.webp
- css/ (for future CSS)
- js/ (for future JS)

---

## 📊 Statistics

### Code Metrics:
- **Python files:** 6
- **Lines of Python:** ~1,400
- **JSON files:** 5
- **Lines of JSON:** ~50,000
- **HTML files:** 4
- **Documentation files:** 6

### Features:
- **Routes:** 15+
- **Database tables:** 2
- **API integrations:** 3
- **Health tools:** 3
- **Datasets:** 5

### Data:
- **Diseases:** 300+
- **Mental health intents:** 12,000+
- **Fitness topics:** 25
- **Nutrition tips:** 30
- **Chat intents:** 50+

---

## 🔄 Data Flow

### 1. User Sends Message
1. User types message in index.html
2. JavaScript sends to /api/chat
3. app.py receives in api_chat()
4. Calls process_message()

### 2. Message Processing
1. Check nutrition keywords → api_services.py
2. Check exercise keywords → api_services.py
3. Check health tool keywords → health_tools.py
4. Else: chatbot_engine.py

### 3. Chatbot Engine
1. Check disease info → diseases.json
2. Check intents → intents.json
3. Check mental health → mental_health_qa.json
4. Check fitness → fitness_qa.json
5. Check nutrition → nutrition_tips.json
6. Fallback response

### 4. Response Delivery
1. process_message() returns response
2. database.py saves to chat_history
3. app.py sends JSON response
4. JavaScript displays in chat

---

## 🔒 Security Files

### Password Hashing
- **File:** utils/database.py
- **Method:** bcrypt
- **Rounds:** Default (12)

### Environment Variables
- **File:** config/settings.py
- **Loader:** python-dotenv
- **Storage:** .env (not committed)

### Session Management
- **File:** app.py
- **Storage:** Secure cookies
- **Lifetime:** 7 days

---

## 🚀 Deployment Files

### For Production:
Need to add:
- Procfile (for Heroku)
- runtime.txt (Python version)
- wsgi.py (WSGI server)
- nginx.conf (if self-hosting)

Currently configured for:
- Development mode
- Local SQLite
- Debug enabled

---

## 📝 Notes

### Files NOT Included:
- `.env` (user must create)
- `data/chatbot.db` (auto-created)
- `.git/` (user can init)
- `__pycache__/` (auto-generated)
- `.pyc` files (auto-generated)

### Files You Might Add:
- tests/ (unit tests)
- docs/ (extended documentation)
- migrations/ (database migrations)
- logs/ (application logs)
- backups/ (database backups)

---

## 💡 Quick Reference

### To Run:
```bash
python app.py
```

### To Test Database:
```bash
python utils/database.py
```

### To Test Chatbot Engine:
```bash
python utils/chatbot_engine.py
```

### To Test Health Tools:
```bash
python utils/health_tools.py
```

### To Test API Services:
```bash
python utils/api_services.py
```

---

## 🎓 Learning Order

**Recommended Reading Order:**

1. START_HERE.md
2. QUICK_START.md
3. app.py
4. utils/database.py
5. utils/chatbot_engine.py
6. utils/api_services.py
7. utils/health_tools.py
8. config/settings.py
9. templates/index.html
10. data/intents.json

---

**This completes the file documentation!**

Every file has a purpose and fits into the overall architecture.
The project is modular, maintainable, and ready for enhancement.

Good luck with your project! 🚀

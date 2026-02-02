# 🩺 Advanced Health & Fitness Chatbot

A professional, scalable health and fitness chatbot with login system, chat history, health tools, and modern UI.

## 🎯 Features

### Core Features
- ✅ **Intent-Based Chatbot** - Smart pattern matching with fuzzy logic
- ✅ **Disease Information** - 300+ diseases with symptoms and treatments
- ✅ **Nutrition Lookup** - USDA FoodData API integration
- ✅ **Mental Health Support** - Safe, general advice with professional referrals

### 🆕 New Features
- ✅ **User Authentication** - Secure signup/login with password hashing
- ✅ **Chat History** - Persistent conversation storage per user
- ✅ **Health Tools** - BMI, Water intake, Calorie calculators
- ✅ **Exercise Suggestions** - Free ExerciseDB API integration
- ✅ **Motivational Quotes** - Daily wellness inspiration
- ✅ **Modern UI** - Clean ChatGPT-inspired interface
- ✅ **Help Guide** - Comprehensive user documentation

### 🔒 Security
- Password hashing with bcrypt
- Session management
- Environment variable configuration
- Input sanitization

## 📂 Project Structure

```
health_chatbot_v2/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── README.md                  # This file
│
├── config/
│   └── settings.py            # Configuration management
│
├── data/
│   ├── intents.json           # Chatbot patterns (MOVED FROM PYTHON!)
│   ├── diseases.json          # Disease database
│   ├── mental_health.json     # Mental health Q&A (NEW!)
│   ├── fitness_qa.json        # Fitness Q&A (NEW!)
│   └── nutrition_tips.json    # Nutrition guidance (NEW!)
│
├── models/
│   ├── user.py                # User model with auth
│   └── chat.py                # Chat history model
│
├── utils/
│   ├── chatbot_engine.py      # Core chatbot logic
│   ├── api_services.py        # External API integrations
│   ├── health_tools.py        # BMI, calorie, water calculators
│   └── database.py            # Database operations
│
├── templates/
│   ├── index.html             # Chat interface
│   ├── login.html             # Login page
│   ├── signup.html            # Registration page
│   └── help.html              # User guide
│
└── static/
    ├── css/
    │   └── style.css          # Modern styling
    ├── js/
    │   └── chat.js            # Frontend logic
    └── img/
        └── bot.webp           # Bot icon
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# API Keys
USDA_API_KEY=your_usda_api_key_here
RAPID_API_KEY=your_rapidapi_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Database (SQLite by default)
DATABASE_PATH=data/chatbot.db
```

### 3. Get Free API Keys

#### USDA FoodData Central (Nutrition)
1. Visit: https://fdc.nal.usda.gov/api-key-signup.html
2. Sign up for a free API key
3. Add to `.env` file

#### RapidAPI (ExerciseDB)
1. Visit: https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb
2. Sign up for free tier (150 requests/day)
3. Add to `.env` file

### 4. Run the Application

```bash
python app.py
```

Visit: http://localhost:5000

## 🎮 How to Use

### For First-Time Users
1. Click "Sign Up" and create an account
2. Login with your credentials
3. Start chatting with the bot!

### Available Commands

**General Queries:**
- "Hi" / "Hello" - Greet the bot
- "How are you?" - Check bot status
- "What can you do?" - See capabilities

**Health Information:**
- "Tell me about diabetes" - Get disease info
- "What are symptoms of flu?" - Learn symptoms
- "Treatment for headache?" - Get treatment options

**Nutrition:**
- "Calories in apple" - Get nutrition facts
- "Nutrition of chicken breast" - Food information

**Health Tools:**
- "Calculate my BMI" - BMI calculator
- "How much water should I drink?" - Water intake
- "Calculate my daily calories" - Calorie needs

**Fitness:**
- "Show me exercises for chest" - Get exercise suggestions
- "Workout for abs" - Abs exercises

**Mental Health:**
- "I feel anxious" - Get support resources
- "How to deal with stress?" - Stress management tips

## 📊 Datasets Used

### Included Datasets
1. **Disease Database** (300+ diseases)
   - Source: Combined medical databases
   - Symptoms, treatments, descriptions

2. **Mental Health Q&A** (100+ intents)
   - Source: NAMI, Mental Health America
   - Safe, general mental health guidance

3. **Fitness Q&A** (50+ intents)
   - Source: Public health organizations
   - Exercise, workout planning

4. **Nutrition Tips** (75+ intents)
   - Source: USDA, WHO guidelines
   - Balanced diet, macro/micronutrients

### External APIs
1. **USDA FoodData Central** - Nutrition information
2. **ExerciseDB** - Exercise database with images

## 🔐 Security Features

- **Password Hashing**: bcrypt with salt
- **Session Management**: Secure Flask sessions
- **Input Sanitization**: XSS prevention
- **Environment Variables**: No hardcoded secrets
- **HTTPS Ready**: Production-ready configuration

## 🎨 UI Design

Inspired by:
- ChatGPT - Clean chat interface
- NotebookLM - Modern, minimalist design

Features:
- Light theme with blue accents
- Responsive design
- Smooth animations
- Loading indicators
- Error handling

## ⚠️ Health Disclaimer

**IMPORTANT**: This chatbot provides general health and fitness information for educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

**Always consult a qualified healthcare provider for:**
- Medical diagnosis
- Treatment decisions
- Emergency situations
- Mental health crises

**If you're experiencing a medical emergency, call emergency services immediately.**

## 🛠️ Development

### Adding New Intents
Edit `data/intents.json`:

```json
{
  "tag": "new_intent",
  "patterns": ["pattern1", "pattern2"],
  "responses": ["response1", "response2"]
}
```

### Adding New Diseases
Edit `data/diseases.json`:

```json
{
  "name": "Disease Name",
  "description": "Description",
  "symptoms": ["symptom1", "symptom2"],
  "treatments": ["treatment1", "treatment2"]
}
```

### Adding New Health Tools
Edit `utils/health_tools.py` and add your function.

## 📝 Best Practices

1. **Keep data separated** - JSON files, not Python code
2. **Use environment variables** - Never hardcode API keys
3. **Validate input** - Sanitize user input
4. **Handle errors gracefully** - User-friendly error messages
5. **Add health disclaimers** - Always remind users to consult professionals

## 🤝 Contributing

This is a learning project. Feel free to:
- Add new health datasets
- Improve UI/UX
- Add new features
- Report bugs

## 📄 License

MIT License - Free for educational and personal use.

## 👨‍💻 Author
**Ashvini Dagdu Pati**
This project was initially built as an academic learning exercise and represents a significantly enhanced version of the [original Health_Bot](https://github.com/ASHVINIPATIL1/Health_Bot). 
It showcases expertise in:
    - Full-stack development
    - API integration
    - Authentication systems
    - Database management
    - Modern UI/UX design
---
>>>>>>> 637c70887ffea7e4490b3dbdddc78c199edfe823

**Made with ❤️ for learning and helping others stay healthy!**

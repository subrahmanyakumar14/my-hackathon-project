"""
College FAQ Chatbot Application
================================
A Flask-based conversational AI that answers frequently asked questions about college services,
fees, admission, hostel, exams, and other student-related information.
"""

from flask import Flask, render_template, request, jsonify
import re

# Initialize the Flask application
app = Flask(__name__)

# College FAQ Knowledge Base
# Each entry contains:
# - intent: Category of the question
# - keywords: Terms that trigger this answer
# - answer: The response to provide to students
FAQ_DATABASE = [
   # Add this object into your FAQ_DATABASE list in app.py:
{
    "intent": "greetings",
    "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"],
    "answer": "Hello! How can I help you today? You can ask about exam dates, tuition fees, library hours, or timetables."
},

  {
        "intent": "fees",
        "keywords": ["payment", "due date"],
        "answer": "Tuition fees for the current semester are due on September 15th. You can pay via the student portal under the Financials tab."
    },
    {
        "intent": "semester fees",
        "keywords": ["fee", "fees", "cost", "tuition"],
        "answer": "Tuition fees for the current semester for CSE CORE was 90000 per semester, for CSE AIML was 120000 per semester, for CSE Data Science was 100000 per semester, for ECE was 80000, and for mechanical 80000."
    },
    {
        "intent": "exam_dates",
        "keywords": ["exam", "exams", "date", "dates", "schedule", "midterm", "final"],
        "answer": "The CA's will be from the 5th week from the course started. Midterm exams begin in the first week of October. Final exams are scheduled from mid-December."
    },
    {
        "intent": "library_hours",
        "keywords": ["library", "hours", "open", "timing", "timings", "close"],
        "answer": "The central library is open Monday to Friday from 8:00 AM to 12:00 PM, and weekends from 10:00 AM to 12:00 PM."
    },
    {
        "intent": "timings",
        "keywords": ["timetable", "schedule", "class", "classes", "timing", "lecture","college timmings","timmings of college"],
        "answer": "The college timings are from 9:00 AM to 5:00 PM. Class timetables can be downloaded from the Academic Portal after logging in with your student ID."
    },
    {
        "intent": "admission",
        "keywords": ["admission", "apply", "eligibility", "criteria", "deadline"],
        "answer": "Admissions for the upcoming academic session close on August 31st. Visit the official admissions portal to apply. The eligibility criteria are: CSE CORE 60% in 12th, CSE AIML 70% in 12th, CSE Data Science 65% in 12th, ECE 55% in 12th, and Mechanical 50% in 12th."
    },
    {
        "intent": "hostel",
        "keywords": ["hostel", "accommodation", "living", "residence"],
        "answer": "The college provides hostel facilities for both male and female students. The application process and availability details can be found on the Student Services portal."
    },
    {
        "intent": "hostel fees",
        "keywords": ["hostel", "fees", "hostel charges", "hostel cost", "mess", "mess charges", "mess cost", "laundry", "laundry charges", "laundry cost"],
        "answer": "The college hostel charges include room rent of 93000 per year, food costs of 44000, and laundry charges of 54000."
    },
    {
        "intent": "exam fees",
        "keywords": ["exam", "fees", "test fees", "examination fees"],
        "answer": "The exam fees for each semester are 50000 per semester."
    },
    {
        "intent": "dress code",
        "keywords": ["dress code", "dress", "uniform", "pev"],
        "answer": "The college dress code is formal attire during college hours. For PEV classes, students are required to wear the official college uniform."
    },
    {
        "intent": "nirf_ranking",
        "keywords": ["nirf", "ranking", "nirf ranking"],
        "answer": "The university is ranked 31st among all universities in India. Category-wise NIRF Rankings (2025): Overall 49th, Pharmacy 13th, Architecture 24th, Law 26th, Management 44th, Engineering 48th."
    }
]


def normalize_text(text):
    """
    Convert text to lowercase and remove special characters.
    This standardizes user input for consistent keyword matching.
    
    Args:
        text (str): The text to normalize
        
    Returns:
        str: Normalized text (lowercase, alphanumeric + spaces only)
    """
    return re.sub(r"[^a-z0-9\s]", "", str(text).lower())



def find_best_answer(user_query):
    """
    Find the best matching FAQ answer based on keyword matching and scoring.
    
    The matching algorithm uses a weighted scoring system:
    - Exact phrase matches in the query get 5 points (3 for single words)
    - Matched individual keywords get 2 points each
    - Generic terms are penalized to reduce irrelevant matches
    
    Args:
        user_query (str): The question asked by the student
        
    Returns:
        str: The most relevant FAQ answer, or a default message if no match is found
    """
    # Normalize the query for consistent matching
    query = normalize_text(user_query)
    words = query.split()
    query_text = " ".join(words)
    query_set = set(words)  # For fast word lookup

    best_match = None
    max_score = 0

    # Search through all FAQ entries for the best match
    for item in FAQ_DATABASE:
        score = 0
        
        # Score each keyword in this FAQ entry
        for keyword in item.get("keywords", []):
            normalized_keyword = normalize_text(keyword)
            if not normalized_keyword:
                continue

            keyword_words = normalized_keyword.split()

            # Exact phrase matches score higher (e.g., "hostel fees" matches "hostel fees")
            if normalized_keyword in query_text:
                score += 5 if " " in normalized_keyword else 3

            # Add points for each matching keyword word found in the query
            score += sum(2 for word in keyword_words if word in query_set)

            # Penalize overly generic single-word terms to avoid false positives
            # (e.g., "fees" alone shouldn't match all fee-related questions equally)
            if len(keyword_words) == 1 and keyword_words[0] in {"fee", "fees", "exam", "date", "class"}:
                score = max(0, score - 1)

        # Keep track of the best match found so far
        # Keep track of the best match found so far
        if score > max_score:
            max_score = score
            best_match = item["answer"]

    # Return the best answer if a match was found, otherwise provide a help message
    if best_match and max_score > 0:
        return best_match
    return "I'm sorry, I couldn't find information regarding that. Please contact student services at support@college.edu."


# ============================================================================
# Flask Routes - Define endpoints for the web application
# ============================================================================

@app.route('/')
def index():
    """Serve the main chatbot interface."""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the user.
    
    Expected POST data: {"message": "user's question"}
    Returns: {"response": "chatbot's answer"}
    """
    # Extract the user's message from the request
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Validate that the message is not empty
    if not user_message.strip():
        return jsonify({'response': 'Please enter a valid question.'}), 400

    # Find and return the best matching answer
    response = find_best_answer(user_message)
    return jsonify({'response': response})


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == '__main__':
    # Run the Flask development server
    # debug=True enables hot-reloading and better error messages
    # port=5000 is the default Flask development port
    app.run(debug=True, port=5000)
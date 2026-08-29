from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# College FAQ Knowledge Base
FAQ_DATABASE = [
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
        "intent": "timetable",
        "keywords": ["timetable", "schedule", "class", "classes", "timing", "lecture"],
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
    return re.sub(r"[^a-z0-9\s]", "", str(text).lower())


def find_best_answer(user_query):
    """Find the best matching FAQ answer using whole-word/phrase matching."""
    query = normalize_text(user_query)
    words = query.split()
    query_text = " ".join(words)
    query_set = set(words)

    best_match = None
    max_score = 0

    for item in FAQ_DATABASE:
        score = 0
        for keyword in item.get("keywords", []):
            normalized_keyword = normalize_text(keyword)
            if not normalized_keyword:
                continue

            keyword_words = normalized_keyword.split()

            # Prefer exact phrase matches, then exact word matches.
            if normalized_keyword in query_text:
                score += 5 if " " in normalized_keyword else 3

            # Add matched word weight without false positives from substrings.
            score += sum(2 for word in keyword_words if word in query_set)

            # Penalize broad generic terms when they appear without specific context.
            if len(keyword_words) == 1 and keyword_words[0] in {"fee", "fees", "exam", "date", "class"}:
                score = max(0, score - 1)

        if score > max_score:
            max_score = score
            best_match = item["answer"]

    if best_match and max_score > 0:
        return best_match
    return "I'm sorry, I couldn't find information regarding that. Please contact student services at support@college.edu."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message.strip():
        return jsonify({'response': 'Please enter a valid question.'}), 400

    response = find_best_answer(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
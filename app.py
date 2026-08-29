from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# College FAQ Knowledge Base
FAQ_DATABASE = [
    {
        "intent": "fees",
        "keywords": [ "payment", "due date"],
        "answer": "Tuition fees for the current semester are due on September 15th. You can pay via the student portal under the Financials tab."
    },
    {
        "intent": "semester fees",
        "keywords": ["fee", "fees", "cost", "tuition"],
        "answer": "Tution fees for the current semester for CSE CORE was 90000 per semester , for CSE AIML was 120000 per semester, for CSE Data Science was 100000 per semester, for ECE was 80000, for mechanical 80000"
    },
    {
        "intent": "exam_dates",
        "keywords": ["exam", "exams", "date", "dates", "schedule", "midterm", "final"],
        "answer": "The CA's will be from the 5th week from the course started, Midterm exams begin on first week of October. Final exams are scheduled from Mid of December "
    },
    {
        "intent": "library_hours",
        "keywords": ["library", "hours", "open", "timing", "timings", "close"],
        "answer": "The central library is open Monday–Friday from 8:00 AM to 12:00 PM, and weekends from 10:00 AM to 12:00 PM."
    },
    {
        "intent": "timetable",
        "keywords": ["timetable", "schedule", "class", "classes", "timing", "lecture"],
        "answer": "The college timings are from 9:00 AM to 5:00 PM. Class timetables can be downloaded from the Academic Portal after logging in with your student ID."
    },
    {
        "intent": "admission",
        "keywords": ["admission", "apply", "eligibility", "criteria", "deadline"],
        "answer": "Admissions for the upcoming academic session close on August 31st. Visit the official admissions portal to apply.The elgibility criteria for CSE CORE is 60% in 12th, for CSE AIML is 70% in 12th, for CSE Data Science is 65% in 12th, for ECE is 55% in 12th, for mechanical is 50% in 12th"
    },
     {
            "intent": "hostel",
            "keywords": ["hostel", "accommodation", "living", "residence"],
            "answer": "The college provides hostel facilities for both male and female students. The application process and availability details can be found on the Student Services portal."
        },
     {
                    "intent": "hostel fees",
                    "keywords": ["hostel", "fees", "hostel charges", "hostel cost", "mess", "fees", "mess charges", "mess cost", "laundry", "laundry charges", "laundry cost"],
                    "answer": "The college  hostel charges room rent of  93000 per year and the food costs 44000 and laundry charges 54000 "
                },
                 {
                                    "intent": "exam fees",
                                    "keywords": ["exam", "fees", "test fees", "examination fees"],
                                    "answer": "The exam fees for each semester 50000 per semester "
                                },
     {
                    "intent": "hostel",
                    "keywords": ["dress code"],
                    "answer": "The college dress code will be when you are having PEV classes otherwise you can wear civil dress. The dress code is formal attire for all students during college hours. For PEV classes, students are required to wear the official college uniform."
                },
     {
                                    "intent": "nirf_ranking",
                                    "keywords": ["NIRF ranking" "nirf ranking"],
                                    "answer": "The universities is ranked 31st among all universities in India. The Category-Wise NIRF Rankings (2025)Overall: 49th rankPharmacy: 13th rankArchitecture: 24th rankLaw: 26th rankManagement: 44th rankEngineering: 48th rank"
                                },
       

]

def find_best_answer(user_query):
    """Clean query and match against knowledge base keywords."""
    query = re.sub(r'[^\w\s]', '', user_query.lower())
    words = query.split()
    
    best_match = None
    max_score = 0
    
    for item in FAQ_DATABASE:
        score = sum(1 for word in words if word in item["keywords"])
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
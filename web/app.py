from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import sys
import threading
import time
import uuid
import io
import contextlib
import re
from flask import g
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/mytripplanner')))
from crew import Mytripplanner
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global dictionary to store progress and report data
progress_store = {}


AGENT_STEPS = [
    {"name": "Destination Data Researcher", "progress": 20, "task": "destination_research_task"},
    {"name": "Local Expert", "progress": 40, "task": "local_insight_task"},
    {"name": "Itinerary Planner", "progress": 60, "task": "itinerary_task"},
    {"name": "Budget Advisor", "progress": 80, "task": "budget_estimate_task"},
    {"name": "Travel Summary", "progress": 100, "task": "travel_summary_task"}
]

def get_session_id():
    """
    Generate or retrieve session ID for tracking user progress.
    If no session exists, creates a new UUID.
    """
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

class CrewOutputCapture:
    def __init__(self, session_id, progress_store):
        self.session_id = session_id
        self.progress_store = progress_store
        self.agent_patterns = [
            (r"destination.*data.*researcher", "Destination Data Researcher", 20),
            (r"local.*expert", "Local Expert", 40),
            (r"itinerary.*planner", "Itinerary Planner", 60),
            (r"budget.*advisor", "Budget Advisor", 80),
            (r"travel.*summary", "Travel Summary", 100)
        ]
        self.last_detected_agent = None
        
    def detect_agent_from_output(self, text):
        """Detect which agent is currently running from crew output"""
        text_lower = text.lower()
        
        for pattern, agent_name, progress in self.agent_patterns:
            if re.search(pattern, text_lower):
                if self.last_detected_agent != agent_name:
                    self.last_detected_agent = agent_name
                    self.progress_store[self.session_id]['current_agent'] = agent_name
                    self.progress_store[self.session_id]['progress'] = progress
                    print(f"DETECTED AGENT CHANGE: {agent_name} ({progress}%)")
                    return True
        return False
    
    def write(self, text):
        
        sys.__stdout__.write(text)
        sys.__stdout__.flush()
        
        t
        if text and len(text.strip()) > 0:
            self.detect_agent_from_output(text)
    
    def flush(self):
        sys.__stdout__.flush()

def run_agent_async(destination, days, session_id):
    """
    Execute the trip planning crew asynchronously.
    Updates progress store based on actual crew output and execution.
    
    Args:
        destination (str): Target travel destination
        days (str): Number of days for the trip
        session_id (str): Unique session identifier for progress tracking
    """
    try:
        inputs = {"location": destination, "days": days}
        
        
        progress_store[session_id]['current_agent'] = "Initializing..."
        progress_store[session_id]['progress'] = 0
        progress_store[session_id]['start_time'] = time.time()
        
        
        crew_instance = Mytripplanner()
        crew = crew_instance.crew()
        
        output_capture = CrewOutputCapture(session_id, progress_store)
        
        
        def monitor_progress():
            """Monitor actual progress without hardcoded timing"""
            start_time = time.time()
            last_progress_update = time.time()
            
            while progress_store[session_id]['report_status'] == 'pending':
                elapsed_time = time.time() - start_time
                current_progress = progress_store[session_id]['progress']
                
                
                time_since_last_update = time.time() - last_progress_update
                if time_since_last_update > 10 and current_progress < 95:  
                   
                    if current_progress < 20:
                        progress_store[session_id]['progress'] = min(20, current_progress + 1)
                    elif current_progress < 40:
                        progress_store[session_id]['progress'] = min(40, current_progress + 1)
                    elif current_progress < 60:
                        progress_store[session_id]['progress'] = min(60, current_progress + 1)
                    elif current_progress < 80:
                        progress_store[session_id]['progress'] = min(80, current_progress + 1)
                    else:
                        progress_store[session_id]['progress'] = min(95, current_progress + 1)
                    
                    last_progress_update = time.time()
                
              
                if progress_store[session_id]['current_agent'] == "Initializing..." and elapsed_time > 5:
                    progress_store[session_id]['current_agent'] = AGENT_STEPS[0]['name']
                    progress_store[session_id]['progress'] = max(progress_store[session_id]['progress'], 5)
                
                time.sleep(2)  
        
        
        monitor_thread = threading.Thread(target=monitor_progress)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print(f"Starting crew execution for destination: {destination}, days: {days}")
        progress_store[session_id]['current_agent'] = AGENT_STEPS[0]['name']
        progress_store[session_id]['progress'] = 5
        
        
        old_stdout = sys.stdout
        try:
            sys.stdout = output_capture
            
            results = crew.kickoff(inputs=inputs)
        finally:
            sys.stdout = old_stdout
        
        print("Crew execution completed successfully")
        
        #
        progress_store[session_id].update({
            'report_raw': str(results.raw),
            'report_status': 'ready',
            'current_agent': 'Complete',
            'progress': 100
        })
        
    except Exception as e:
        print(f"Error in crew execution: {e}")
        progress_store[session_id].update({
            'report_raw': f"Error generating report: {e}",
            'report_status': 'error',
            'current_agent': 'Error Occurred',
            'progress': 0
        })

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page route - handles form submission and redirects to progress page.
    """
    if request.method == 'POST':
        destination = request.form['destination']
        days = request.form['days']
        session_id = get_session_id()
        
        
        progress_store[session_id] = {
            'report_status': 'pending',
            'report_raw': '',
            'destination': destination,
            'days': days,
            'current_agent': 'Initializing...',
            'progress': 0
        }
        
        #
        thread = threading.Thread(target=run_agent_async, args=(destination, days, session_id))
        thread.daemon = True  
        thread.start()
        
        return redirect(url_for('progress'))
    
    return render_template('home.html')

@app.route('/progress')
def progress():
    """
    Progress page route - shows current agent and progress status.
    """
    session_id = get_session_id()
    data = progress_store.get(session_id, {})
    status = data.get('report_status', 'pending')
    current_agent = data.get('current_agent', 'Initializing...')
    progress_percent = data.get('progress', 0)
    
    return render_template('progress.html', 
                         agent=current_agent, 
                         status=status, 
                         progress=progress_percent)

@app.route('/progress_status')
def progress_status():
    """
    API endpoint for AJAX progress updates.
    Returns JSON with current status, agent, and progress percentage.
    """
    session_id = get_session_id()
    data = progress_store.get(session_id, {})
    
    return jsonify({
        'status': data.get('report_status', 'pending'),
        'agent': data.get('current_agent', 'Initializing...'),
        'progress': data.get('progress', 0)
    })

@app.route('/report')
def report():
    """
    Report page route - displays final trip planning results.
    Redirects to progress if report is not ready.
    """
    session_id = get_session_id()
    data = progress_store.get(session_id, {})
    status = data.get('report_status', 'pending')
    
    
    if status != 'ready' and status != 'error':
        return redirect(url_for('progress'))
    
    
    report_raw = data.get('report_raw', 'No report generated.')
    destination = data.get('destination', 'N/A')
    days = data.get('days', 'N/A')
    
    sample_report = {
        'destination': destination,
        'days': days,
        'sections': [
            {'title': 'Travel Report', 'content': report_raw},
        ]
    }
    
    return render_template('report.html', report=sample_report)

if __name__ == '__main__':
    app.run(debug=True)
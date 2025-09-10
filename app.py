from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
db = TinyDB('incidents.json')
Incident = Query()

@app.route('/')
def index():
    incidents = db.all()
    for incident in incidents:
        if 'history' in incident and len(incident['history']) > 0:
            start_time = datetime.strptime(incident['timestamp'], '%Y-%m-%d %H:%M:%S')
            last_update = datetime.strptime(incident['history'][-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
            duration = last_update - start_time
            incident['work_duration'] = str(duration)
        else:
            incident['work_duration'] = 'N/A'
    return render_template('index.html', incidents=incidents)

@app.route('/add', methods=['POST'])
def add_incident():
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    priority = request.form['priority']
    operator = request.form['operator']
    incident_type = request.form['type']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history = [{
        'timestamp': timestamp,
        'status': status,
        'description': description,
        'operator': operator
    }]
    db.insert({
        'title': title,
        'description': description,
        'status': status,
        'priority': priority,
        'operator': operator,
        'type': incident_type,
        'timestamp': timestamp,
        'history': history
    })
    return redirect(url_for('index'))

@app.route('/update/<int:incident_id>', methods=['POST'])
def update_incident(incident_id):
    status = request.form['status']
    description = request.form['description']
    operator = request.form['operator']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    incidents = db.all()
    if incident_id < len(incidents):
        incident = incidents[incident_id]
        incident['status'] = status
        incident['description'] = description
        incident['operator'] = operator
        incident['history'].append({
            'timestamp': timestamp,
            'status': status,
            'description': description,
            'operator': operator
        })
        db.update(incident, doc_ids=[incident.doc_id])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

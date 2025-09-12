from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import os, uuid

app = Flask(__name__)
db = TinyDB('incidents.json')
Incident = Query()

ARCHIVE_DIR = 'incident_archives'
os.makedirs(ARCHIVE_DIR, exist_ok=True)


@app.route('/')
def index():
    incidents = db.all()

    # DB principale
    for inc in incidents:
        if 'uuid' not in inc:
            inc['uuid'] = str(uuid.uuid4())
            db.update({'uuid': inc['uuid']}, doc_ids=[inc.doc_id])
        inc['unique_id'] = f"main::{inc['uuid']}"

    # Archivi
    for filename in os.listdir(ARCHIVE_DIR):
        if filename.endswith('.json'):
            archive_db = TinyDB(os.path.join(ARCHIVE_DIR, filename))
            for inc in archive_db.all():
                if 'uuid' not in inc:
                    inc['uuid'] = str(uuid.uuid4())
                    archive_db.update({'uuid': inc['uuid']}, doc_ids=[inc.doc_id])
                # assegnazione dell'ID corretto per l'archivio
                inc['unique_id'] = f"archive::{filename}::{inc['uuid']}"
                incidents.append(inc)

    incidents.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    recent = incidents[:10]

    for i in recent:
        if i.get('history'):
            start = datetime.strptime(i['timestamp'], '%Y-%m-%d %H:%M:%S')
            last = datetime.strptime(i['history'][-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
            i['work_duration'] = str(last - start)
        else:
            i['work_duration'] = 'N/A'

    return render_template('index.html', incidents=recent)


@app.route('/add', methods=['POST'])
def add_incident():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    uid = str(uuid.uuid4())
    history = [{
        'timestamp': now,
        'status': request.form['status'],
        'description': request.form['description'],
        'operator': request.form['operator']
    }]
    db.insert({
        'uuid': uid,
        'title': request.form['title'],
        'description': request.form['description'],
        'status': request.form['status'],
        'priority': request.form['priority'],
        'operator': request.form['operator'],
        'type': request.form['type'],
        'timestamp': now,
        'history': history
    })
    return redirect(url_for('index'))


@app.route('/update/<string:unique_id>', methods=['POST'])
def update_incident(unique_id):
    status = request.form['status']
    description = request.form['description']
    operator = request.form['operator']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    source, rest = unique_id.split("::", 1)

    if source == "main":
        inc = db.get(Incident.uuid == rest)
        if inc:
            inc['status'] = status
            inc['description'] = description
            inc['operator'] = operator
            inc['history'].append({
                'timestamp': timestamp,
                'status': status,
                'description': description,
                'operator': operator
            })

            if status.lower() in ['resolved', 'closed']:
                today = datetime.now().strftime('%Y-%m-%d')
                archive_file = os.path.join(ARCHIVE_DIR, f'incidents_archive_{today}.json')
                archive_db = TinyDB(archive_file)

                # clona il record senza doc_id e assegna subito l'unique_id corretto
                to_archive = {k: v for k, v in inc.items() if k != 'doc_id'}
                to_archive['unique_id'] = f"archive::{os.path.basename(archive_file)}::{to_archive['uuid']}"
                archive_db.insert(to_archive)

                db.remove(doc_ids=[inc.doc_id])
            else:
                db.update(inc, doc_ids=[inc.doc_id])

    elif source == "archive":
        fname, uid = rest.rsplit("::", 1)
        archive_file = os.path.join(ARCHIVE_DIR, fname)
        if os.path.exists(archive_file):
            adb = TinyDB(archive_file)
            inc = adb.get(Incident.uuid == uid)
            if inc:
                inc['status'] = status
                inc['description'] = description
                inc['operator'] = operator
                inc['history'].append({
                    'timestamp': timestamp,
                    'status': status,
                    'description': description,
                    'operator': operator
                })
                adb.update(inc, doc_ids=[inc.doc_id])
                adb.compact()

    return redirect(url_for('index'))


@app.route('/incident/<string:unique_id>')
def incident_details(unique_id):
    source, rest = unique_id.split("::", 1)
    incident = None
    if source == "main":
        incident = db.get(Incident.uuid == rest)
    elif source == "archive":
        fname, uid = rest.rsplit("::", 1)
        path = os.path.join(ARCHIVE_DIR, fname)
        if os.path.exists(path):
            adb = TinyDB(path)
            incident = adb.get(Incident.uuid == uid)

    if not incident:
        return "Incident not found", 404

    incident['unique_id'] = unique_id
    if incident.get('history'):
        start = datetime.strptime(incident['timestamp'], '%Y-%m-%d %H:%M:%S')
        last = datetime.strptime(incident['history'][-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
        incident['work_duration'] = str(last - start)
    else:
        incident['work_duration'] = 'N/A'

    return render_template('details.html', incident=incident)


@app.route('/search_archives')
def search_archives():
    query = request.args.get('query', '').lower()
    results = []
    for filename in os.listdir(ARCHIVE_DIR):
        if filename.endswith('.json'):
            adb = TinyDB(os.path.join(ARCHIVE_DIR, filename))
            for inc in adb.search(
                (Incident.title.matches(f'(?i).*{query}.*')) |
                (Incident.description.matches(f'(?i).*{query}.*'))
            ):
                if inc.get('history'):
                    start = datetime.strptime(inc['timestamp'], '%Y-%m-%d %H:%M:%S')
                    last = datetime.strptime(inc['history'][-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
                    inc['work_duration'] = str(last - start)
                else:
                    inc['work_duration'] = 'N/A'
                inc['unique_id'] = f"archive::{filename}::{inc['uuid']}"
                results.append(inc)
    return render_template('archive_results.html', results=results, query=query)


if __name__ == '__main__':
    app.run(debug=True)

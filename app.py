from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import os

app = Flask(__name__)
db = TinyDB('incidents.json')
Incident = Query()

# Path per la directory di archiviazione
ARCHIVE_DIR = 'incident_archives'
if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)


@app.route('/')
def index():
    # Carica tutti gli incidenti dal database principale
    incidents = db.all()

    # Assegna un ID univoco a ogni incidente dal database principale
    for inc in incidents:
        inc['unique_id'] = f"main-{inc.doc_id}"

    # Carica gli incidenti da tutti i file di archivio
    for filename in os.listdir(ARCHIVE_DIR):
        if filename.endswith('.json'):
            archive_db = TinyDB(os.path.join(ARCHIVE_DIR, filename))
            archived_incidents = archive_db.all()
            for inc in archived_incidents:
                # Assegna un ID univoco a ogni incidente archiviato
                inc['unique_id'] = f"archive-{filename}-{inc.doc_id}"
            incidents.extend(archived_incidents)

    # Ordina tutti gli incidenti (aperti e archiviati) per data in ordine decrescente
    incidents.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'), reverse=True)

    # Seleziona solo gli ultimi 10 incidenti
    recent_incidents = incidents[:10]

    for incident in recent_incidents:
        if 'history' in incident and len(incident['history']) > 0:
            start_time = datetime.strptime(incident['timestamp'], '%Y-%m-%d %H:%M:%S')
            last_update = datetime.strptime(incident['history'][-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
            duration = last_update - start_time
            incident['work_duration'] = str(duration)
        else:
            incident['work_duration'] = 'N/A'

    return render_template('index.html', incidents=recent_incidents)


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


@app.route('/update/<string:unique_id>', methods=['POST'])
def update_incident(unique_id):
    status = request.form['status']
    description = request.form['description']
    operator = request.form['operator']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    parts = unique_id.split('-')
    source = parts[0]
    doc_id = int(parts[-1])

    incident = None
    if source == 'main':
        incident = db.get(doc_id=doc_id)
        if incident:
            incident['status'] = status
            incident['description'] = description
            incident['operator'] = operator
            incident['history'].append({
                'timestamp': timestamp,
                'status': status,
                'description': description,
                'operator': operator
            })
            if status.lower() in ['resolved', 'closed']:
                today = datetime.now().strftime('%Y-%m-%d')
                archive_file = os.path.join(ARCHIVE_DIR, f'incidents_archive_{today}.json')
                archive_db = TinyDB(archive_file)
                incident_dict = dict(incident)
                if 'doc_id' in incident_dict:
                    del incident_dict['doc_id']
                archive_db.insert(incident_dict)
                db.remove(doc_ids=[doc_id])
                db.compact()
            else:
                db.update(incident, doc_ids=[incident.doc_id])
    elif source == 'archive':
        filename = '-'.join(parts[1:-1])
        archive_file_path = os.path.join(ARCHIVE_DIR, filename)
        if os.path.exists(archive_file_path):
            archive_db = TinyDB(archive_file_path)
            incident = archive_db.get(doc_id=doc_id)
            if incident:
                incident['status'] = status
                incident['description'] = description
                incident['operator'] = operator
                incident['history'].append({
                    'timestamp': timestamp,
                    'status': status,
                    'description': description,
                    'operator': operator
                })
                archive_db.update(incident, doc_ids=[incident.doc_id])

    return redirect(url_for('index'))


@app.route('/incident/<string:unique_id>')
def incident_details(unique_id):
    parts = unique_id.split('-')
    source = parts[0]
    doc_id = int(parts[-1])

    incident = None
    if source == 'main':
        incident = db.get(doc_id=doc_id)
        if incident:
            # Aggiungi unique_id all'incidente per il form di aggiornamento
            incident['unique_id'] = f"main-{incident.doc_id}"
    elif source == 'archive':
        filename = '-'.join(parts[1:-1])
        archive_file_path = os.path.join(ARCHIVE_DIR, filename)
        if os.path.exists(archive_file_path):
            archive_db = TinyDB(archive_file_path)
            incident = archive_db.get(doc_id=doc_id)
            if incident:
                # Aggiungi unique_id all'incidente per il form di aggiornamento
                incident['unique_id'] = f"archive-{filename}-{incident.doc_id}"

    if incident:
        if 'history' in incident and len(incident['history']) > 0:
            start_time = datetime.strptime(incident['timestamp'], '%Y-%m-%d %H:%M:%S')
            last_update = datetime.strptime(incident['history'][-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
            duration = last_update - start_time
            incident['work_duration'] = str(duration)
        else:
            incident['work_duration'] = 'N/A'
        return render_template('details.html', incident=incident)
    return "Incident not found", 404


@app.route('/search_archives')
def search_archives():
    query = request.args.get('query', '').lower()
    results = []

    for filename in os.listdir(ARCHIVE_DIR):
        if filename.endswith('.json'):
            archive_db = TinyDB(os.path.join(ARCHIVE_DIR, filename))
            found_incidents = archive_db.search(
                (Incident.title.matches(f'(?i).*{query}.*')) |
                (Incident.description.matches(f'(?i).*{query}.*'))
            )

            for inc in found_incidents:
                if 'history' in inc and len(inc['history']) > 0:
                    start_time = datetime.strptime(inc['timestamp'], '%Y-%m-%d %H:%M:%S')
                    last_update = datetime.strptime(inc['history'][-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
                    duration = last_update - start_time
                    inc['work_duration'] = str(duration)
                else:
                    inc['work_duration'] = 'N/A'
                inc['unique_id'] = f"archive-{filename}-{inc.doc_id}"  # Crea l'ID unico
                results.append(inc)

    return render_template('archive_results.html', results=results, query=query)


if __name__ == '__main__':
    app.run(debug=True)
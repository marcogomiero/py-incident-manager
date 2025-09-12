🛠️ Py Incident Manager
==========================

A lightweight web application for managing incidents and planned activities/changes in a control room, built with Flask and TinyDB.

* * * * *

✨ Key Features
--------------

-   Add and view incidents and planned activities/changes
-   Edit status, description, operator, and type
-   Track update history with timestamps and operator info
-   Automatically calculate work duration
-   Manual operator assignment
-   Timestamp logging for creation and updates
-   Local database using TinyDB (JSON file)

* * * * *

📦 Requirements
---------------

-   Python 3.x
-   Flask
-   TinyDB

Install required packages:

```
pip install flask tinydb
```

* * * * *

🚀 How to Run
-------------

1.  Clone the repository:

```
git clone https://github.com/marcogomiero/py-incident-manager.git
```

1.  Navigate to the project folder:

```
cd py-incident-manager
```

1.  Start the app:

```
python app.py
```

1.  Open your browser at:

```
http://127.0.0.1:5000
```

* * * * *

📁 Project Structure
--------------------

```
incident-manager/
├── app.py
├── incidents.json
└── templates/
    └── index.html
```

* * * * *

📌 Notes
--------

-   The database is a simple JSON file (`incidents.json`)
-   All data is stored locally
-   The interface is designed to be simple and functional
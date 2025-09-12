📛 **Py Incident Manager**\
A lightweight web application for managing incidents and planned activities or changes in a control room, built with **Flask**, **TinyDB**, and a **Bootstrap 5** front-end.

* * * * *

✨ **Key Features**\
- **Add and view** incidents and planned activities/changes\
- **Edit** status, description, operator, and type\
- **Track update history** with timestamps and operator information\
- **Automatic calculation** of work duration\
- **Manual operator assignment**\
- **Timestamp logging** for creation and updates\
- **Local database** powered by TinyDB (JSON file)\
- **Responsive UI** using locally hosted Bootstrap 5 (no external CDN required)

* * * * *

📦 **Requirements**\
- Python 3.x\
- Flask\
- TinyDB

Install the required packages:\
`pip install flask tinydb`

* * * * *

🚀 **How to Run**\
1️⃣ **Clone the repository**\
`git clone https://github.com/marcogomiero/py-incident-manager.git`

2️⃣ **Navigate to the project folder**\
`cd py-incident-manager`

3️⃣ **Start the application**\
`python app.py`

4️⃣ **Open your browser**\
`http://127.0.0.1:5000`

* * * * *

📁 **Project Structure**\
py-incident-manager/\
- app.py\
- incidents.json\
- static/\
  - bootstrap.min.css\
  - bootstrap.bundle.min.js\
- templates/\
  - base.html\
  - index.html\
  - details.html

* * * * *

📝 **Notes**\
- The database is a simple JSON file (`incidents.json`); all data is stored locally.\
- The UI uses **Bootstrap 5** served from the `static` directory, so it works even without an internet connection.\
- Designed to be lightweight, easy to run, and quick to deploy on any machine with Python installed.
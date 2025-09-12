⚡️ Py Incident Manager
======================

A sleek, zero-setup web app to **track, update, and close incidents** in real time.\
Built with **Flask**, **TinyDB**, and a fully responsive **Bootstrap 5** interface.\
Run it locally, offline, and look like you own the control room.

* * * * *

✨ Features That Actually Matter
-------------------------------

-   🆕 **Create incidents in seconds** -- no page reloads, just click and type.

-   🔄 **Live updates & full history** -- every status change is timestamped and attributed.

-   ⏱ **Automatic work-duration tracking** -- stop guessing how long an outage lasted.

-   📂 **Archive & restore** -- closed incidents slide into a tidy archive but stay searchable.

-   💻 **Offline-ready** -- TinyDB JSON storage means **no external DB, no internet required**.

-   🎨 **Polished UI** -- dark navbar, color-coded badges, modals that actually look good.

* * * * *

🖼 Screenshots (coming soon)
--------------

**Dashboard**

**Add New Incident**

**Incident Details & History**

* * * * *

🚀 Quick Start
--------------

1.  **Clone the repo**

    `git clone https://github.com/marcogomiero/py-incident-manager.git
    cd py-incident-manager`

2.  **Install dependencies**

    `pip install flask tinydb`

3.  **Run the app**

    `python app.py`

4.  **Open your browser**

    `http://127.0.0.1:5000`

You'll be managing incidents before your coffee gets cold.

* * * * *

🛠 Tech Stack
-------------

-   **Flask** -- lightweight Python web framework

-   **TinyDB** -- schema-less JSON database

-   **Bootstrap 5 (local)** -- responsive, mobile-first UI with zero CDN dependencies

* * * * *

📂 Project Structure
--------------------

`py-incident-manager/
├── app.py
├── incidents.json
├── static/
│   ├── bootstrap.min.css
│   └── bootstrap.bundle.min.js
└── templates/
    ├── base.html
    ├── index.html
    └── details.html`

* * * * *

📝 Notes
--------

-   All data stays local in `incidents.json`---perfect for air-gapped environments.

-   Designed to be **minimal, fast, and ridiculously easy** to deploy on any machine with Python.
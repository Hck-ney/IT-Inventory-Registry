# Asset-Lifecycle-Tracker 🚀

A professional IT Inventory Management system built with **Django** and **PostgreSQL**. This application tracks the movement of company hardware from initial procurement through employee assignment, repair cycles, and final decommissioning.

## 🛠️ Key Functionalities
* **Lifecycle Management:** Tracks asset states (Available, Assigned, In Repair, Retired).
* **Employee Mapping:** Links hardware directly to staff members with assignment history.
* **Automated Status Logic:** Logic-driven badges that update based on equipment health and location.
* **Production Ready:** Configured with WhiteNoise for static files and Gunicorn for high-performance hosting.

## 🧰 Tech Stack
* **Framework:** Django (Python)
* **Database:** PostgreSQL
* **Deployment:** Render
* **Static Assets:** WhiteNoise
* **Environment Handling:** Decoupled secrets using Environment Variables
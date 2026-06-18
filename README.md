# School Hub 🏫

School Hub is a secure, sandboxed web-based networking and bulletin board platform built exclusively for students utilizing the official EMIS infrastructure (`@students.gov.ge`). 

By parsing and validating the school handle from the student’s email address upon registration, the system dynamically groups and partitions user activity profiles. This ensures that announcements, updates, and campus posts remain completely sandboxed and visible only to peers attending that exact same institution.

---

## 🚀 Features

* **EMIS Sandboxed Feeds:** Data separation by school domain. Students only view and interact with posts created by peers within their own school network context.
* **Three-Table Relational Database Architecture:** Structured entirely using a normalized SQL relationship layout managed via SQLite and SQLAlchemy.
* **Full Post Management (CRUD):** Authenticated students can create text-based notices, optionally upload image attachments, and delete their own active publications.
* **Interactive Engagement:** Built-in validation tracking for student interactions allowing users to "Like" posts within their institution.
* **Modern Form Validation:** Full front-end/back-end verification using WTForms, including custom email domain rules and standard parameter checks.
* **Clean Light Mode Interface:** Designed with a professional, high-contrast light theme built on standard Bootstrap 5 layouts for exceptional legibility.

---

## 📊 Database Architecture

The backend implements a normalized relational database design containing **exactly three primary model entities** isolated within the localized folder context:

1.  **`School` Table:** Tracks unique institutional domains extracted from registration strings.
2.  **`User` Table:** Holds student registration metadata (Name, Student ID, Grade, Email, Hashed Password) linked directly to their parent `School` ID record.
3.  **`Post` Table:** Contains bulletin announcements, optional image file paths, creation timestamps, and relationship links back to the author (`User`) and context (`School`).

*An internal, lightweight many-to-many intermediate table (`post_likes`) is utilized strictly to track relational user-to-post liking vectors without adding unneeded entity models.*

---

## 🛠️ Project Structure

```text
students_web/
│
├── instance/
│   └── school_hub.db      # Reconfigured SQLite isolated destination database
├── static/
│   ├── images/            # Dynamically processed user image uploads
│   └── style.css          # Customized corporate indigo light-mode layout definitions
├── templates/
│   ├── base.html          # Global Bootstrap structural outer shell setup
│   ├── index.html         # School-partitioned home dashboard grid feed
│   ├── details.html       # Isolated target announcement expand panel
│   ├── add_post.html      # Content creation form panel
│   ├── login.html         # Secure registration/login views
│   ├── register.html      
│   └── about.html         
├── app.py                 # Application launcher
├── ext.py                 # Core initialization container (Flask, SQLAlchemy, LoginManager)
├── models.py              # Three-table schema database blueprints
├── forms.py               # WTForms backend configuration rules
└── init_db.py             # Script to cleanly regenerate target database tables

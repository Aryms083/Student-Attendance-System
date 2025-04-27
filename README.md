# Student Attendance System

This is a **Python-based Student Attendance System** that uses **facial recognition** to automate the process of marking attendance.  
It integrates with **Firebase** for real-time data storage and file management.

---

## Features

- 🔥 Real-time face recognition and attendance marking
- ☁️ Secure integration with **Firebase** for database and storage
- 🖼️ Beautiful UI with background images from a custom **resources** folder
- 🧠 User-friendly scripts for:
  - Encoding new student faces
  - Adding student data to the database
  - Creating and managing usernames

---

## Project Structure

| File/Folder            | Purpose |
|-------------------------|---------|
| `main2.py`              | Main execution file to run the attendance system |
| `encoding_generator.py` | Generates facial encoding files (`.p` format) |
| `add_to_database.py`    | Adds new student records to the Firebase database |
| `username.py`           | Creates and manages unique usernames |
| `resources/`            | Contains background images used by the UI |
| `ServiceAccountKey.json`| Firebase service account credentials *(Not uploaded for security)* |

---

## Setup Instructions

1. Clone this repository.
2. Set up a **Firebase** project and download the service account key.
3. Place your `ServiceAccountKey.json` inside the project folder.
4. Install required Python libraries:

   ```bash
   pip install -r requirements.txt

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
   Run the encoding generator to add new students:

python encoding_generator.py
Add students to the database using:

python add_to_database.py
Start the attendance system:

python main2.py
Notes
Secrets like Firebase keys are never pushed to the public repository.

Please configure Firebase Storage and Realtime Database with the correct permissions.

All images for UI backgrounds must be placed in the resources folder.

Disclaimer
This project is developed for educational purposes and internal use.
Any unauthorized copying, distribution, or public hosting without permission is discouraged.

License
© 2025 Aryms083 - All rights reserved.

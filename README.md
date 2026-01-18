# Videoflix

Videoflix is a video streaming application consisting of a backend powered by Docker and a separate frontend application.

---

- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables-env)
- [How to Use](#how-to-use)

---

## Prerequisites

Before starting the project, make sure the following tools are installed and properly configured on your system:

- **Python (>= 3.10)**
  - Required for local development and dependency management
  - Verify installation:
    ```bash
    python --version
    ```

- **FFmpeg**  
  - Must be installed and available in your system `PATH`
  - **Add FFmpeg to PATH (Windows):**
    1. Download FFmpeg from the official website.
    2. Extract the archive (e.g. to `C:\ffmpeg`).
    3. Open *System Properties* → *Environment Variables*.
    4. Under *System variables*, select `Path` → *Edit*.
    5. Add the path to the `bin` folder (e.g. `C:\ffmpeg\bin`).
    6. Save and restart your terminal.
  - **Add FFmpeg to PATH (macOS / Linux):**
    - Install via package manager:
      ```bash
      brew install ffmpeg
      ```
      or
      ```bash
      sudo apt install ffmpeg
      ```
    - Verify installation:
      ```bash
      ffmpeg -version
      ```

- **Docker Desktop**
  - Install Docker Desktop and make sure it is running before starting the backend.

---

## Backend Setup

1. Clone the backend repository:
```bash
git clone https://github.com/Hummner/Videoflix.git .
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
```

- **Windows**
```bash
venv\Scripts\activate
```

- **macOS / Linux**
```bash
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create the environment file:
```bash
cp .env.template .env
```

5. Open the `.env` file and fill in all required environment variables.

6. Start the backend using Docker:
```bash
docker compose up --build
```
or
```bash
docker-compose up --build
```

---

## Frontend Setup

1. Clone the frontend repository:
```bash
git clone https://github.com/Developer-Akademie-Backendkurs/project.Videoflix
```

2. Open the frontend project in your code editor (for example VS Code).

3. Start the project using **Live Server**.

4. Open the application in your browser via the provided Live Server URL.

---

## Notes

- Make sure Docker Desktop is running before starting the backend.
- FFmpeg is required for video processing and must be accessible globally.
- Backend and frontend are handled in separate repositories.

### Line Endings (Windows)

If you encounter issues running shell scripts inside Docker, make sure the file uses **LF** line endings.

- Open the `.sh` file in **VS Code**
- Change `CRLF` to `LF` (bottom-right corner)
- Save the file and rebuild the containers

---


## Environment Variables (.env)

This project uses environment variables for configuration.
Create a .env file based on .env.template and fill in the following values:

1. Django Admin User
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com


Credentials for the automatically created Django superuser

Used to access the Django admin panel (/admin)


2. Database Configuration (PostgreSQL)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=db
DB_PORT=5432


Database credentials used by Django

DB_HOST=db refers to the PostgreSQL service name defined in docker-compose.yml

Default PostgreSQL port is 5432

3. Email Configuration
EMAIL_HOST=your_email_host
EMAIL_PORT=587
EMAIL_HOST_USER=your_email_username
EMAIL_HOST_PASSWORD=your_email_passaword
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=your_email (e.g Videoflix Support <firstname@lastname.com>)


Used for sending emails (e.g. account-related emails)

EMAIL_PORT=587 with EMAIL_USE_TLS=True is recommended

Fill in EMAIL_HOST_USER and EMAIL_HOST_PASSWORD with valid credentials

DEFAULT_FROM_EMAIL defines the sender address

Security Note

⚠️ Never commit the .env file to version control.
It contains sensitive information and must remain private.


# How to use

## Add Videos (Admin Panel Only)

Videos can only be added via the Django Admin panel. Adding videos via the REST API is not supported.

 - Make sure the backend is running.

1. Open the Django Admin panel in your browser:

   http://localhost:8000/admin


2. Log in with the superuser credentials from your .env:

 - DJANGO_SUPERUSER_USERNAME

 - DJANGO_SUPERUSER_PASSWORD

3. In the admin dashboard, navigate to the video section (Videos).

4. Click **Add** and upload the video (and fill in any additional required fields).
  - The **thumbnail is optional**.
  - If no thumbnail is provided, the application will automatically generate one from the **first frame** of the video.
  - A **custom thumbnail can be added later**.
  - The **video file itself cannot be modified** after it has been uploaded.

5. Save the entry.

After saving, the backend will process the video and make it available in the application.

## Frontend Features

In the frontend you can:

Register a new account

Activate your account (via activation email)

Reset your password

Watch videos in multiple quality levels (depending on what is available)

## Project Name

**Videoflix**

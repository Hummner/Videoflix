# Videoflix

Videoflix is a video streaming application consisting of a backend powered by Docker and a separate frontend application.

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

(Optional) Freeze installed dependencies:
```bash
pip freeze > requirements.txt
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

---

## Project Name

**Videoflix**

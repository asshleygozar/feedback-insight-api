# Feedback Insights API

An AI powered api server that takes single or batch like input of likert scale and open-ended questions that gets analyze by LLM (Large Language Model) and provide sentiment analysis using structured response.

I built this project to deepen my understanding of fundamentals of Applied AI Engineering. The idea came from my previous capstone research project where I have integrated sentiment analysis for student satisfaction survey where our backend analyze and understand sentiment feedback from the students and return categorized and structurized response for a thorough understanding of students thoughts and experiences.

## Technology Stack
This project is built thanks to the following technologies

**Backend Technologies**

- Python v3.12.13 (Programming Language)
- FastAPI v0.139.2 (Server Framework)
- Uvicorn v0.51.0" (ASGI Web server)

**CI/CD**

- Docker (For containerization and portability)
- Github Actions (Automation of deployment)

## Functionalities
- Analyzes single object feedback consisting of open-ended response with likert scale with label and weight points
- Batch analysis of array of object of feedback consisting of open-ended responses and liker scales with label and weight points from different respondees

## Getting Started

Follow the steps below to run the server api both on development and production mode

### Development Mode

**Step 1:** First clone the fork of the original repo and copy the https url from the code button

```bash
git clone <https url of your own fork repo>
```

**Step 2:** Inside of your directory where the cloned repository resides, change directory to feedback-insight-api

```bash
cd feedback-insight-api
```

**Step 3:** Configure env file by copying .env.example into your own .env file.

```bash
cp .env.example .env
```

**Step 4:** Setup and install project dependencies by following the command

```bash
uv sync
```

**Step 5:** Run the application using the command

```bash
uv run uvicorn app.main:app --reload --port <your_port_here> # This runs directly using web server defaults to port 8000 if port not provided

# or

uv run app/main.py # This automatically use the port you have configure on .env file
```

### Production Mode

Not available yet

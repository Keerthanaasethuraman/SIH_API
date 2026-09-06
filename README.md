# SIH API Backend

Backend API for the Smart India Hackathon (SIH) surveillance project.

## Project Architecture

Frontend → API → Backend → PostgreSQL Database

AI → API → PostgreSQL Database

## Technologies Used

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Psycopg2
- JWT Authentication
- Pydantic

## Current Completed Features

### Authentication
- User registration
- User login
- JWT access token generation
- JWT protected API endpoints

### Cameras
- Create camera
- Get all cameras
- Update camera
- Delete camera

### Persons
- Create person
- Get persons
- Update person
- Delete person

### Detections
- Create detection
- Get detections
- Detection classification
- Confidence score
- Camera association
- Person association

### Alerts
- Create alert
- Get alerts
- Resolve alert

### Evidence
- Create evidence metadata
- Get evidence metadata

### Dashboard
- Total cameras
- Active cameras
- Total persons
- Total detections
- Authorized detections
- Unauthorized detections
- Active alerts
- Total evidence

### History
- Detection history
- Alert history

## Project Structure

```text
SIH_API/
├── main.py
├── database.py
├── auth_utils.py
├── auth_dependency.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── models/
│   ├── user.py
│   ├── camera.py
│   ├── alert.py
│   ├── detection.py
│   ├── person.py
│   └── evidence.py
│
├── schemas/
│   └── user.py
│
└── routers/
    ├── auth.py
    ├── cameras.py
    ├── alerts.py
    ├── detections.py
    ├── persons.py
    ├── evidence.py
    ├── dashboard.py
    └── history.py
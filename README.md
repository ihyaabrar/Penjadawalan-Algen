# Scheduling System

A professional scheduling system built with Flask and React.

## Features

- User authentication and authorization
- Course management
- Room management
- Teacher management
- Schedule optimization using genetic algorithm and tabu search
- Real-time monitoring and analytics
- Export functionality for schedules

## Tech Stack

### Backend
- Flask
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Prometheus Monitoring

### Frontend
- React
- Material-UI
- Redux Toolkit
- Axios
- Formik + Yup

## Setup

### Backend

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://localhost/scheduling_db
JWT_SECRET_KEY=your-jwt-secret-key-here
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the backend:
```bash
python src/app.py
```

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the frontend:
```bash
npm start
```

## API Documentation

The API documentation is available at `/api/docs` when the backend is running.

## Monitoring

Prometheus metrics are available at `/metrics`.

## License

MIT

# Deloitte Graduate Hiring – Java & API Development Track

## Candidate Info
- **Full Name:** [Your Full Name]
- **Email:** [Your Email]
- **College:** [Your College Name]
- **Skill Track:** Java & API Development

## Project Overview
This project demonstrates Java fundamentals and API development:
1. OOP – Employee Management (Inheritance, Polymorphism, Streams)
2. Data Structures – Custom Stack, Queue, Linked List
3. Algorithms – Bubble Sort, Merge Sort, Binary Search, Fibonacci (memoized)
4. Exception Handling & File I/O
5. REST API Server using Java's built-in HttpServer

## How to Run

### On Replit (Java environment)
Just click **Run** – Replit will compile and execute `Main.java` automatically.

### Locally
```bash
javac Main.java
java Main
```

## API Endpoints (Task 5)
Once running, the server starts on port **8080**:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/employees` | List all employees |
| GET | `/api/employees/{id}` | Get employee by ID |

Test with:
```bash
curl http://localhost:8080/api/health
curl http://localhost:8080/api/employees
curl http://localhost:8080/api/employees/1
```

> Press **ENTER** in the terminal to stop the server after testing.

# Abuhurairah Faheem — BSCS23077

# StudySync Distributed Systems Resiliency Assignment
### Parallel and Distributed Computing (PDC)

---

# Project Overview

This project is a practical implementation of distributed systems fault-tolerance patterns using a FastAPI backend.

The original StudySync architecture suffered from several real-world distributed system failures:

- synchronous external API dependencies,
- cascading failures,
- blocked backend workers,
- poor fault isolation,
- degraded application availability.

This implementation redesigns the backend using a **Circuit Breaker Pattern with Fallback Responses** to improve resiliency and maintain system availability during external LLM outages.

---

# Real Production Problem

The original backend directly waited for responses from an external LLM API.

## Original Flow

```text
Client Request
      ↓
FastAPI Backend
      ↓
External LLM API
      ↓
Wait until timeout
```

If the external API became:
- slow,
- unavailable,
- overloaded,
- rate-limited,

then FastAPI workers remained blocked for several seconds.

Under concurrent traffic:
- requests accumulated,
- latency increased,
- worker exhaustion occurred,
- the entire backend became unstable.

This is a classical distributed systems cascading failure problem.

---

# Engineering Goal

The goal of this project was to:

- isolate external dependency failures,
- prevent backend worker exhaustion,
- implement graceful degradation,
- improve availability,
- reduce latency during outages,
- simulate real production resiliency behavior.

---

# Implemented Solution

This project implements:

## Circuit Breaker Pattern

The circuit breaker monitors external API failures.

After repeated failures:
- the breaker opens,
- backend stops calling the failing API,
- fallback responses are returned instantly.

This prevents:
- unnecessary waiting,
- cascading failures,
- system-wide latency spikes.

---

# Architecture Design

## Without Circuit Breaker

```text
User Requests
      ↓
FastAPI Backend
      ↓
External LLM API (Slow/Down)
      ↓
Workers Blocked
      ↓
Application Latency Increases
```

---

## With Circuit Breaker

```text
User Requests
      ↓
FastAPI Backend
      ↓
Circuit Breaker
      ↓
External LLM API

If failures exceed threshold:
      ↓
Circuit Opens
      ↓
Fallback Response Returned Instantly
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| FastAPI | Backend Framework |
| Python AsyncIO | Asynchronous request handling |
| HTTPX | Concurrent request simulation |
| Uvicorn | ASGI Server |
| Custom Middleware | Required assignment header |

---

# Project Structure

```text
StudySync-PDC/
│
├── main.py
├── llm_service.py
├── middleware.py
├── test_failure.py
├── requirements.txt
└── README.md
```

---

# Distributed Systems Concepts Demonstrated

## 1. Fault Tolerance

The backend continues functioning even when the external LLM fails.

---

## 2. Graceful Degradation

Instead of crashing, the system returns fallback responses.

Example:

```json
{
  "status": "circuit_open",
  "response": "LLM unavailable. Cached response returned instantly."
}
```

---

## 3. Fail-Fast Architecture

The backend stops waiting for unhealthy dependencies after repeated failures.

---

## 4. Cascading Failure Prevention

Slow external APIs no longer block backend workers.

---

# Circuit Breaker Logic

The breaker tracks:

- failure count,
- timeout window,
- service recovery state.

## States

| State | Behavior |
|---|---|
| Closed | Requests flow normally |
| Open | Requests fail immediately |
| Half-Open | System tests recovery |

---

# Failure Simulation Methodology

The project simulates a real unstable external LLM provider.

## Simulated Failure Conditions

- 80% API failure rate
- artificial timeout delays
- concurrent request bursts

---

# Test Methodology

The script:

```bash
python test_failure.py
```

sends 10 concurrent requests to the backend.

Two scenarios are tested:

## Scenario 1 — Without Circuit Breaker

Expected behavior:
- requests wait for slow API,
- latency increases,
- backend responsiveness degrades.

---

## Scenario 2 — With Circuit Breaker

Expected behavior:
- backend stops calling unhealthy API,
- requests return instantly,
- application remains responsive.

---

# Experimental Results

## Without Circuit Breaker

```text
===== TESTING WITHOUT CIRCUIT BREAKER =====

Total Time: 8.18 seconds
```

### Observed Behavior

- workers blocked,
- long response times,
- backend slowdown,
- poor scalability.

---

## With Circuit Breaker

```text
===== TESTING WITH CIRCUIT BREAKER =====

Total Time: 0.11 seconds
```

### Observed Behavior

- immediate fallback responses,
- fail-fast execution,
- backend stability maintained,
- latency drastically reduced.

---

# CAP Theorem Discussion

This implementation prioritizes:

| Property | Priority |
|---|---|
| Availability | High |
| Partition Tolerance | High |
| Strict Consistency | Lower |

During external API outages:
- maintaining responsiveness is more important than waiting for perfect consistency.

This is a practical trade-off commonly used in real production systems.

---

# Middleware Requirement

The assignment required a custom HTTP header:

```text
X-Student-ID: BSCS23077
```

This was implemented using FastAPI middleware.

Example:

```python
response.headers["X-Student-ID"] = "BSCS23077"
```

---

# Setup Instructions

## 1. Install Python

Download Python:

https://www.python.org/downloads/

---

## 2. Install Dependencies

```bash
pip install fastapi uvicorn httpx
```

---

## 3. Run Backend

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

# API Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Health check |
| `/without-breaker` | Simulates vulnerable backend |
| `/with-breaker` | Simulates resilient backend |

---

# Run Failure Simulation

Open another terminal:

```bash
python test_failure.py
```

---

# Expected Output

## Without Breaker

```text
Total Time: 8+ seconds
```

---

## With Breaker

```text
Total Time: <1 second
```

---

# Demo Video Methodology

The demonstration video shows:

1. Original vulnerable architecture
2. Slow failing requests without resiliency
3. Circuit breaker activation
4. Fast fallback responses
5. Backend remaining responsive during outages

---

# Real-World Relevance

This architecture pattern is widely used in:

- Netflix microservices,
- Stripe payment infrastructure,
- cloud API gateways,
- AI SaaS platforms,
- distributed backend systems.

Circuit breakers are essential in production systems where external dependencies cannot be trusted to remain healthy continuously.

---

# Conclusion

This project transforms the original StudySync backend from a fragile synchronous architecture into a fault-tolerant distributed system.

The implementation successfully demonstrates:

- fault isolation,
- graceful degradation,
- fail-fast execution,
- latency reduction,
- resiliency engineering,
- distributed systems reliability patterns.

The experimental results clearly show how circuit breakers protect backend availability during unstable external service conditions.

---

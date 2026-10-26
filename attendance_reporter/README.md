# Attendance Report Generator

A modular Python system for parsing, processing, and managing attendance reports, ensuring data integrity and working with immutable models (Frozen Dataclasses).

## System Requirements
- Python 3.10 or higher
- pytest (for running tests)

## Project Structure
- `src/models/`: Definition of domain models and types.
- `src/parsing/`: OCR services, classification component, and parsing templates (Template Method) for Type A and Type B reports.
- `src/transformation/`: Invariant enforcement (InvariantValidator) and processing/hour calculation strategies (Strategy Pattern).
- `src/generation/`: Output generator for creating processed files.
- `tests/`: Unit and integration test suite.

## Running the Test Suite
To run all system tests using pytest, execute the following in the terminal:
```bash
pytest -v -s
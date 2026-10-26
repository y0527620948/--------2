# Decision Log - Attendance Report Generator

This document records the architectural and core decisions made during the system's development:

1. **Data Immutability (Frozen Dataclasses):**
   - **Decision:** Using frozen models for the data structures of reports and rows.
   - **Rationale:** Ensuring raw and parsed data are not accidentally affected or modified during transformation stages, preserving information integrity and reliability.

2. **Template Method Pattern for Parsing:**
   - **Decision:** Creating an abstract base class that centralizes common pipeline steps and requires specific implementations for subclasses of different report types.
   - **Rationale:** Preventing code duplication and creating a unified, stable working interface.

3. **Strategy Pattern for Transformation:**
   - **Decision:** Separating processing logic and calculations into dedicated strategy classes for each report type.
   - **Rationale:** Adhering to development principles that allow easy extensibility and the addition of new report types or future calculation rules without modifying core code.

4. **Factory Class for Routing:**
   - **Decision:** Centralizing parser and strategy selection in a central Factory class.
   - **Rationale:** Preventing scattered conditional branching and concentrating the decision point in one clear location.

5. **Invariant Validation:**
   - **Decision:** Creating an independent validation component for hours and logical data (such as validating check-in and check-out times).
   - **Rationale:** Preventing incorrect data from entering processing stages and ensuring business consistency.
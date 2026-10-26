# Architecture Overview - Attendance Report Generator

The Attendance Report Generator system is built on a Layered Architecture that clearly separates the parsing, transformation, validation, and generation stages.

## System Layers

1. **Domain Models Layer:**
   - Contains data types and immutable domain models (`AttendanceRow`, `AttendanceReport`) defined as `frozen dataclasses` to ensure no unintended modifications occur during the processing pipeline.

2. **Parsing & OCR Layer:**
   - **OCR & Cleaning:** Raw text cleaning and preparation for analysis.
   - **Classifier:** A classification mechanism that identifies the report type (`TYPE_A` or `TYPE_B`).
   - **Template Method Pattern:** An abstract base parser class (`BaseParser`) encapsulating shared logic, alongside specialized parsers (`TypeAParser`, `TypeBParser`) that convert text into domain models.
   - **Factory Pattern (`ReportPipelineFactory`):** Centralizes the dynamic routing of the correct parser and strategy based on the report type, avoiding scattered conditional branching.

3. **Transformation & Invariants Layer:**
   - **InvariantValidator:** A domain rule enforcement layer (such as ensuring departure time is later than arrival time) to guarantee business logic integrity.
   - **Strategy Pattern:** Separate processing strategies (`TypeATransformationStrategy`, `TypeBTransformationStrategy`) that execute necessary computations and hour distributions.

4. **Generation Layer:**
   - **Report Generator:** The component responsible for producing final output files cleanly, while fully preserving source files in Read-Only mode.
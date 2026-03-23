# Module 03 Python Port — Shaping Notes

## Scope
Port Module 03 (Anti-Corruption Layer) from Java/Quarkus to Python/FastAPI, following patterns established in Modules 01-02 Python ports.

## Decisions
- Separate directory: `03-Anticorruption-Layer-Python/`
- Same tech stack as Modules 01-02 (FastAPI, SQLAlchemy, aiokafka, pytest)
- Domain enums use `enum.Enum` (no framework dependency)
- External system models use Pydantic `BaseModel` (HTTP boundary)
- Aggregate does NOT store meal_preference/tshirt_size (matches Java)
- Add tests even though Java Module 03 has none

## Context
- **Visuals:** None
- **References:** Java Module 03 solution, Python Module 02 solution
- **Product alignment:** Phase 1 MVP — port Modules 01-03

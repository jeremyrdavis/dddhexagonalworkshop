# Plan: Port Module 03 (Anti-Corruption Layer) to Python

Port the Java Anti-Corruption Layer module to Python, adding integration with a fictional "Salesteam" external system. The ACL translates external models into domain commands, protecting domain purity.

## Key Decisions
- Aggregate does NOT store meal_preference/tshirt_size (matches Java)
- Python enums for domain value objects, Pydantic for external models
- Address becomes optional in command (Salesteam doesn't provide it)
- Size XS coerced to S in translator

## Tasks
1. Scaffold from Module 02 Python solution
2. Add MealPreference/TShirtSize enums, update command
3. Create external system models (Pydantic)
4. Implement SalesteamToDomainTranslator
5. Create Salesteam endpoint (POST /salesteam/)
6. Tests for translator, endpoint, enums
7. Documentation (5 steps + Overview + README)

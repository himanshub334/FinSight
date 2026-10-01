# Operations

Recommended production controls:
- Store trained artifacts in S3 with immutable version identifiers.
- Store dataset hash and feature schema with every model.
- Monitor drift and precision/recall after feedback labels arrive.
- Alert when feature completeness drops below 90%.
- Use a secrets manager for database credentials.
- Schedule retraining through AWS Lambda/EventBridge.

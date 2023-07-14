create_owner_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email", "pattern": "^\\S+@\\S+\\.\\S+$"},
        "password": {"type": "string"}
    },
    "required": ["email", "password"]
}

create_opinion_schema = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "rating": {"type": "integer", "minimum": 0, "maximum": 5}
    },
    "required": ["text", "rating"]
}

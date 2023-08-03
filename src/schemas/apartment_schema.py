create_apartment_schema = {
    "type": "object",
    "properties": {
        "apartment_name": {"type": "string"},
        "number_of_rooms": {"type": "integer"},
        "number_of_guests": {"type": "integer"},
        "price": {"type": "integer"}
    },
    "required": ["apartment_name", "number_of_rooms", "number_of_guests", "price"]
}

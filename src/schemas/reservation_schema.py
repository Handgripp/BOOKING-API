create_reservation_schema = {
    "type": "object",
    "properties": {
        "date_from": {"type": "string", "format": "date"},
        "date_to": {"type": "string", "format": "date"},
        "number_of_guests": {"type": "integer"},
        "room_deposit": {"type": "integer"},

    },
    "required": ["date_from", "date_to", "number_of_guests", "room_deposit"]
}

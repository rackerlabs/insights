inventory = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "hostname": {"type": "string", "maxLength": 100},
        },
    "required": ["hostname"],
}
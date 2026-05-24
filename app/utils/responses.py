"""Handels Responses and Converts to XML/CSV"""
from dicttoxml import dicttoxml
from fastapi import Response
from app.schemas.olympic import OlympicEventOut
import csv
import io


def to_xml(data: list) -> Response:
    """Convert a list of dicts to an XML response."""
    content = dicttoxml(data, custom_root="events", item_func=lambda x: "event", attr_type=False)
    return Response(content=content, media_type="application/xml")


def to_csv(data: list) -> Response:
    """Convert a list of dicts to a CSV response."""
    buffer = io.StringIO()
    if not data:
        return Response(content="", media_type="text/csv")

    writer = csv.DictWriter(buffer, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return Response(content=buffer.getvalue(), media_type="text/csv")


def format_response(events: list, accept: str):
    """Return XML, CSV, or JSON depending on the Accept header.
    
    Accepts either ORM model instances or pre-serialized dicts (cache hits).
    """
    if events and isinstance(events[0], dict):
        # Already serialized (came from cache)
        serialized = events
    else:
        # ORM objects — serialize them
        serialized = [OlympicEventOut.model_validate(e).model_dump() for e in events]

    if "application/xml" in accept:
        return to_xml(serialized)
    if "text/csv" in accept:
        return to_csv(serialized)
    return serialized

from fastapi import Query

page_size = Query(
    default=20, alias='page_size', description='Items amount on page', ge=1, le=100
)

page_number = Query(
    default=1, alias='page_number', description='Page number for pagination', ge=1
)

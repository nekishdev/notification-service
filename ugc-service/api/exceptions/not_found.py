class NotFoundError(BaseException):
    def __init__(self, entity_name: str, entity_id) -> None:
        message = f"Entity [{entity_name} - {entity_id}] not found"
        super().__init__(message)

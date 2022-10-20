import uuid


class UserPermissionError(BaseException):
    def __init__(self, user_id: uuid.UUID, action: str, entity_name: str, entity_id) -> None:
        message = f"User [{user_id}] do not have permission [action: {action}, entity: {entity_name}, id: {entity_id}]"
        super().__init__(message)

class CrudError(BaseException):
    def __init__(self, action: str, entity_name: str, entity_id, error="undefined") -> None:
        message = f"CRUD operation failed [action: {action}, entity: {entity_name}, id: {entity_id}]. {error}"
        super().__init__(message)

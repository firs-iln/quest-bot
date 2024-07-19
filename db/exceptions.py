class InvalidSchemaError(Exception):
    ...


class InvalidDataError(InvalidSchemaError):
    ...


class NotFoundException(Exception):
    ...

from uuid import UUID

from fastapi_users import models, schemas


class UserSchemaReturn(schemas.BaseUser[models.ID]):
    id: UUID
    email: str


class UserSchemaAdd(schemas.BaseUserCreate):
    pass

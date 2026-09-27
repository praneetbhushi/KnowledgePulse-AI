from app.db.models.role import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):

    def __init__(self):
        super().__init__(Role)


role_repository = RoleRepository()
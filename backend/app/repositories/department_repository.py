from app.db.models.department import Department
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):

    def __init__(self):
        super().__init__(Department)


department_repository = DepartmentRepository()
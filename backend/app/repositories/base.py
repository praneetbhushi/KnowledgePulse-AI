from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic Base Repository
    Provides reusable CRUD operations for all models.
    """

    def __init__(
        self,
        model: Type[ModelType]
    ):
        self.model = model

    def get(
        self,
        db: Session,
        id: int
    ):
        return (
            db.query(self.model)
            .filter(self.model.id == id)
            .first()
        )

    def get_all(
        self,
        db: Session
    ):
        return (
            db.query(self.model)
            .all()
        )

    def create(
        self,
        db: Session,
        obj
    ):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(
        self,
        db: Session,
        id: int
    ):
        instance = self.get(db, id)

        if instance:
            db.delete(instance)
            db.commit()
        return instance
    
    def update(
    self,
    db: Session,
    db_obj,
    obj_data: dict
    ):
        for key, value in obj_data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj


    def delete(
        self,
        db: Session,
        id: int
    ):
        obj = self.get(db, id)

        if obj is None:
            return None

        db.delete(obj)
        db.commit()

        return obj
    def get_all(
    self,
    db: Session,
    skip: int = 0,
    limit: int = 100
    ):
        return (
        db.query(self.model)
        .offset(skip)
        .limit(limit)
        .all()
    )
        
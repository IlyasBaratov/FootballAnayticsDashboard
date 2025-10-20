from typing import *

from sqlalchemy.orm import Session
from sqlalchemy import select

M = TypeVar('M')

class Repository(Generic[M]):
    def __init__(self, model: Type[M]) -> None:
        self.Model:Type[M] = model

    def get(self, db: Session, id) -> M:
        return self.db.get(self.Model, id)

    def all(self, db: Session) -> List[M]:
        statement = db.query(self.Model).all()
        return list(db.execute(statement).scalars().all())

    def find(self, db: Session, **filters) -> List[M]:
        statement = select(self.Model).filter_by(**filters)
        return list(db.execute(statement).scalars().all())
        # statement = select([self.Model]).where(self.Model.id == id)
        # return list(db.execute(statement).scalars().all())
    def add(self, db: Session, obj: M) -> M:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    def addMany(self, db: Session, objs: Sequence[M]) -> Sequence[M]:
        db.add_all(list(objs))
        db.commit()
        for obj in objs:
            db.refresh(obj)
        return objs
    def delete(self, db: Session, id) -> M:
        obj = self.get(db, id)
        if obj is None:
            return None
        db.delete(obj)
        db.commit()
        return obj

    def upsert(self, db: Session, match_fields: dict, defaults: dict) -> M:
        stmt = select(self.model).filter_by(**match_fields)
        existing = db.execute(stmt).scalars().first()
        if existing:
            for k, v in defaults.items():
                setattr(existing, k, v)
            db.commit()
            db.refresh(existing)
            return existing
        obj = self.model(**match_fields, **defaults)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

"""
Generic repository pattern implementation for database operations.
"""
from typing import Generic, TypeVar, Type, List, Sequence, Optional, Any

from sqlalchemy.orm import Session
from sqlalchemy import select

M = TypeVar('M')


class Repository(Generic[M]):
    """
    Generic repository for CRUD operations.
    
    Type Parameters:
        M: SQLAlchemy model class
        
    Example:
        repo = Repository(Team)
        team = repo.get(db, team_id)
    """
    
    def __init__(self, model: Type[M]) -> None:
        self.model: Type[M] = model

    def get(self, db: Session, id: Any) -> Optional[M]:
        """Get a single record by ID."""
        return db.get(self.model, id)

    def all(self, db: Session) -> List[M]:
        """Get all records."""
        statement = select(self.model)
        return list(db.execute(statement).scalars().all())

    def find(self, db: Session, **filters) -> List[M]:
        """Find records matching filters."""
        statement = select(self.model).filter_by(**filters)
        return list(db.execute(statement).scalars().all())

    def add(self, db: Session, obj: M) -> M:
        """Add a single record."""
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def add_many(self, db: Session, objs: Sequence[M]) -> Sequence[M]:
        """Add multiple records."""
        db.add_all(list(objs))
        db.commit()
        for obj in objs:
            db.refresh(obj)
        return objs

    def delete(self, db: Session, id: Any) -> Optional[M]:
        """Delete a record by ID."""
        obj = self.get(db, id)
        if obj is None:
            return None
        db.delete(obj)
        db.commit()
        return obj

    def upsert(self, db: Session, match_fields: dict, defaults: dict) -> M:
        """
        Insert or update a record.
        
        Args:
            db: Database session
            match_fields: Fields to match for finding existing record
            defaults: Fields to update/insert
            
        Returns:
            The created or updated record
        """
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


from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from extensions import db
from models.models import User


class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_all(model, page=None, per_page=None):
    try:
        query = db.session.query(model)
        if page and per_page:
            query = query.paginate(page, per_page)
        return query.all()

    except SQLAlchemyError as error:
        raise DatabaseError(f"Error retrieving users from {model.__tablename__}: {str(error)}")


def get_user_by_id(model, user_id):
    try:
        return db.session.get(model, user_id)
    except SQLAlchemyError as error:
        raise DatabaseError(f"Error retrieving user from {model.__tablename__}: {str(error)}")


def get_user_by_email(email_id):
    try:
        return User.query.filter_by(email=email_id).first()
    except SQLAlchemyError as error:
        raise DatabaseError(
            f"Error retrieving user from {User.__tablename__}: {str(error)}")


def get_by_birthday_id(model, birthday_id, user_id):
    try:
        return db.session.query(model).filter_by(id=birthday_id, author_id=user_id).first()
    except SQLAlchemyError as error:
        raise DatabaseError(f"Error retrieving birthday record from {model.__tablename__}: {str(error)}")


def birthday_record_exists(model, birthday_id):
    try:
        return db.session.query(model).filter_by(id=birthday_id).first()
    except SQLAlchemyError as error:
        raise DatabaseError(f"Error retrieving birthday record from {model.__tablename__}: {str(error)}")


def add(entry):
    try:
        db.session.add(entry)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
    except SQLAlchemyError as error:
        db.session.rollback()
        raise DatabaseError(f"Error adding record to {entry.__tablename__}: {str(error)}")


def put():
    try:
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise DatabaseError(f"Error updating record: {str(error)}")


def delete(record):
    try:
        db.session.delete(record)
        db.session.commit()

    except SQLAlchemyError as error:
        db.session.rollback()
        raise DatabaseError(f"Error deleting record: {str(error)}")

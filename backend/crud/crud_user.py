from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, obj_in: UserCreate, is_superuser: bool = False):
    create_data = obj_in.model_dump()

    # Default username to email if not provided
    if not create_data.get("username"):
        create_data["username"] = create_data["email"]

    create_data.pop("password")
    db_user = User(**create_data)
    db_user.hashed_password = get_password_hash(obj_in.password)
    db_user.is_superuser = is_superuser

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def is_active(user: User) -> bool:
    return user.is_active


def is_superuser(user: User) -> bool:
    return user.is_superuser


class CRUDUser:
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # Create a dictionary for the database model
        db_obj_data = {
            "email": obj_in.email,
            "full_name": obj_in.full_name,
            "username": obj_in.username or obj_in.email,  # Default username to email
            "hashed_password": get_password_hash(obj_in.password),
        }

        db_obj = User(**db_obj_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> User | None:
        return db.query(User).filter(User.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser()

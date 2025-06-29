import logging

from crud import crud_user
from db.session import SessionLocal
from schemas.user import UserCreate
from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db) -> None:
    # Check if superuser exists
    user = crud_user.get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud_user.create_user(db, user=user_in, is_superuser=True)
        logger.info(f"Superuser {settings.FIRST_SUPERUSER} created.")
    else:
        logger.info(f"Superuser {settings.FIRST_SUPERUSER} already exists in database.")

def main() -> None:
    logger.info("Creating initial data...")
    db = SessionLocal()
    init_db(db)
    db.close()
    logger.info("Initial data created.")

if __name__ == "__main__":
    main() 
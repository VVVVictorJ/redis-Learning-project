import logging

from crud.crud_user import create_user, get_user_by_email
from db.session import SessionLocal
from schemas.user import UserCreate
from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db) -> None:
    # Check if superuser exists
    user = get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="Super Administrator",
        )
        user = create_user(db, obj_in=user_in, is_superuser=True)
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

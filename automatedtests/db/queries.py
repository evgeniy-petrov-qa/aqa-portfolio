from sqlalchemy.orm import Session

from automatedtests.db.models import User


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """Fetch user from DB by id."""
    return session.get(User, user_id)
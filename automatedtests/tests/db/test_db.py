import pytest
from sqlalchemy import inspect as sa_inspect

from automatedtests.db.models import User
from automatedtests.db.queries import get_user_by_id

@pytest.mark.skip
@pytest.mark.regression
def test_get_user_by_id(db_session):
    user = get_user_by_id(session=db_session, user_id=201)

    assert user is not None, "User with id=201 not found in DB"
    assert isinstance(user, User), f"Expected User object, got: {type(user)}"

    assert isinstance(user.id, int), f"id must be int, got: {type(user.id)}"
    assert user.uuid is not None, "Field uuid must not be None"
    assert isinstance(user.uuid, str) and len(user.uuid) > 0, f"uuid must be a non-empty string, got: {user.uuid!r}"

    # ORM lifecycle: object fetched from DB => persistent state
    state = sa_inspect(user)
    assert state.persistent, "Object must be in persistent state after fetching from DB"
    assert not state.detached, "Object must not be in detached state"
    assert not state.expired, "Object data must not be expired"

    # Identity map: repeated query returns same object without a SQL query
    user_cached = get_user_by_id(session=db_session, user_id=201)
    assert user is user_cached, "Identity map must return the same object, not a new one"
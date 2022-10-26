from sqlalchemy.exc import IntegrityError
from aiogram import types
from dotenv import load_dotenv
import os, logging

from utils.db_api.schemas.table_db import session, User, Contest, UsersInContests


load_dotenv()


def register_user(message: types.Message) -> bool:
    """
    Add user in DB.
    """
    username = message.from_user.username if message.from_user.username else None
    user = User(
        id=message.from_user.id,
        phone=message.contact.phone_number,
        username=username,
        name=message.from_user.full_name,
    )

    if str(user.id) in os.getenv("ADMIN_ID").split(","):
        user.admin = True

    session.add(user)

    try:
        session.commit()
        logging.info(f"{user} add in DB")
        return True
    except IntegrityError:
        session.rollback()
        logging.warning(f"{user} not add in DB")
        return False


def select_user(user_id: int) -> User:
    """
    Select simple user from DB.
    """
    user = session.query(User).filter(User.id == user_id).first()
    return user


def add_contest(data: dict) -> bool:
    """
    Add dict data in DB.
    """
    contest = Contest(
        name=data["name"],
        photo=data["photo"],
        description=data["description"],
        price=data["price"],
    )

    session.add(contest)

    try:
        session.commit()
        logging.info(f"{contest} add in DB")
        return True
    except IntegrityError:
        session.rollback()
        logging.warning(f"{contest} not add in DB")
        return False


def get_contests(contest: str = None, column: str = None) -> list:
    """
    Return list contests
    param:
    contest - simple contest
    column - column in table
    """
    where = f" WHERE name = '{contest}'" if contest else ""
    select = f"{column}" if column else "*"
    contests = session.execute(f"SELECT {select} FROM contests{where}").fetchall()
    return contests


def user_pay(data: dict) -> bool:
    """
    Add user's payment in DB.
    """
    contest = UsersInContests(
        payment_id=data["payment_id"],
        user_id=data["user_id"],
        contestname=data["contestname"],
    )

    session.add(contest)

    try:
        session.commit()
        logging.info(f"{contest} add in DB")
        return True
    except IntegrityError:
        session.rollback()
        logging.warning(f"{contest} not add in DB")
        return False


def get_user_in_contest(contest: str) -> list:
    """
    Return list of users who paid for the contest
    param:
    contest - contestname
    """
    req = f"SELECT user_id FROM users_in_contests WHERE contestname = '{contest}'"
    users = session.execute(req).fetchall()
    users = list(map(lambda user: user[0], users))
    return users


def have_payment(user_id: int, contest: str) -> list:
    """
    Returns a list definition the user has paid for the contest
    """
    contests = session.execute(
        f"SELECT * FROM users_in_contests WHERE user_id={user_id} and contestname='{contest}'"
    ).fetchall()
    return contests

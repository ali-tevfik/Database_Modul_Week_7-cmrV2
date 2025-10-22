from models.user_model import User


def get_user_by_username(db, username: str):
    user = db.query(User).filter(User.username == username).all()
    return user

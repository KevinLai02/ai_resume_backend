# crud.py
# crud.py
from sqlalchemy.orm import Session
from db.entities.User import User

# 新增一個 User
def create_user(db: Session, name: str, email: str, password: str):
    new_user = User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 根據 ID 查詢 User
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# 根據 Email 查詢 User
def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()

# 查詢所有 User
def get_all_users(db: Session):
    return db.query(User).all()

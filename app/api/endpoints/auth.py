from sqlalchemy.orm import Session
from app.cruds.user import get_user_by_email, create_new_user
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.schemas.user import UserCreate, User
from fastapi import APIRouter, Depends, HTTPException, Response
from app.core.config import settings

router = APIRouter()

@router.post('/регистрация/', response_model=User, summary='Регистрация нового пользователя')
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail='Email уже зарегистрирован')
    if "@" not in user.email:
        raise HTTPException(status_code=422, detail="Некорректный формат email")

    return create_new_user(db=db, user=user)


@router.post('/вход/', summary='Вход в систему')
def login_user(
        user: UserCreate,
        db: Session = Depends(get_db),
        response: Response = None):

    if '@' not in user.email or '.' not in user.email.split('@')[-1]:
        raise HTTPException(status_code=422, detail='Некорректный формат email')

    db_user = get_user_by_email(db, email=user.email)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Некорректный email или пароль')

    access_token = create_access_token(data={'sub': db_user.email})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        samesite='lax')

    return {
        'status': 'success',
        'message': 'Вход выполнен успешно'}

@router.post('/выход/', summary='Выход из системы')
def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "success", "message": "Выход выполнен успешно"}
# /backend/app/database/init_db.py
from sqlalchemy.orm import Session
from app.database.models import User
from app.core.security import get_password_hash, create_api_key

def create_default_users(db: Session) -> None:
    """
    Cria usuários padrão se eles não existirem
    """
    # Lista de usuários padrão
    default_users = [
        {
            "email": "admin@tenismatch.com",
            "password": "abc123",
            "is_active": True
        },
        {
            "email": "tester@tenismatch.com",
            "password": "abc123",
            "is_active": True
        }
    ]
    
    for user_data in default_users:
        # Verifica se usuário já existe
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if not user:
            # Cria novo usuário
            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                is_active=user_data["is_active"],
                api_key=create_api_key()
            )
            db.add(user)
            print(f"Usuário criado: {user_data['email']}")
    
    db.commit()
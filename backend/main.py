from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import os

from backend.database.connection import engine, get_db, Base
from backend.models.shared_models import User, Role
from backend.security.hashing import get_password_hash, verify_password
from backend.security.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.routers import sector1_victim
from backend.routers import sector2_officer
from backend.routers import sector3_threat
from backend.routers import sector4_admin
from backend.models.sector4_admin import LoginHistory

# Initialize tables (In a real app, use Alembic. For this project, we'll assume the SQL script is run manually)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cyber Crime & Threat Intelligence Platform")

app.include_router(sector1_victim.router)
app.include_router(sector2_officer.router)
app.include_router(sector3_threat.router)
app.include_router(sector4_admin.router)

@app.post("/auth/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    # Basic registration logic
    role = db.query(Role).filter(Role.role_name == user_data.get('role_name', 'Victim')).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    db_user = db.query(User).filter(User.email == user_data['email']).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = get_password_hash(user_data['password'])
    new_user = User(
        full_name=user_data['full_name'],
        email=user_data['email'],
        phone_number=user_data.get('phone_number'),
        password_hash=hashed_password,
        role_id=role.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.user_id}

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        if user:
            # Log failed login attempt
            history = LoginHistory(
                user_id=user.user_id,
                event_type="Login Failed"
            )
            db.add(history)
            db.commit()
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log successful login
    history = LoginHistory(
        user_id=user.user_id,
        event_type="Login Success"
    )
    db.add(history)
    db.commit()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.role_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.role_name}

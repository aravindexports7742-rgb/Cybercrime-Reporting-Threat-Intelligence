from fastapi import Depends, HTTPException
from backend.security.auth import get_current_user
from backend.models.shared_models import User

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role.role_name not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return True

def get_role_checker(allowed_roles):
    return RoleChecker(allowed_roles)

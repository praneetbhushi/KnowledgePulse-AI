from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
def require_admin(
    current_user=Depends(get_current_user)
):
    """
    Allow only Admin users.
    """

    if current_user.role.name != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user
def require_manager(
    current_user=Depends(get_current_user)
):
    """
    Allow Manager or Admin.
    """

    allowed_roles = [
        "Admin",
        "Manager"
    ]

    if current_user.role.name not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required"
        )

    return current_user
def require_employee(
    current_user=Depends(get_current_user)
):
    return current_user
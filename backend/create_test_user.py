from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.department import Department
from app.core.security import get_password_hash


db = SessionLocal()

try:
    # Find Admin role
    admin_role = db.query(Role).filter(Role.name == "Admin").first()

    if admin_role is None:
        print("ERROR: Admin role not found.")
        print("Available roles:")
        for role in db.query(Role).all():
            print(role.id, role.name)
        raise SystemExit

    # Find an existing department
    department = db.query(Department).first()

    if department is None:
        print("ERROR: No department found.")
        raise SystemExit

    email = "admin@test.com"
    password = "Admin@123"

    # Check whether user already exists
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        print("Test user already exists.")
        print("User ID:", existing_user.id)
        print("Email:", existing_user.email)
        print("Role:", existing_user.role.name)
    else:
        user = User(
            name="Test Admin",
            email=email,
            password=get_password_hash(password),
            department_id=department.id,
            role_id=admin_role.id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print("Test Admin created successfully!")
        print("User ID:", user.id)
        print("Email:", email)
        print("Password:", password)
        print("Role:", admin_role.name)

finally:
    db.close()
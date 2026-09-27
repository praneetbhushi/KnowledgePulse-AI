from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.services.user_service import user_service


def create_test_users():
    db = SessionLocal()

    try:
        users = [
            UserCreate(
                name="Test Manager",
                email="manager@test.com",
                password="Manager@123",
                department_id=1,
                role_id=2,
            ),
            UserCreate(
                name="Test Employee",
                email="employee@test.com",
                password="Employee@123",
                department_id=1,
                role_id=3,
            ),
        ]

        for user_data in users:
            try:
                user = user_service.create_user(
                    db,
                    user_data
                )

                print(
                    f"Created: {user.email} "
                    f"(ID={user.id}, role_id={user.role_id})"
                )

            except Exception as e:
                print(
                    f"Skipped {user_data.email}: {e}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    create_test_users()
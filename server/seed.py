from app import app, db
from models import User, Loan
from datetime import datetime

def seed_database():
    with app.app_context():
        print("Sedding the database...")
        User.query.delete()
        Loan.query.delete()


        users=[
            User(
                first_name="Cheryl",
                last_name="Mbani",
                email="cherylmbani@gmail.com",
                #phone_number="0711111111",
                password="password123"
            ),
            User(
                first_name="Roynald",
                last_name="Roynald",
                email="roynald@gmail.com",
                #phone_number="0722222222",
                password='password123'

            ),
            User(
                first_name="Tonny",
                last_name="Ramo",
                email="Tonyramo@gmail.com",
                #phone_number="0733333333",
                password='password123'
            ),
            User(
                first_name="Amayo",
                last_name="Nandy",
                email="amayonandy@gmail.com",
                #phone_number="0744444444",
                password="password123"
            )
        ]
        db.session.add_all(users)
        db.session.commit()

        loans=[
            Loan(
                amount=1000,
                loan_type="secured",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                application_status="PENDING",
                reason="I want to attend school",
                user_id=1
            ),
            Loan(
                amount=2000,
                loan_type="secured",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                application_status="APPROVED",
                reason="I want to do farming",
                user_id=2
            ),
            Loan(
                amount=3000,
                loan_type="unsecured",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                application_status="REJECTED",
                reason="To pay another pending loan",
                user_id=3

            ),
            Loan(
                loan_type="secured",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                application_status="REJECTED",
                reason="To pay for hospital bills",
                user_id=2

            )

        ]
        db.session.add_all(loans)
        db.session.commit()
        print("Seeded successfully!")

if __name__=="__main__":
    seed_database()
 



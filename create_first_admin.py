import getpass
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

def main():
    print("--- Create First Admin User ---")
    db: Session = SessionLocal()
    
    username = input("Enter username: ")
    
    # Check if user already exists
    if crud.get_admin_by_username(db, username):
        print(f"Admin with username '{username}' already exists. Aborting.")
        return
        
    password = getpass.getpass("Enter password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    
    if password != password_confirm:
        print("Passwords do not match. Aborting.")
        return
        
    admin_in = schemas.AdminCreate(username=username, password=password)
    admin = crud.create_admin(db, admin_in)
    
    print(f"Successfully created admin user: {admin.username}")
    db.close()

if __name__ == "__main__":
    main()
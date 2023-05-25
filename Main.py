from User.login_system import UserLoginSystem
from Database.SQL import EasySql

if __name__ == "__main__":
    db = EasySql()
    login_system = UserLoginSystem(db)
    login_system.run()

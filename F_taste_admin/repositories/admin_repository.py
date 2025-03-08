from F_taste_admin.utils.credentials import admin_id, admin_password

class AdminRepository:
    @staticmethod
    def get_admin_credentials():
        return admin_id, admin_password
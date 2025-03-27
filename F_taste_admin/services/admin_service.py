from F_taste_admin.repositories.admin_repository import AdminRepository
from F_taste_admin.utils.jwt_token_factory import JWTTokenFactory

#import di kafka
from F_taste_admin.kafka.kafka_producer import send_kafka_message
from F_taste_admin.utils.kafka_helpers import wait_for_kafka_response
######

jwt_factory = JWTTokenFactory()




class AdminService:
    
    
    @staticmethod
    def login_admin(s_admin):
        if "id_admin" not in s_admin or "password" not in s_admin:
            return {"esito_login":"Dati mancanti"}, 400
        id_admin=s_admin["id_admin"]
        password=s_admin["password"]
        stored_id, stored_password = AdminRepository.get_admin_credentials()
        if id_admin == stored_id and password == stored_password:
            return {
                "esito": "successo",
                "access_token": jwt_factory.create_access_token(id_admin, 'admin'),
                "refresh_token": jwt_factory.create_refresh_token(id_admin, 'admin')
            }, 200
        return {"esito": "credenziali errate"}, 401
    
    
    @staticmethod
    def delete_paziente(s_admin):
        id_paziente=s_admin['id_paziente']
        if not id_paziente:  # Controllo valore vuoto o assente
            return {"message": "ID paziente richiesto"}, 400  # HTTP 400 Bad Request
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.delete.request",message)
        response=wait_for_kafka_response(["patient.delete.success", "patient.delete.failed"])
        return response
    
    
    @staticmethod
    def delete_nutrizionista(s_admin):
        email=s_admin['email']
        if not email:  # Controllo valore vuoto o assente
            return {"message": "email nutrizionista richiesta"}, 400  # HTTP 400 Bad Request
        message={"email":email}
        send_kafka_message("dietitian.delete.request",message)
        response=wait_for_kafka_response(["dietitian.delete.success", "dietitian.delete.failed"])
        return response
    
    
    @staticmethod
    def get_pazienti():
        message = {}  # Non ci sono parametri, quindi il messaggio può essere vuoto 
        send_kafka_message("patient.getAll.request", message)
        response = wait_for_kafka_response(["patient.getAll.success", "patient.getAll.failed"])
        return response
    
    
    @staticmethod
    def get_nutrizionisti():
        message = {}  # Non ci sono parametri, quindi il messaggio può essere vuoto 
        send_kafka_message("dietitian.getAll.request", message)
        response = wait_for_kafka_response(["dietitian.getAll.success", "dietitian.getAll.failed"])
        return response
    
    
    

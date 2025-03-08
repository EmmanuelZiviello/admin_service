from flask import request
from flask_restx import Resource, fields
from F_taste_admin.namespaces import admin_ns
from F_taste_admin.limiter_config import limiter
from F_taste_admin.services.admin_service import AdminService
from F_taste_admin.utils.jwt_custom_decorators import admin_required


paziente_to_delete = admin_ns.model('paziente_to_delete', {
    'id_paziente': fields.String('id paziente')
})


class AdminPaziente(Resource):

    @admin_required()
    @admin_ns.expect(paziente_to_delete)
    @admin_ns.doc('elimina paziente')
    def delete(self):
        patient_json = request.get_json()
        return AdminService.delete_paziente(patient_json)
    
class Pazienti(Resource):
 
    @admin_required()
    @admin_ns.doc('ricevi tutti i pazienti')
    def get(self):
        return AdminService.get_pazienti()
    



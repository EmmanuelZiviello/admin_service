from flask import request
from flask_restx import Resource, fields
from F_taste_admin.namespaces import admin_ns
from F_taste_admin.limiter_config import limiter
from F_taste_admin.services.admin_service import AdminService
from F_taste_admin.utils.jwt_custom_decorators import admin_required


nutrizionista_delete_model = admin_ns.model('nutrizionista_to_delete', {
    'email': fields.String('email del nutrizionista'),
})


class AdminNutrizionista(Resource):

    @admin_required()
    @admin_ns.expect(nutrizionista_delete_model)
    @admin_ns.doc('elimina nutrizionista')
    def delete(self):
        dietitian_json = request.get_json()
        return AdminService.delete_nutrizionista(dietitian_json)
    
class Nutrizionisti(Resource):
 
    @admin_required()
    @admin_ns.doc('ricevi tutti i nutrizionisti')
    def get(self):
        return AdminService.get_nutrizionisti()
    


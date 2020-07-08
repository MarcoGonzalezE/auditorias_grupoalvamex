from odoo import api, fields, models 
from datetime import datetime 

class AuditoriaPlantillas(models.Model):
	_name = 'auditoria.plantilla'

	name = fields.Char(string="Nombre")
	seccion_ids = fields.Many2many('auditoria.plantilla.secciones', string="Secciones")


class AuditoriaPlantillaSecciones(models.Model):
	_name = 'auditoria.plantilla.secciones'
	_order = 'sequence'

	name = fields.Char(string="Nombre de Seccion")
	puntos = fields.Integer(string="Puntos")
	conceptos_ids = fields.One2many('auditoria.plantilla.conceptos', 'seccion_id', string="Conceptos")
	sequence = fields.Integer(string='Sequence', default=10)

	@api.multi
	def abrir_seccion(self):
		form_id = self.env.ref('auditorias_grupoalvamex.auditoria_plantillas_secciones_view_form')
		return{
            'type':'ir.actions.act_window',
            'name':'Seccion',
            'res_model':'auditoria.plantilla.secciones',
            'res_id': self.id,
            'view_mode':'form',
            'view_type':'form',
            'view_id': form_id.id,
            'contex':{},
            'target':'current',
        }


class AuditoriaConceptos(models.Model):
	_name = 'auditoria.plantilla.conceptos'

	name = fields.Char(string="Concepto")
	seccion_id = fields.Many2one('auditoria.plantilla.secciones', string="Seccion ID")
	sequence = fields.Integer(string='Sequence', default=10)


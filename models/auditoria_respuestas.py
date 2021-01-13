from odoo import api, fields, models 

class PreguntaRespuesta(models.Model):
	_name = 'auditoria.pregunta.respuesta'

	auditoria_id = fields.Many2one('auditoria.supervision', string="Auditoria ID")
	concepto = fields.Char(string="Concepto")
	#evaluacion = fields.Selection([('aprobado','Aprobado'),('proceso','Proceso'),('no_cumple','No Cumple')], string="Evaluacion")
	observaciones = fields.Char(string="Observaciones")
	tipo = fields.Selection([('concepto','Concepto'),('seccion','Seccion')], string="Tipo de Linea")
	numero = fields.Integer(string="No")
	resultado = fields.Integer(string="Resultado")

	aprobado = fields.Boolean(string="Aprobado")
	proceso = fields.Boolean(string="Proceso")
	no_cumple = fields.Boolean(string="No Cumple")

	def boton_aprobado(self):
		if self.aprobado == True:
			self.aprobado = False
			self.resultado = 0
		else:
			self.aprobado = True
			self.resultado = 5

		self.proceso = False
		self.no_cumple = False

	def boton_proceso(self):
		if self.proceso == True:
			self.proceso = False
			self.resultado = 0
		else:
			self.proceso = True
			self.resultado = 3

		self.aprobado = False
		self.no_cumple = False

	def boton_nocumple(self):
		if self.no_cumple == True:
			self.no_cumple = False
		else:
			self.no_cumple = True
		self.aprobado = False
		self.proceso = False
		self.resultado = 0
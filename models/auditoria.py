from odoo import api, fields, models 
from datetime import datetime 

class AuditoriaPosturas(models.Model):
	_name = 'auditoria.supervision'

	name = fields.Char(string="Nombre")
	area = fields.Char(string="Area")
	seccion = fields.Char(string="Seccion")
	verifico = fields.Char(string="Verifico")
	auditado = fields.Char(string="Auditado")
	fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now)
	concepto_ids = fields.One2many('auditoria.pregunta.respuesta', 'auditoria_id', string="Conceptos")
	plantilla_id = fields.Many2one('auditoria.plantilla', string="Plantilla")
	puntaje_maximo = fields.Integer(string="Puntaje Maximo")
	puntaje_obtenido = fields.Integer(string="Puntaje Obtenido")
	numero_auditoria = fields.Char(string="Auditoria")
	estado = fields.Selection([('linea','En Linea'),('finalizada','Finalizada')], string="Estado", default='linea')
	calificacion = fields.Integer(string="Calificacion")
	#Firmas
	firma_auditado = fields.Binary(string="Firma Auditado")
	firma_verifico = fields.Binary(string="Firma Verifico")
	firma_gerencia = fields.Binary(string="Firma Gerencia")

	@api.model
	def create(self, vals):
		if vals.get('numero_auditoria','Nuevo') == 'Nuevo':
			vals['numero_auditoria'] = self.env['ir.sequence'].next_by_code('auditoria.supervision') or "Nuevo"
		return  super(AuditoriaPosturas, self).create(vals)


	@api.multi
	@api.onchange('plantilla_id')
	def _cargar_plantilla(self):
		self.name = self.plantilla_id.name
		plantilla = self.env['auditoria.plantilla'].search([('id','=',self.plantilla_id.id)])
		seccion = self.env['auditoria.plantilla.secciones']
		p_ids = []
		num = 0
		for p in plantilla.seccion_ids:
			seccion = self.env['auditoria.plantilla.secciones'].search([('id','=',p.id)])
			p_ids.append((0,0,{'concepto':seccion.name,'tipo':'seccion','aprobado':True,'proceso':True,'no_cumple':True}))
			for s in seccion.conceptos_ids:
				concepto = self.env['auditoria.plantilla.conceptos'].search([('id','=', s.id),('tipo','in',(plantilla.tipo.id,1))],order="sequence asc")
				for c in concepto:
					num += 1
					p_ids.append((0,0,{'concepto':c.name,'tipo':'concepto','numero':num}))
			self.puntaje_maximo = num * 5

		self.concepto_ids = p_ids
		self.puntaje_obtenido = 0
		self.calificacion = 0

	# def obtener_resultados(self):
	# 	for c in self.concepto_ids:
	# 		a = 0
	# 		p = 0
	# 		resultados = 0
	# 		secciones = self.env['auditoria.plantilla.secciones'].search([('name','=',c.concepto)])
	# 		for s in secciones.conceptos_ids:
	# 			conceptos = self.env['auditoria.pregunta.respuesta'].search([('concepto','=',s.name)])
	# 			print(conceptos)
	# 			for r in conceptos:
	# 				resultados += r.resultado
	# 		print(resultados)
		# 		secciones.update({'resultado':resultado})
		# return secciones

	def obtener_resultados(self):
		respuestas = self.env['auditoria.pregunta.respuesta'].search([('auditoria_id','=',self.id),('tipo','=','seccion')])
		total = 0
		validos = 0
		cal = 0
		for r in respuestas:
			secciones = self.env['auditoria.plantilla.secciones'].search([('name','=',r.concepto)])
			suma = 0
			for s in secciones.conceptos_ids:
				conceptos = self.env['auditoria.pregunta.respuesta'].search([('concepto','=',s.name),('auditoria_id','=',self.id)])
				for c in conceptos:
					suma = c.resultado + suma
					if c.no_cumple == False and c.aprobado == False and c.proceso == False:
						c.observaciones = 'No Aplica'
					else:
						validos += 1
						if c.observaciones == 'No Aplica':
							c.observaciones = ''
				r.resultado = suma
			total = r.resultado + total
		self.puntaje_obtenido = total
		self.puntaje_maximo = validos * 5
		cal = float(self.puntaje_obtenido)/float(self.puntaje_maximo)
		self.calificacion = cal * 100

	@api.multi
	def imprimir_auditoria(self):
		return self.env['report'].get_action(self, 'auditorias_grupoalvamex.auditoria_reporte_document')

	def final(self):
		self.estado = 'finalizada'


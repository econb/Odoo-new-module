# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class Idea(models.Model):
    _name = 'ideas.idea'
    nombre = fields.Char(string="Nombre")
    grupo = fields.Integer(string="Grupo")
    descripcion = fields.Text(string="Descripción")
    fecha_ini = fields.Datetime(string="Fecha inicio")
    fecha_fin = fields.Datetime(string="Fecha límite", compute="_fun_fecha", readonly=True)
    votos = fields.One2many(string="Votos", comodel_name='ideas.voto', inverse_name='idea_id', readonly=True)
    calificacion = fields.Float(string="Calificación", compute="_fun_calificacion", readonly=True, store=False)
    
    @api.depends('fecha_ini')
    def _fun_fecha(self):
        fecha_ini_copy = fields.Datetime.from_string(self.fecha_ini)
        if fecha_ini_copy is not None:
            one_month_later = fecha_ini_copy + timedelta(weeks=4)
            self.fecha_fin = fields.Datetime.to_string(one_month_later)
            
    @api.depends('votos')
    def _fun_calificacion(self): 
        if len(self.votos) > 0:
            avg = sum(voto_id.calificacion for voto_id in self.votos) / len(self.votos)
            self.calificacion = avg
            

class Voto(models.Model):
    _name = 'ideas.voto'
    calificacion = fields.Float(string="Calificación", digits=(3,1))
    fecha = fields.Datetime(string="Fecha voto", default=fields.Datetime.now(), readonly=True) 
    idea_id = fields.Many2one(string="Selección", comodel_name='ideas.idea', required=True, ondelete='cascade')
    usuario = fields.Many2one(string="Usuario", comodel_name="res.users")
    
    #Fields of idea
    idea_descripcion = fields.Text(related="idea_id.descripcion", string="Idea", store=False, readonly=True)
    idea_fecha_ini = fields.Datetime(related='idea_id.fecha_ini', string="Inicio votaciones", store=False, readonly=True)
    idea_fecha_fin = fields.Datetime(related='idea_id.fecha_fin', string="Fin votaciones", store=False, readonly=True)
    
    @api.constrains('calificacion')
    def _check_calificacion(self):
        if self.calificacion < 0 or self.calificacion > 10:
            raise exceptions.ValidationError("La calificación debe ser entre 0 y 10.")
            
    @api.constrains('idea_id')
    def _check_fecha_idea(self):
        lim_inf = fields.Datetime.from_string(self.idea_fecha_ini)
        lim_sup = fields.Datetime.from_string(self.idea_fecha_fin)
        actual = fields.Datetime.from_string(self.fecha)
        if actual < lim_inf or actual > lim_sup:
            error_message = "Las votaciones para esta idea se deben realizar entre las fechas " + self.idea_fecha_ini + " y " + self.idea_fecha_fin
            raise exceptions.ValidationError(error_message)
         
class Grupo(models.Model):
    _name = 'ideas.grupo'   
    nombre = fields.Char(string="Nombre")
    personas = fields.Many2many(string="Personas", comodel_name='res.users')

#REFERENCES
#http://odoo-new-api-guide-line.readthedocs.io/en/latest/fields.html
#https://www.odoo.com/documentation/10.0/reference/orm.html
#https://www.odoo.com/documentation/10.0/howtos/backend.html

# class ideas(models.Model):
#     _name = 'ideas.ideas'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
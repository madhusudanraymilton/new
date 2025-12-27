from odoo import models, fields

class CliRecord(models.Model):
    _name = 'cli.record'
    _description = 'CLI Record'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Price', required=True)
    available = fields.Boolean(string='Available', default=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft', required=True, tracking=True)
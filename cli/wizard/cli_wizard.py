from odoo import models, fields

class CliWizard(models.TransientModel):
    _name = 'cli.wizard'
    _description = 'CLI Wizard'

    message = fields.Text(string='Message', readonly=True, default='Are you sure you want to proceed?')
    record_id = fields.Many2one('cli.record', string='Record')

    def action_confirm(self):
        return self.env.ref('cli.action_report_cli_record').report_action(self.record_id)

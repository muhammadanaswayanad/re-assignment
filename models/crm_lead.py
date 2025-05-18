from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_open_reassign_wizard(self):
        """Open the reassignment wizard."""
        self.ensure_one()
        
        # Create wizard as a form
        return {
            'name': _('Reassign Lead'),
            'type': 'ir.actions.act_window',
            'res_model': 'lead.reassignment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_lead_id': self.id,
            }
        }

class LeadReassignmentWizard(models.TransientModel):
    _name = 'lead.reassignment.wizard'
    _description = 'Lead Reassignment Wizard'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=True, readonly=True)
    new_user_id = fields.Many2one('res.users', string='New Salesperson', 
                                  domain=[('share', '=', False)], required=True)

    def action_request_reassignment(self):
        """Request a lead reassignment that will be processed by the scheduler."""
        self.ensure_one()
        
        # Create reassignment request
        self.env['lead.reassignment'].create({
            'lead_id': self.lead_id.id,
            'new_user_id': self.new_user_id.id,
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Reassignment request submitted. It will be processed shortly.'),
                'type': 'success',
                'sticky': False,
            }
        }

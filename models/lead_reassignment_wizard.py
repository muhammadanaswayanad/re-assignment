from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class LeadReassignmentWizard(models.TransientModel):
    _name = 'lead.reassignment.wizard'
    _description = 'Lead Reassignment Wizard'

    lead_id = fields.Many2one(
        'crm.lead', 
        string='Lead', 
        required=True
    )
    new_user_id = fields.Many2one(
        'res.users', 
        string='New Salesperson', 
        domain=[('share', '=', False)],  # Only internal users
        required=True
    )
    
    def action_reassign(self):
        """Reassign the lead to another salesperson using sudo()."""
        self.ensure_one()
        
        try:
            # Perform reassignment with sudo to bypass security
            lead = self.env['crm.lead'].sudo().browse(self.lead_id.id)
            if not lead.exists():
                raise ValidationError(_("The lead does not exist."))
            
            # Store old user for the message
            old_user_id = lead.user_id
            
            # Update the lead's salesperson
            lead.write({'user_id': self.new_user_id.id})
            
            # Log the change in the chatter
            message = _(
                "Lead reassigned from %s to %s by %s"
            ) % (
                old_user_id.name if old_user_id else _("Unassigned"),
                self.new_user_id.name,
                self.env.user.name
            )
            lead.sudo().message_post(body=message)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Success"),
                    'message': _("Lead successfully reassigned to %s") % self.new_user_id.name,
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Error"),
                    'message': str(e),
                    'type': 'danger',
                    'sticky': False,
                }
            }

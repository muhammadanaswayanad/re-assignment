from odoo import api, fields, models, _
from odoo.exceptions import AccessError

class LeadReassignment(models.Model):
    _name = 'lead.reassignment'
    _description = 'Lead Reassignment Request'
    _rec_name = 'lead_id'
    _order = 'create_date desc'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=True, ondelete='cascade')
    new_user_id = fields.Many2one('res.users', string='New Salesperson', required=True)
    requested_by = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('failed', 'Failed')
    ], string='Status', default='pending')
    notes = fields.Text(string='Notes')

    def process_reassignments(self):
        """Process all pending lead reassignments."""
        pending = self.search([('state', '=', 'pending')])
        for record in pending:
            try:
                lead = self.env['crm.lead'].sudo().browse(record.lead_id.id)
                if lead.exists():
                    old_user = lead.user_id
                    lead.write({'user_id': record.new_user_id.id})
                    
                    # Log the change in chatter
                    message = _(
                        "Lead reassigned from %s to %s by %s"
                    ) % (
                        old_user.name if old_user else _("Unassigned"),
                        record.new_user_id.name,
                        record.requested_by.name
                    )
                    lead.sudo().message_post(body=message)
                    
                    record.write({
                        'state': 'done',
                        'notes': _('Reassignment completed on %s') % fields.Datetime.now()
                    })
                else:
                    record.write({
                        'state': 'failed',
                        'notes': _('Lead no longer exists')
                    })
            except Exception as e:
                record.write({
                    'state': 'failed',
                    'notes': _('Error: %s') % str(e)
                })
        return True

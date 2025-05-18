from odoo import api, fields, models


class CrmLeadReassign(models.TransientModel):
    _name = 'crm.lead.reassign.wizard'
    _description = 'Reassign Lead to Another Salesperson'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=True)
    user_id = fields.Many2one('res.users', string='Salesperson', required=True,
                              domain=[('share', '=', False)])

    @api.model
    def default_get(self, fields):
        res = super(CrmLeadReassign, self).default_get(fields)
        if self.env.context.get('active_model') == 'crm.lead' and self.env.context.get('active_id'):
            res['lead_id'] = self.env.context.get('active_id')
        return res
    
    def action_reassign(self):
        self.ensure_one()
        # Using sudo() to bypass access restrictions as specified in requirements
        self.lead_id.sudo().write({
            'user_id': self.user_id.id
        })
        return {'type': 'ir.actions.act_window_close'}

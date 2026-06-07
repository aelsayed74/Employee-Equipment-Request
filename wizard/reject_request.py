from odoo import fields, models
from odoo.exceptions import ValidationError
class RejectRequest(models.TransientModel):
    _name="reject.request"
    request_id = fields.Many2one("employee.equipment.request")
    reason = fields.Char(required=True)
    
    def action_confirm(self):
        self.ensure_one()
        if not self.reason or not self.reason.strip():
            raise ValidationError(" You must write the rejection reason")
        self.request_id.write({
            'state': 'rejected',
            'rejection_reason': self.reason
        })
        return {'type': 'ir.actions.act_window_close'}
    
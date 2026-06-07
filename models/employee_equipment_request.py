from odoo import models , fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
class EmployeeEquipmentRequest(models.Model):
    _name = 'employee.equipment.request'
    _rec_name = 'ref'
    _inherit=["mail.thread","mail.activity.mixin"]
    _description = 'Employee Equipment Request'
    employee_name = fields.Char(required=True, size = 30, tracking=True)
    equipment_type = fields.Selection([
        ('computer','Computer'),
        ('phone','Phone'),
        ('screen','Screen')
    ],required=True, tracking=True)
    created_at = fields.Datetime(required=True, tracking=True)
    description = fields.Text(tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',required=True)
    rejection_reason = fields.Text(string='Rejection Reason', tracking=True)
    is_late = fields.Boolean()
    state = fields.Selection([
    ('draft','Draft'),
    ('submitted','Submitted'),
    ('approved','Approved'),
    ('rejected','Rejected'),
    ('done','Done'),
    ],required=True, string='Status', default='draft', group_expand='_read_group_states', tracking=True)
    # This is to cancel the alphabetical order of the executions in the Kanban view
    @api.model
    def _read_group_states(self, stages, domain, order):
        return ['draft', 'submitted', 'approved', 'rejected', 'done']
    
    # Refrence 
    ref = fields.Char(readonly=True, default='New')
    @api.model_create_multi
    def create(self, vals):
        res = super(EmployeeEquipmentRequest, self).create(vals)
        if res.ref =='New':
            res.ref = self.env['ir.sequence'].next_by_code('equipment_sequence')
        return res
    @api.constrains('created_at')
    def _check_created_at_date(self):
        for record in self:
            if record.created_at:
                current_date = fields.Datetime.now().date()
                record_date = record.created_at.date()
                if record_date < current_date:
                    raise ValidationError("The order creation date cannot be in the past! Please select a valid date")
    
        
    @api.constrains('employee_id', 'employee_name', 'equipment_type', 'state')
    def _check_duplicate_request(self):
        for record in self:
            if record.state in ['draft', 'submitted', 'approved']:
                domain = [
                    ('equipment_type', '=', record.equipment_type),
                    ('state', 'in', ['draft', 'submitted', 'approved'])
                ]
                if record.id:
                    domain.append(('id', '!=', record.id))
                if record.employee_id:
                    domain.append(('employee_id', '=', record.employee_id.id))
                elif record.employee_name:
                    domain.append(('employee_name', '=ilike', record.employee_name.strip()))
                else:
                    continue
                duplicate_exists = self.search(domain, limit=1)
                if duplicate_exists:
                    raise ValidationError(_(
                        "Sorry, this employee already has an existing order for the same type of device being processed (Draft/Submitted/Approved)!"))
    def action_draft(self):
        for rec in self:
            rec.state="draft"
    def action_submitted(self):
        for rec in self:
            rec.state="submitted"
    def action_approved(self):
        for rec in self:
            rec.state="approved"
    def action_rejected(self):
        self.ensure_one()
        return {
            'name': 'Write the rejection reason',
            'type': 'ir.actions.act_window',    
            'res_model': 'reject.request',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_request_id': self.id,
            }
        }
    def action_done(self):
        for rec in self:
            rec.state="done"
            
    def action_send_pending_requests_reminder(self):
        all_requests = self.search([])
        
        if not all_requests:
            return  
            
        for rec in all_requests:
            if rec.state == 'submitted':
                rec.is_late = True
                message_body = _(
                    "⚠️ Pending Request Reminder!\n\n"
                    "The request number %s for employee (%s) to request a device (%s) "
                    "is still awaiting review and approval."
                ) % (rec.ref or '', rec.employee_name or '', rec.equipment_type or '')
                rec.message_post(
                    body=message_body,
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment'
                )
            else:
                rec.is_late = False
                
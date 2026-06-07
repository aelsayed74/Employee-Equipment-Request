from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit='hr.employee'
    equipment_request_count = fields.Integer(compute='_compute_equipment_request_count', string="Equipment Requests Count")
    
    
    @api.depends('equipment_request_count')
    def _compute_equipment_request_count(self):
        for rec in self:
            request_count = self.env['employee.equipment.request'].search_count([
                ('employee_id', '=', rec.id)])
            rec.equipment_request_count = request_count
            
    def action_view_equipment_requests(self):
        self.ensure_one()
        return {
            'name': 'Equipment Requests',
            'type': 'ir.actions.act_window',
            'res_model': 'employee.equipment.request', # اسم موديل طلبات المعدات الخاص بك
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)], # فلترة الطلبات لتخص هذا الموظف فقط
            'context': {'default_employee_id': self.id}, # لجعل الموظف الحالي مختاراً تلقائياً عند إنشاء طلب جديد
        }
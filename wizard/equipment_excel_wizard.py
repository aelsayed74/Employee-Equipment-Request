import base64
import io
from odoo import models, fields, api
from odoo.exceptions import UserError
import xlsxwriter

class EquipmentExcelWizard(models.TransientModel):
    _name = 'equipment.excel.wizard'
    _description = 'Equipment Report Excel Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    employee_id = fields.Many2one('hr.employee', string='Employee')

    def action_generate_excel(self):
        self.ensure_one()
        
        # 1. بناء دالة الفلترة الديناميكية بناءً على مدخلات المستخدم
        domain = []
        if self.date_from:
            domain.append(('created_at', '>=', self.date_from))
        if self.date_to:
            domain.append(('created_at', '<=', self.date_to))
        if self.employee_id:
            domain.append(('employee_id', '=', self.employee_id.id))

        # جلب البيانات المفلترة من الموديل الرئيسي
        requests = self.env['employee.equipment.request'].search(domain)
        
        if not requests:
            raise UserError("No records found matching the selected filters!")

        # 2. تجهيز ملف الإكسيل في الذاكرة المؤقتة (In-Memory Buffer)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Equipment Requests')

        # 3. تصميم التنسيقات (Styles)
        # تنسيق العنوان الرئيسي
        title_format = workbook.add_format({
            'bold': True, 'font_size': 16, 'align': 'center', 
            'bg_color': '#1F4E79', 'font_color': 'white', 'border': 1
        })
        # تنسيق الهيدر للجدول
        header_format = workbook.add_format({
            'bold': True, 'font_size': 11, 'align': 'center', 
            'bg_color': '#D9E1F2', 'font_color': '#1F4E79', 'border': 1
        })
        # تنسيق البيانات العادية
        data_format = workbook.add_format({'font_size': 10, 'align': 'left', 'border': 1})
        # تنسيق التواريخ
        date_format = workbook.add_format({'font_size': 10, 'align': 'center', 'num_format': 'yyyy-mm-dd', 'border': 1})

        # 4. كتابة البيانات داخل الشيت
        # دمج الخلايا للعنوان الرئيسي
        worksheet.merge_range('A1:F1', 'Equipment Requests Report', title_format)
        worksheet.set_row(0, 30) # ضبط ارتفاع صف العنوان

        # عناوين الأعمدة
        headers = ['Reference', 'Employee Name', 'Equipment Type', 'Created At', 'State', 'Description']
        for col_num, header_title in enumerate(headers):
            worksheet.write(2, col_num, header_title, header_format)
        worksheet.set_row(2, 20)

        # كتابة صفوف البيانات من قاعدة البيانات
        row_num = 3
        for req in requests:
            worksheet.write(row_num, 0, req.ref or '', data_format)
            worksheet.write(row_num, 1, req.employee_id.name or req.employee_name or '', data_format)
            worksheet.write(row_num, 2, req.equipment_type or '', data_format)
            
            # معالجة التاريخ والوقت ليظهر بشكل نقي في إكسيل
            if req.created_at:
                worksheet.write_datetime(row_num, 3, req.created_at, date_format)
            else:
                worksheet.write(row_num, 3, '', data_format)
                
            worksheet.write(row_num, 4, (req.state or '').capitalize(), data_format)
            worksheet.write(row_num, 5, req.description or '', data_format)
            row_num += 1

        # ضبط عرض الأعمدة تلقائياً لتناسب النصوص
        worksheet.set_column('A:F', 20)

        # إغلاق وحفظ الملف في الذاكرة
        workbook.close()
        output.seek(0)

        # 5. تشفير الملف وتحويله إلى أودو لتبدأ عملية التحميل التلقائي
        file_data = base64.b64encode(output.read())
        output.close()

        # إنشاء مرفق مؤقت (Attachment)
        attachment = self.env['ir.attachment'].create({
            'name': 'Equipment_Requests_Report.xlsx',
            'type': 'binary',
            'datas': file_data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        # إرجاع أكشن التحميل المباشر المتوافق مع متصفحات Odoo 17
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
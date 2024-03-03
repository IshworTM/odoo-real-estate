from odoo import fields, models, api

class StudentManagement(models.Model):
    _name = "student.management"
    _description = "Student management system for schools."

    name = fields.Char(
        required=True,
        string="Name"
    )

    age = fields.Integer(
        required=True,
        string="Age",
        default="10"
    )

    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('others', 'Others'),
            ('not_specified', 'Not specified'),
        ],
        required=True,
        string="Gender"
    )

    roll_no = fields.Integer(
        required=True,
        string="Roll. No",
        default=0
    )

    math = fields.Integer(
        required=True,
        string="Maths"
    )   
    science = fields.Integer(
        required=True,
        string="Science"
    )    
    english = fields.Integer(
        required=True,
        string="English"
    )    
    nepali = fields.Integer(
        required=True,
        string="Nepali"
    )

    opt_subject_ids = fields.Many2many(
        "student.optional.subjects",
        required=True,
        string="Optional Subjects"
    )
from odoo import fields, models

class StudentOptionalSubjects(models.Model):
    _name = "student.optional.subjects"
    _description = "Optional Subjects"

    name = fields.Char(
        string="Subject Name",
        required=True
    )

    marks = fields.Integer(
        string="Marks",
        required=True
    )

    teacher = fields.Char(
        string="Teacher",
        required=True
    )
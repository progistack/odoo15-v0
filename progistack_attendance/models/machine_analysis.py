# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    device_id = fields.Char(string="ID biométrique de l'employé")
    heur_travail_jour = fields.Float(string="Heurs de Travail par Jours")
    heur_arrive = fields.Float(string ="Heure d'arrivée")
    heur_depart = fields.Float(string="Heure de départ")
    heur_arrive_tard = fields.Selection([('15', '15 munites'), ('30', '30 munites'), ('45', '45 munites'),
                                         ('1', '1 heure')], default='15')
    employee_absence_id = fields.One2many('employee.absence', 'employee_id', string="Employee Absence")
    make_invisible = fields.Boolean(string="Masquer label")
    heur_debut_pose = fields.Float(string="Heure de Début de Pause")
    heur_fin_pose = fields.Float(string="Heure de Fin de Pause")
    heur_de_travail = fields.Float(string="Nombre d'heure de travail par jour")
    weekend_day = fields.Many2many('week.day', 'employee_day_help', 'employee_id', 'day_id', string='Jours de travail')

class HrAbsence(models.Model):
    _name = 'hr.absence'

    employee_id = fields.Many2one('hr.employee', string='Employé')
    date_absence = fields.Date(string='Date')
    heur_perdu = fields.Float(string="Heure perdue")

class HrEmployeeAbsence(models.Model):
    _name = 'employee.absence'

    motif_absence = fields.Selection([('maladie', 'Maladie'), ('conge', 'Congé'), ('autre', 'Autre')], string="Motif de l'absence")
    date_debut_absence = fields.Date(string="Date de début", require=True)
    date_fin_absence = fields.Date(string="Date de fin", require=True)
    employee_id = fields.Many2one('hr.employee', ondelete='cascade', string="Employee")

class HrAnalyse(models.Model):
    _name = 'hr.analyse'
    employee_id = fields.Many2one('hr.employee', ondelete='cascade', string="Employee")
    heur_de_travail = fields.Float(string='Heure de travail')


class WeekDay(models.Model):
    _name = "week.day"

    name = fields.Char(string="nom du jour")

class ZkMachine(models.Model):
    _name = 'zk.machine.attendance'
    _inherit = 'hr.attendance'

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """overriding the __check_validity function for employee attendance."""
        pass

    device_id = fields.Char(string="ID de l'appareil biométrique")
    punch_type = fields.Selection([('0', 'Entrée'),
                                   ('1', 'Sortie'),
                                   ('2', 'Pause'),
                                   ('3', 'Reprise pause'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out'),
                                   ('201', 'success'),
                                   ('255', 'error')
                                   ],
                                  string='Punching Type')

    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2','Type_2'),
                                        ('3','Password'),
                                        ('4','Card')], string='Category')
    punching_time = fields.Datetime(string='Punching Time')
    address_id = fields.Many2one('res.partner', string='Adresse de travail')


class ReportZkDevice(models.Model):
    _name = 'zk.report.daily.attendance'
    _auto = False
    _order = 'punching_day desc'

    name = fields.Many2one('hr.employee', string='Employee')
    punching_day = fields.Datetime(string='Date')
    address_id = fields.Many2one('res.partner', string='Adresse de travail')
    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2','Type_2'),
                                        ('3','Password'),
                                        ('4','Card')],
                                       string='Catégorie')
    punch_type = fields.Selection([('0', 'Entrée'),
                                   ('1', 'Sortie'),
                                   ('2', 'Pause'),
                                   ('3', 'Reprise pause'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out'),
                                   ('201', 'success'),
                                   ('255', 'error')], string='Type de Pointage')
    punching_time = fields.Datetime(string='Temps de Pointage')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'zk_report_daily_attendance')
        query = """
            create or replace view zk_report_daily_attendance as (
                select
                    min(z.id) as id,
                    z.employee_id as name,
                    z.write_date as punching_day,
                    z.address_id as address_id,
                    z.attendance_type as attendance_type,
                    z.punching_time as punching_time,
                    z.punch_type as punch_type
                from zk_machine_attendance z
                    join hr_employee e on (z.employee_id=e.id)
                GROUP BY
                    z.employee_id,
                    z.write_date,
                    z.address_id,
                    z.attendance_type,
                    z.punch_type,
                    z.punching_time
            )
        """
        self._cr.execute(query)



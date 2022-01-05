# -*- coding: utf-8 -*-

import datetime
import logging
from struct import unpack

import pytz

from odoo import _
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from .zkconst import *

_logger = logging.getLogger(__name__)
try:
    from zk import ZK, const
except ImportError:
    _logger.error("Veuillez installer la bibliothèque pyzk.")

_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    device_id = fields.Char(string="ID biométrique de l'employé")
    absence_non_prevu = fields.Date(string="Absence")
    heur_planifie = fields.Float(string="Arrivée planifiée")
    heur_sup_jour = fields.Float(string="Heurs Supplementaire")
    heur_depart = fields.Float(string="Départ planifié")
    pointge_oublie = fields.Boolean(string="Pointage oublié")
    status = fields.Selection([('retard', 'Retard'), ('pile', "A l'heure")], string=" Statut")
    worked_hour = fields.Float(string="heures travaillées")
    date_pointage=fields.Date(string="Date")
    heure_entre = fields.Float(string="arrivée réelle")
    heure_sortie = fields.Float(string="Départ réel")
    visible = fields.Boolean(string="Visible")

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        raise UserError(_("Vous essayez de changer l'employé."))

    @api.depends('heure_entre', 'heure_sortie')
    def _compute_worked_hours(self):
        print("----------------------depends")
        for attendance in self:
            if attendance.heure_entre and attendance.heure_sortie:
                delta = attendance.heure_sortie - attendance.heure_entre
                #attendance.worked_hour = (delta.total_seconds() / 3600.0) - 2
                attendance.worked_hour = delta - 2
                attendance.heur_sup_jour = attendance.worked_hour - 8
            else:
                attendance.worked_hour = False
                attendance.heur_sup_jour = False

    def get_total_hours(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'name': _('Modifications de la date de sortie'),
            'res_model': 'hr.attendance',
        }
        action['view_id'] = self.env.ref('progistack_attendance.view_modifie_date').id

        return action


class ZkMachine(models.Model):
    _name = 'zk.machine'

    name = fields.Char(string='Machine IP', required=True)
    port_no = fields.Integer(string='No Port', required=True)
    address_id = fields.Many2one('res.partner', string='Adresse de travail')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)

    def device_connect(self, zk):
        try:
            conn = zk.connect()
            return conn
        except:
            return False

    def clear_attendance(self):
        for info in self:
            print('self ---', self)
            try:
                machine_ip = info.name
                zk_port = info.port_no
                timeout = 30
                try:
                    zk = ZK(machine_ip, port=zk_port, timeout=timeout, password=0, force_udp=False, ommit_ping=False)
                except NameError:
                    raise UserError(_("Absence de librairie Veuillez l'installer avec 'pip3 install pyzk'."))
                conn = self.device_connect(zk)
                if conn:
                    conn.enable_device()
                    clear_data = zk.get_attendance()
                    print("---------- clear clear", clear_data)
                    if clear_data:
                        # conn.clear_attendance()
                        print("---------- clear clear1", clear_data)
                        self._cr.execute("""delete from zk_machine_attendance""")
                        conn.disconnect()
                        raise UserError(_('Enregistrements de présence supprimés.'))
                    else:
                        raise UserError(
                            _("Impossible d'effacer le journal de présence. Êtes-vous sûr que le journal de présence n'est pas vide."))
                else:
                    raise UserError(
                        _('Impossible de se connecter au périphérique de présence. Veuillez utiliser le bouton Tester la connexion pour vérifier.'))
            except:
                raise ValidationError(
                    "Impossible d'effacer le journal de présence. Êtes-vous sûr que le dispositif de présence est connecté et que l'enregistrement n'est pas vide.")

    def getSizeUser(self, zk):
        """Checks a returned packet to see if it returned CMD_PREPARE_DATA,
        indicating that data packets are to be sent

        Returns the amount of bytes that are going to be sent"""
        command = unpack('HHHH', zk.data_recv[:8])[0]
        if command == CMD_PREPARE_DATA:
            size = unpack('I', zk.data_recv[8:12])[0]
            print("size", size)
            return size
        else:
            return False

    def zkgetuser(self, zk):
        """Start a connection with the time clock"""
        try:
            users = zk.get_users()
            print(users)
            return users
        except:
            return False

    @api.model
    def cron_download(self):
        machines = self.env['zk.machine'].search([])
        for machine in machines:
            machine.download_attendance()

    def download_attendance(self):
        _logger.info("++++++++++++Cron Executed++++++++++++++++++++++")
        zk_attendance = self.env['zk.machine.attendance']
        att_obj = self.env['hr.attendance']
        user_ids = []
        all_employee_ids = []
        absence_aut_ids = []
        absence_ids = []
        employee_pointe_id = []

        today_time = datetime.today().strftime('%Y-%m-%d')
        today_heur = datetime.today().hour + datetime.today().minute / 60

        for info in self:
            machine_ip = info.name
            zk_port = info.port_no
            timeout = 15
            try:
                zk = ZK(machine_ip, port=zk_port, timeout=timeout, password=0, force_udp=False, ommit_ping=False)
            except NameError:
                raise UserError(_("Module Pyzk introuvable. Veuillez l'installer avec 'pip3 install pyzk'."))
            conn = self.device_connect(zk)
            print("-----------------", conn)
            if conn:
                # conn.disable_device() #Device Cannot be used during this time.
                try:
                    user = conn.get_users()
                    print('*********user---------------------', user)
                except:
                    user = False
                print("***************----------------1")
                try:
                    print("***************----------------2")
                    attendance = conn.get_attendance()
                    print("***************----------------", attendance)
                    for each in attendance:
                        pointage_time = each.timestamp.strftime('%Y-%m-%d')
                        if pointage_time == today_time:
                            user_ids.append(each.user_id)
                    print("all ----------ids ---", user_ids)
                    all_employee = self.env['hr.employee'].search([])
                    all_absence_aut = self.env['employee.absence'].search([])
                    all_absence = self.env['hr.absence'].search([])
                    for ep in all_employee:
                        all_employee_ids.append(ep.id)
                    print("all ids employee", all_employee_ids)
                    for ab_aut in all_absence_aut:
                        absence_aut_ids.append(ab_aut.id)
                    for abs in all_absence:
                        absence_ids.append(abs.id)
                except:
                    attendance = False
                if attendance:
                    for each in attendance:
                        print('------------punch', each.punch)
                        print('************ddffddff', each.user_id)
                        atten_time = each.timestamp
                        atten_time = datetime.strptime(atten_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(
                            self.env.user.partner_id.tz or 'GMT')
                        local_dt = local_tz.localize(atten_time, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        atten_time = datetime.strptime(
                            utc_dt, "%Y-%m-%d %H:%M:%S")
                        atten_time = fields.Datetime.to_string(atten_time)
                        pointage_date = each.timestamp.strftime('%Y-%m-%d')
                        pointage_heur = each.timestamp.hour + each.timestamp.minute / 60
                        if user:
                            for uid in user:
                                print("----ids----------",(pointage_heur))

                                print("------- dodod ------", datetime.today().strftime('%Y-%m-%d'))
                                if uid.user_id == each.user_id and pointage_date == today_time:
                                    get_user_id = self.env['hr.employee'].search(
                                        [('device_id', '=', each.user_id)])
                                    nmbre_user_id = user_ids.count(each.user_id)
                                    get_user_id = self.env['hr.employee'].search(
                                        [('device_id', '=', each.user_id)])[-1]
                                    print("******* get_user_id", get_user_id.id)
                                    print("-----------", get_user_id.heur_arrive)
                                    if get_user_id:
                                        duplicate_atten_ids = zk_attendance.search(
                                            [('device_id', '=', each.user_id), ('punching_time', '=', atten_time)])
                                        print("duplicate ----", duplicate_atten_ids)
                                        if get_user_id.id not in employee_pointe_id:
                                            employee_pointe_id.append(get_user_id.id)
                                        if str(each.punch) == '255':
                                            pass
                                        else:
                                            # fait pareil pour les autre heurs

                                            att_var = att_obj.search([('employee_id', '=', get_user_id.id),
                                                                      ('date_pointage', '=', False)])
                                            print("date de pointage",att_var)
                                            if not duplicate_atten_ids:
                                                if nmbre_user_id == 1:
                                                    print("yetststs")

                                                    zk_attendance.create({'employee_id': get_user_id.id,
                                                                          'device_id': each.user_id,
                                                                          'attendance_type': str(each.status),
                                                                          'punch_type': '0',
                                                                          'punching_time': atten_time,
                                                                          'address_id': info.address_id.id})
                                                    if not att_var:
                                                        print("ttttttttttttttttttttttttttttt")
                                                        att_var.create({'employee_id': get_user_id.id,
                                                                        'check_in': atten_time,
                                                                        'heur_planifie': get_user_id.heur_arrive,
                                                                        'heur_depart': get_user_id.heur_depart,
                                                                        'heure_entre': pointage_heur,
                                                                        'visible': False,
                                                                        'date_pointage': pointage_date})


                                                else:
                                                    att_var = att_obj.search([('employee_id', '=', get_user_id.id)])
                                                    zk_attendance.create({'employee_id': get_user_id.id,
                                                                          'device_id': each.user_id,
                                                                          'attendance_type': str(each.status),
                                                                          'punch_type': '0',
                                                                          'punching_time': atten_time,
                                                                          'address_id': info.address_id.id})
                                                    print("nous somme ici", att_var)
                                                    if att_var:
                                                        att_var[-1].write({'check_out': atten_time, 'heure_sortie': pointage_heur})

                                            """ 
                                            else:

                                                employee_line.write({'check_out': atten_time})

                                                zk_attendance.create({'employee_id': get_user_id.id,
                                                                      'device_id': each.user_id,
                                                                      'attendance_type': str(each.status),
                                                                      'punch_type': '0',
                                                                      'punching_time': atten_time,
                                                                      'address_id': info.address_id.id})
                                            """

                            else:
                                pass
                    for val in all_employee_ids:
                        if val not in employee_pointe_id:
                            if val not in absence_aut_ids:
                                absence = self.env['hr.absence']
                                duplicate_absence = absence.search(
                                    [('employee_id', '=', val), ('date_absence', '=', today_time)])
                                if not duplicate_absence:
                                    absence.create({
                                        'employee_id': val,
                                        'date_absence': today_time,
                                        'heur_perdu': -8
                                    })
                        else:
                            self.env['hr.absence'].search(
                                [('employee_id', '=', val), ('date_absence', '=', today_time)]).unlink()

                    for i in employee_pointe_id:

                        nbre_ocurence = employee_pointe_id.count(i)
                        if nbre_ocurence == 1:
                            print("--------", i)
                            user_ocu = self.env['hr.attendance'].search([('employee_id', '=', i)])[-1]
                            if user_ocu.heur_depart + 0.5 < today_heur and user_ocu.visible == False:
                                print("okokokokkooko")
                                user_ocu.write({'visible': True, 'heure_sortie': user_ocu.heur_depart})
                # zk.enableDevice()
                conn.disconnect
                return True
            else:
                raise UserError(_("Impossible d'obtenir le journal des présences, veuillez réessayer plus tard."))
        else:
            raise UserError(_('Connexion impossible, veuillez vérifier les paramètres et les connexions réseau.'))

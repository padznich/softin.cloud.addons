# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################
from openerp import models, fields, api

#List of Project Sections
class ProjectSectionList(models.Model):
    _name = 'project.section.list'
    _description = 'List of Project Sections'
    _order = 'sequence'
    _rec_name = 'short_name'

    long_name = fields.Char(string='Long Name', required=True, size=200)
    short_name = fields.Char(string='Short Name', required=True, size=50)
    sequence = fields.Integer('Sequence')

#Project Sections for Project Module
class ProjectSection(models.Model):
    _name = 'project.section'
    _description = 'Project Sections'
    _rec_name = 'project_linesection_id'

    project_section_id = fields.Many2one('project.section.list',
                                          string='Section', ondelete='restrict',
                                          index=True, relation='data_section_rel', required=True)
    project_section_line_id = fields.Many2one('project.project', string='Project Reference',
                                              index=True, required=True, ondelete='cascade')
    #monetary field, wage-rate/ставка
    currency_id = fields.Many2one('res.currency', string='Currency')
    wage_rate = fields.Monetary('Wage-rate',
                                currency_field='currency_id',
                                help="Cost of this project section")
    #Laboriousness/трудозатраты
    labor = fields.Float(digits=(6, 2), string="Laboriousness", help="Laboriousness of this project section")

    #Плановая стоимость (Computed fields)
    planned_cost = fields.Float(string="Planned Cost", compute='_taken_cost')

    @api.depends('wage_rate', 'labor')
    def _taken_cost(self):
        for record in self:
            record.planned_cost = record.wage_rate * record.labor


class ProjectProject(models.Model):
    _inherit = 'project.project'

    section_line = fields.One2many('project.section', 'project_section_line_id', string='Section Lines', copy=True)

    #Подсчет полных трудозатрат и стоимости
    @api.depends('section_line')
    def _amount_all(self):
        for project in self:
            amount_total_cost = amount_total_labor = 0.0
            #
            for section in project.section_line:
                amount_total_cost += section.planned_cost
                amount_total_labor += section.labor

            project.update({
                'amount_total_labor': project.currency_id.round(amount_total_labor),
                'amount_total_cost': project.currency_id.round(amount_total_cost),
            })

    amount_total_labor = fields.Monetary(string='Total Laboriousness', store=True,
                                      readonly=True, compute='_amount_all')

    amount_total_cost = fields.Monetary(string='Total Planned Cost', store=True,
                                      readonly=True, compute='_amount_all')

#Add Project Section by Project Tasks
class SectionByTask(models.Model):
    _inherit = 'project.task'

    section_id = fields.Many2one('project.section', string='Section')

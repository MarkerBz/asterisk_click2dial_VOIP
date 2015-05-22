# -*- encoding: utf-8 -*-
from openerp.osv import orm, fields
from openerp.tools.translate import _


class number_not_found(orm.TransientModel):
    _inherit = "number.not.found"
    
    _columns = {
        'new_applicant_name': fields.char('New Applicant Name', size=128),
        
        'to_update_applicant_id': fields.many2one(
            'hr.applicant', 'Applicant to Update',
            #domain=[('type', '=', 'applicant')],
            help="Applicant on which the phone number will be written"),
        'current_applicant_phone': fields.related(
            'to_update_applicant_id', 'partner_phone', type='char',
            relation='hr.applicant', string='Current Phone', readonly=True),
        'current_applicant_mobile': fields.related(
            'to_update_applicant_id', 'partner_mobile', type='char',
            relation='hr.applicant', string='Current Mobile', readonly=True),
        }
    
    def create_applicant(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wiz = self.browse(cr, uid, ids[0], context=context)
        
        if (not wiz.new_applicant_name) or (wiz.new_applicant_name.replace(' ', '') == ''):
            raise orm.except_orm(_('Error:'), _("Set New Applicant Name!"))
        
        _new_partner = self.pool.get('res.partner').create(cr, uid, {
            'name' : wiz.new_applicant_name,
            wiz.number_type : wiz.e164_number,
        })
        
        _new_applic = self.pool.get('hr.applicant').create(cr, uid, {
            'name' : wiz.new_applicant_name,
            'partner_id' : _new_partner,
            'partner_%s' % wiz.number_type : wiz.e164_number,
        })
        
        action = {
            'name'      : _('New Applicant'),
            'type'      : 'ir.actions.act_window',
            'res_model' : 'hr.applicant',
            'res_id'    : _new_applic,
            #'view_type': 'form',
            #'view_mode': 'kanban,tree,form,graph,calendar',
            'view_mode' : 'form,kanban,tree,graph,calendar',
            'target'    : 'current',
            'nodestroy' : False,
        }
        
        return action
    
    def update_applicant(self, cr, uid, ids, context=None):
        wiz = self.browse(cr, uid, ids[0], context=context)
        if not wiz.to_update_applicant_id:
            raise orm.except_orm(
                _('Error:'),
                _("Select the Applicant to Update!"))
        
        if wiz.to_update_applicant_id.partner_id:
            self.pool['res.partner'].write(
                cr, uid, wiz.to_update_applicant_id.partner_id.id,
                {wiz.number_type: wiz.e164_number}, context=context)
        
        self.pool['hr.applicant'].write(
            cr, uid, wiz.to_update_applicant_id.id,
            {'partner_%s' % wiz.number_type: wiz.e164_number}, context=context)
        
        action = {
            'name'      : _('Applicant: %s' % wiz.to_update_applicant_id.name),
            'type'      : 'ir.actions.act_window',
            'res_model' : 'hr.applicant',
            'res_id'    : wiz.to_update_applicant_id.id,
            'view_mode' : 'form,kanban,tree,graph,calendar',
            #'view_id'   : False,
            #'view_type' : 'form',
            'target'    : 'current',
            'nodestroy' : False,
        }
        return action
    
    def onchange_to_update_applicant(
            self, cr, uid, ids, to_update_applicant_id, context=None):
        res = {'value': {}}
        if to_update_applicant_id:
            to_update_applicant = self.pool['hr.applicant'].browse(
                cr, uid, to_update_applicant_id, context=context)
            res['value'].update({
                'current_applicant_phone': to_update_applicant.partner_phone,
                'current_applicant_mobile': to_update_applicant.partner_mobile,
                })
        else:
            res['value'].update({
                'current_applicant_phone': False,
                'current_applicant_mobile': False,
                })
        return res

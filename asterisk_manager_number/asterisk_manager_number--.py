# -*- encoding: utf-8 -*-
from openerp.osv import orm


class phone_common(orm.AbstractModel):
    
    _inherit = 'phone.common'
    
    def get_name_from_phone_number(
            self, cr, uid, presented_number, context=None):
        '''Function to get name from phone number. Usefull for use from IPBX
        to add CallerID name to incoming calls.'''
        res = self.get_record_from_phone_number(
            cr, uid, presented_number, context=context)
        if res:
            
            #//+++++++++++++++++++++
            #res[0] = 'res.partner'     res[1] = 8
            obj = self.pool.get(res[0]).browse(cr, uid, [res[1]], context=context)[0]
            managers_number = ''
            try:
                if obj.user_id:
                    managers_number = obj.user_id.internal_number
            except:
                pass
            return '%s", "%s' % (res[2], managers_number)
            
            #return res[2]
            
        else:
            return False


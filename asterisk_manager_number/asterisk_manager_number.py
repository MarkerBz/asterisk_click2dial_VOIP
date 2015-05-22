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
            
            #//!!!!!!!!!!!!!!!!!!!!
            depart_managers_numbers = ''
            try:
                if obj.section_id:
                    users_pool = self.pool.get('res.users')
                    cr.execute('''
                        SELECT
                            member_id
                        FROM
                            sale_member_rel
                        WHERE
                            section_id = %s
                        ''', (obj.section_id.id,)
                    )
                    for manager_id in cr.fetchall():
                        user_obj = users_pool.browse(cr, uid, [manager_id[0]], context=context)[0]
                        if user_obj.internal_number:
                            depart_managers_numbers = '%s;%s' % (depart_managers_numbers, user_obj.internal_number)
            except:
                pass
            return '%s;%s%s' % (res[2], managers_number, depart_managers_numbers)
            
            #return res[2]
            
        else:
            return False


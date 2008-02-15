from trytond.osv import fields, OSV
STATES = {'readonly': "active == False",}

class Category(OSV):
    "Partner Category"

    _name = "partner.category"
    _description = __doc__
    _order = 'parent,name'
    _parent_name = 'parent'

    def name_get(self, cursor, user, ids, context=None):

        if not len(ids):
            return []
        categories = self.browse(cursor, user, ids, context=context)
        res = []
        for category in categories:
            if category.parent:
                name = category.parent.name+' / '+ category.name
            else:
                name = category.name
            res.append((category.id, name))
        return res

    def _name_get_fnc(self, cursor, user, obj_id, name, value, arg,
            context=None):
        res = self.name_get(cursor, user, ids, context)
        return dict(res)

    def check_recursion(self, cursor, user, ids, parent=None):
        return super(Category, self).check_recursion(cursor, user,
            ids,parent="parent")

    _columns = {
        'name': fields.Char('Category Name', required=True, size=64,
                states= STATES,),
        'parent': fields.Many2One('partner.category', 'Parent Category',
                select=True, states= STATES,),
        'complete_name': fields.Function(_name_get_fnc, method=True,
                type="char", string='Name', states= STATES,),
        'childs': fields.One2Many('partner.category', 'parent',
            'Childs Category', states= STATES,),
        'active' : fields.Boolean('Active'),
    }

    _defaults = {
        'active' : lambda *a: 1,
    }

    _constraints = [
        (check_recursion,
         'Error ! You can not create recursive categories.', ['parent'])
    ]

Category()

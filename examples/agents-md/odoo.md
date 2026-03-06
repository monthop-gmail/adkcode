# AGENTS.md — Odoo ERP

## Stack
- Odoo 17 Community / Enterprise
- Python 3.10+
- PostgreSQL
- OWL (Odoo Web Library) สำหรับ frontend
- Docker Compose สำหรับ development

## Rules
- ตอบเป็นภาษาไทยเสมอ
- ทำตาม Odoo coding guidelines อย่างเคร่งครัด
- ห้ามแก้ core module โดยตรง — สร้าง custom module inherit เสมอ
- Model name ใช้ dot notation: `my_module.my_model`
- Security: ต้องมี `ir.model.access.csv` และ `record rules` ทุก model
- ทดสอบด้วย `odoo-bin -d testdb -u my_module --test-enable`

## Module Structure
```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   ├── my_model_views.xml
│   └── menu_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── data/
│   └── default_data.xml
├── wizard/
│   ├── __init__.py
│   └── my_wizard.py
├── report/
│   ├── my_report.xml
│   └── my_report_template.xml
├── static/
│   └── src/
│       ├── js/
│       ├── xml/
│       └── scss/
└── i18n/
    └── th.po
```

## __manifest__.py Template
```python
{
    'name': 'ชื่อ Module ภาษาไทย',
    'version': '17.0.1.0.0',
    'category': 'Custom',
    'summary': 'สรุปสั้นๆ ว่า module ทำอะไร',
    'author': 'My Company',
    'website': 'https://mycompany.com',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/my_model_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

## Model Conventions
```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MyModel(models.Model):
    _name = 'my_module.my_model'
    _description = 'คำอธิบาย Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # tracking
    _order = 'create_date desc'

    name = fields.Char(string='ชื่อ', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'ร่าง'),
        ('confirmed', 'ยืนยัน'),
        ('done', 'เสร็จสิ้น'),
        ('cancelled', 'ยกเลิก'),
    ], string='สถานะ', default='draft', tracking=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    # Compute field
    total = fields.Float(compute='_compute_total', store=True)

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total = sum(rec.line_ids.mapped('subtotal'))

    # Constraint
    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if len(rec.name) < 3:
                raise ValidationError(_('ชื่อต้องมีอย่างน้อย 3 ตัวอักษร'))

    # State transitions
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
```

## View XML Conventions
```xml
<!-- Tree View -->
<record id="my_model_view_tree" model="ir.ui.view">
    <field name="name">my.model.tree</field>
    <field name="model">my_module.my_model</field>
    <field name="arch" type="xml">
        <tree>
            <field name="name"/>
            <field name="state" widget="badge"
                   decoration-success="state == 'done'"
                   decoration-info="state == 'confirmed'"
                   decoration-danger="state == 'cancelled'"/>
        </tree>
    </field>
</record>

<!-- Form View -->
<record id="my_model_view_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my_module.my_model</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <button name="action_confirm" type="object"
                        string="ยืนยัน" class="btn-primary"
                        invisible="state != 'draft'"/>
                <button name="action_cancel" type="object"
                        string="ยกเลิก"
                        invisible="state in ('done', 'cancelled')"/>
                <field name="state" widget="statusbar"
                       statusbar_visible="draft,confirmed,done"/>
            </header>
            <sheet>
                <group>
                    <group>
                        <field name="name"/>
                    </group>
                    <group>
                        <field name="company_id"/>
                    </group>
                </group>
                <notebook>
                    <page string="รายละเอียด">
                        <field name="line_ids">
                            <tree editable="bottom">
                                <field name="product_id"/>
                                <field name="quantity"/>
                                <field name="price"/>
                                <field name="subtotal"/>
                            </tree>
                        </field>
                    </page>
                </notebook>
            </sheet>
            <div class="oe_chatter">
                <field name="message_follower_ids"/>
                <field name="activity_ids"/>
                <field name="message_ids"/>
            </div>
        </form>
    </field>
</record>
```

## Security (ir.model.access.csv)
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_module_my_model,base.group_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_module_my_model,base.group_system,1,1,1,1
```

## Inheritance Patterns
```python
# เพิ่ม field ใน model เดิม
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char(string='ฟิลด์เพิ่มเติม')

# เพิ่มปุ่มใน view เดิม
<record id="sale_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="custom_field"/>
        </xpath>
    </field>
</record>
```

## Common Tasks
- สร้าง custom module ใหม่
- Inherit model/view ที่มีอยู่
- สร้าง report (QWeb PDF)
- สร้าง wizard (Transient Model)
- สร้าง scheduled action (ir.cron)
- Migrate module ข้าม version
- สร้าง REST API endpoint (controller)

## Docker Development
```yaml
# docker-compose.yml
services:
  odoo:
    image: odoo:17
    ports:
      - "8069:8069"
    volumes:
      - ./custom_addons:/mnt/extra-addons
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_DB=postgres
```

## Commands
- Install module: `odoo-bin -d mydb -i my_module`
- Update module: `odoo-bin -d mydb -u my_module`
- Run tests: `odoo-bin -d testdb -u my_module --test-enable --stop-after-init`
- Scaffold: `odoo-bin scaffold my_module ./custom_addons`
- Shell: `odoo-bin shell -d mydb`

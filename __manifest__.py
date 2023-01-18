# -*- coding: utf-8 -*-
{
    'name': "Synchronous Integration",

    'summary': """
       User for sync data from e-commercer platform to Odoo
    """,

    'description': """
        Long description of module's purpose for sync data from e-commercer platform to Odoo
    """,

    'author': "Blue Pheasant",
    'website': "https://github.com/Blue-Pheasant",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sync',
    'version': '0.1',
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "base_rest",
        "base_rest_datamodel",
        "base_rest_pydantic",
        "component",
        "extendable",
    ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/products.xml',
        'wizard/accept_sync_product.xml',
    ],
    
    # only loaded in demonstration mode
    "external_dependencies": {
        "python": ["jsondiff", "extendable-pydantic", "pydantic"]
    }    
}

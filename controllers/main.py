# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import format_amount
from odoo.addons.sale.controllers.variant import VariantController

_logger = logging.getLogger("COntrolador :::::::")


class PosController(VariantController):
    @http.route(['/sale/get_combination_info'], type='json', auth="user", methods=['POST'])
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        combination = request.env['product.template.attribute.value'].browse(combination)
        pricelist = self._get_pricelist(pricelist_id)
        cids = request.httprequest.cookies.get('cids', str(request.env.user.company_id.id))
        allowed_company_ids = [int(cid) for cid in cids.split(',')]
        ProductTemplate = request.env['product.template'].with_context(allowed_company_ids=allowed_company_ids)
        if 'context' in kw:
            ProductTemplate = ProductTemplate.with_context(**kw.get('context'))
        if kw.get("alto") and kw.get("ancho"):
            ProductTemplate = ProductTemplate.with_context(medidas=True,alto=int(kw.get("alto")),ancho=int(kw.get("ancho")))
        product_template = ProductTemplate.browse(int(product_template_id))
        res = product_template._get_combination_info(combination, int(product_id or 0), int(add_qty or 1), pricelist)
        if 'parent_combination' in kw:
            parent_combination = request.env['product.template.attribute.value'].browse(kw.get('parent_combination'))
            if not combination.exists() and product_id:
                product = request.env['product.product'].browse(int(product_id))
                if product.exists():
                    combination = product.product_template_attribute_value_ids
            res.update({
                'is_combination_possible': product_template._is_combination_possible(combination=combination,
                                                                                     parent_combination=parent_combination),
                'parent_exclusions': product_template._get_parent_attribute_exclusions(
                    parent_combination=parent_combination)
            })
        return res

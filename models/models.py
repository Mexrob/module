# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api

_logger = logging.getLogger("Modelo :::::::")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    alto = fields.Integer("Alto")
    ancho = fields.Integer("Ancho")
    medidas = fields.Char("Medidas", compute="format_medidas")

    def format_medidas(self):
        for l in self:
            l.medidas = "%d x %d mm" % (l.alto, l.ancho)

    @api.depends('alto','ancho')
    def _compute_price_unit(self):
        super()._compute_price_unit()

    def _get_display_price(self):
        price = super(SaleOrderLine,self)._get_display_price()
        if self.alto and self.ancho:
            price = price * self.alto * self.ancho
        return price


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)
        if self.env.context.get('medidas'):
            alto = self.env.context.get('alto', 0)
            ancho = self.env.context.get('ancho', 0)
            combination_info['list_price'] = combination_info['list_price'] * alto * ancho
            combination_info['price'] = combination_info['price'] * alto * ancho
        return combination_info


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_find_product_line(self, product_id, line_id=None, **kwargs):
        lines = super(SaleOrder, self)._cart_find_product_line(product_id, line_id=line_id, **kwargs)
        if kwargs.get("alto") and kwargs.get("ancho"):
            lines = lines.filtered(lambda l: l.alto == int(kwargs.get("alto")) and l.ancho == int(kwargs.get("ancho")))
        return lines

    def _prepare_order_line_values(
            self, product_id, quantity, linked_line_id=False,
            no_variant_attribute_values=None, product_custom_attribute_values=None,
            **kwargs
    ):
        values = super(SaleOrder, self)._prepare_order_line_values(product_id, quantity,
                                                                   linked_line_id=linked_line_id,
                                                                   no_variant_attribute_values=no_variant_attribute_values,
                                                                   product_custom_attribute_values=product_custom_attribute_values,
                                                                   **kwargs)
        values['alto'] = kwargs.get("alto",0)
        values['ancho'] = kwargs.get("ancho",0)
        return values

    @api.model
    def actualizar_plantilla(self):
        pass
        template = self.env.ref("sale.mail_template_sale_confirmation")
        template.template_fs = "website_custom/views/views.xml"
        template.reset_template()
        _logger.warning("actualizando plantilla")
        self.env.cr.commit()
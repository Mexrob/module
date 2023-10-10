odoo.define('website_custom.product_m', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    require('website_sale.website_sale');
    var VariantMixin = require('website_sale.VariantMixin');

    publicWidget.registry.WebsiteSale.include({
        init: function () {
            this._super.apply(this, arguments);
            this.events = _.extend(this.events, {
                "change input[id=alto]": "onchange_medida",
                "change input[id=ancho]": "onchange_medida",
            });
        },
        onchange_medida: function (ev) {
            let alto = $('input[id="alto"]').val();
            let ancho = $('input[id="ancho"]').val();
            if (alto > 0 && ancho > 0) {
                return VariantMixin.onChangeVariant.apply(this, arguments);
            }
        },
        _getOptionalCombinationInfoParam($product) {
            let alto = $('input[id="alto"]').val();
            let ancho = $('input[id="ancho"]').val();
            return {alto: alto, ancho: ancho};
        },
        _submitForm: function () {
            const params = this.rootProduct;

            const $product = $('#product_detail');
            const productTrackingInfo = $product.data('product-tracking-info');
            if (productTrackingInfo) {
                productTrackingInfo.quantity = params.quantity;
                $product.trigger('add_to_cart_event', [productTrackingInfo]);
            }
            params.alto = $('input[id=alto]').val();
            params.ancho = $('input[id=ancho]').val();
            params.add_qty = params.quantity;
            params.product_custom_attribute_values = JSON.stringify(params.product_custom_attribute_values);
            params.no_variant_attribute_values = JSON.stringify(params.no_variant_attribute_values);
            delete params.quantity;
            return this.addToCart(params);
        },
        _onChangeCombination: function (ev, $parent, combination) {
            var self = this;
            var $price = $parent.find(".oe_price:first .oe_currency_value");
            var $default_price = $parent.find(".oe_default_price:first .oe_currency_value");
            var $optional_price = $parent.find(".oe_optional:first .oe_currency_value");
            let val = combination.price >1 ? combination.price: 0;
            $price.text(self._priceToStr(val));
            $default_price.text(self._priceToStr(combination.list_price));

            var isCombinationPossible = true;
            if (!_.isUndefined(combination.is_combination_possible)) {
                isCombinationPossible = combination.is_combination_possible;
            }
            this._toggleDisable($parent, isCombinationPossible);

            if (combination.has_discounted_price) {
                $default_price
                    .closest('.oe_website_sale')
                    .addClass("discount");
                $optional_price
                    .closest('.oe_optional')
                    .removeClass('d-none')
                    .css('text-decoration', 'line-through');
                $default_price.parent().removeClass('d-none');
            } else {
                $default_price
                    .closest('.oe_website_sale')
                    .removeClass("discount");
                $optional_price.closest('.oe_optional').addClass('d-none');
                $default_price.parent().addClass('d-none');
            }

            var rootComponentSelectors = [
                'tr.js_product',
                '.oe_website_sale',
                '.o_product_configurator'
            ];

            // update images only when changing product
            // or when either ids are 'false', meaning dynamic products.
            // Dynamic products don't have images BUT they may have invalid
            // combinations that need to disable the image.
            if (!combination.product_id ||
                !this.last_product_id ||
                combination.product_id !== this.last_product_id) {
                this.last_product_id = combination.product_id;
                self._updateProductImage(
                    $parent.closest(rootComponentSelectors.join(', ')),
                    combination.display_image,
                    combination.product_id,
                    combination.product_template_id,
                    combination.carousel,
                    isCombinationPossible
                );
            }

            $parent
                .find('.product_id')
                .first()
                .val(combination.product_id || 0)
                .trigger('change');

            $parent
                .find('.product_display_name')
                .first()
                .text(combination.display_name);

            $parent
                .find('.js_raw_price')
                .first()
                .text(combination.price)
                .trigger('change');

            this.handleCustomValues($(ev.target));
        },

    });

});
   
    
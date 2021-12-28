odoo.define('fidelite.QuotationOrder',function(require){
    'use strict';

     const SaleOrderManagementControlPanel = require('pos_sale.SaleOrderManagementControlPanel');
     const Registries = require('point_of_sale.Registries');
     const { useListener } = require('web.custom_hooks');

     const QuotationOrder = SaleOrderManagementControlPanel =>
            class extends SaleOrderManagementControlPanel{
                constructor() {
                    super(...arguments);
                    useListener('close-screen', this.add_point);
                }

                add_point(){
                     const userInfo = this.env.pos.get_client();
                     if(userInfo){
                         let alltotal = 0
                         const existLoyalty = userInfo.loyalty ;
                         alltotal = this.env.pos.get_order().get_subtotal();
                         const total =  Math.round(alltotal + existLoyalty)
                         setTimeout(
                         function()
                             {
                                $('.loyalty-operation').html( '<span> Points </br>'+alltotal +'</span>');
                                $('.loyalty-total').html('Total : '+total);
                                $(".cadre-point").css({"background-color": "#35717B"});
                              }, 150);
                     }
                }
            }
     Registries.Component.extend(SaleOrderManagementControlPanel, QuotationOrder);
});
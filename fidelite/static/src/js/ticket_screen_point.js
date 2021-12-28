odoo.define('TickerScreenPoint',function(require){

    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');
    const { useListener } = require('web.custom_hooks');
    const rpc = require('web.rpc');

    const TickerScreenPoint = TicketScreen =>
        class extends TicketScreen{
            constructor() {
                super(...arguments);
                useListener('do-refund', this.add_points);
                useListener('close-screen', this.add_point_on_close);
            }
            add_points(){
                const order = this.getSelectedSyncedOrder();
                if(order){
                    const userInfo = order.get_client();
                    let alltotal = 0
                     const existLoyalty = userInfo.loyalty ;
                     alltotal = this.env.pos.get_order().get_subtotal();
                     const total =  Math.round(alltotal + existLoyalty);
                     setTimeout(
                     function()
                         {
                            $('.loyalty-operation').html( '<span> Points </br>'+alltotal +'</span>');
                            $('.loyalty-total').html('Total : '+total);
                            $(".cadre-point").css({"background-color": "#35717B"});
                          }, 200);
                }
            }

             add_point_on_close(){
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
                          }, 200);
              }

            }


        }

     Registries.Component.extend(TicketScreen, TickerScreenPoint);
     return TickerScreenPoint ;
});
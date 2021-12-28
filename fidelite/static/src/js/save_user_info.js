odoo.define('fidelite.SaveUserInfo', function(require) {
   'use strict';
   //affiche le programme de fidelite lorsque le point est superieur 100000

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');
    const { useListener } = require('web.custom_hooks');
    const rpc = require('web.rpc');
    const SaveUserInfo = PaymentScreen =>
        class extends PaymentScreen {

            constructor() {
                super(...arguments);
                useListener('new-payment-line', this.resetData);
            }

            changeColor(){
                const userInfo = this.env.pos.get_client();
                if (userInfo){
                    if(userInfo.loyalty >= 100000){
                        $('.control-button-reward').css('background-color','#AACE3A');
                    }else{
                        $('.control-button-reward').css('background-color','');
                    }
                }
            }

            add_points(){
                console.log('---------kisissisisisisisisisisisissi-------------------',this.env.pos.get_client())
                console.log('---------pososososososos-------------------',this.env.pos)
                const userInfo = this.env.pos.get_client();
                if(userInfo){
                    console.log('--------------------->>>>>>>>>>>>>>>>>88888888888--kiiiiii--POS-orders',this.env.pos.get_order());
                    console.log('>>>>>>>>>>>>>>>--kiiiiii--POS-orders',this.env.pos.get_order().orderlines.models);
                    const existLoyalty = userInfo.loyalty ;
                    const order = this.env.pos.get_order().orderlines.models ;
                    let alltotal = 0
                    //calcul du prix totale de article du client
                    _.each(order, function(line){
                         alltotal = (line.price * line.quantity) + alltotal ;
                          });
                     console.log('totototo-------',alltotal);

                     const subtotal = this.env.pos.get_order().get_subtotal();
                     let linePoint = this.env.pos.get_order().get_selected_orderline().price ;
                     console.log('--------------------->>>>>>>>>>>>>>>>>line pointe',);
                     const total = Math.round(existLoyalty + alltotal)
                     setTimeout(
                          function()
                          {
                            $('.loyalty-operation').html( '<span> Points </br>'+'+' + alltotal +'</span>');
                             console.log('--------------------->>>>>>>>>>>>>>>>>tototal',total);
                             $('.loyalty-total').html('Total : '+total);
                             $(".cadre-point").css({"background-color": "#35717B"});
                          }, 200);

                  }else{
                     $('.loyalty-operation').html( '<span></span>');
                     $('.loyalty-total').html('');
                  }
            }

            update_user_info(userInfo){
                let loyalty = parseFloat(userInfo.loyalty);
                console.log("wep wep wep ----------------",(loyalty));
                rpc.query({
                model: 'res.partner',
                method: 'save_user',
                args: [userInfo.id, loyalty],
                }).then(function (result) {

                });
            }

            resetData() {
                const userInfo = this.env.pos.get_client()
                if (userInfo){
                    console.log('----------typeof loyalty----------',this.env.receipt);
                    console.log('----------type pvp----------',(this.env.pos.user_point));

                    userInfo.loyalty = this.env.pos.user_point //parseFloa
                    this.env.pos.remiseAdd = false
                    this.env.pos.user_point_validate_payment = 0
                    //this.env.bus.on('save-customer', this, userInfo);
                    console.log('-----------------user info',userInfo);
                    this.update_user_info(userInfo);
                    this.env.pos.user_point = 0;
                }

            }

        }
        Registries.Component.extend(PaymentScreen, SaveUserInfo);

        return PaymentScreen;
});
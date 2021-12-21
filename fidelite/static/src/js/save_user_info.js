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
                    console.log('----------type pvp----------',typeof(this.env.pos.user_point_validate_payment));

                    userInfo.loyalty = this.env.pos.user_point //parseFloat
                    this.env.pos.user_point = 0
                    this.env.pos.remiseAdd = false
                    this.env.pos.user_point_validate_payment = 0
                    //this.env.bus.on('save-customer', this, userInfo);
                    console.log('-----------------user info',userInfo);
                    this.update_user_info(userInfo)
                }

            }

        }
        Registries.Component.extend(PaymentScreen, SaveUserInfo);

        return PaymentScreen;
});
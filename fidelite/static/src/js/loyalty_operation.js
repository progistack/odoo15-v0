odoo.define('fidelite.LoyaltyOperation', function (require) {
"use strict";

    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const addPoint = 0


    const LoyaltyOperation = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
                //useListener('click-product', this.onSelectClient);
                useListener('click-product', this.add_point);
                useListener('click-product', this.changeColor);
                useListener('click-customer', this.add_point);
                useListener('set-numpad-mode', this.add_point);
                useListener('update-selected-orderline', this.add_point);
                useListener('new-orderline-selected', this.add_point);
                useListener('click-pay', this.add_point);
            }
            add_point() {
                const userInfo = this.env.pos.get_client()
                if (userInfo){
                    //$('.display-point').html('<p> Points </p>')
                    if (this.env.pos.remiseAdd){
                        if (this.env.pos.get_order().get_selected_orderline()){
                            const existLoyalty = userInfo.loyalty
                            const subtotal = this.env.pos.get_order().get_subtotal()
                            $('.loyalty-operation').html( '<span> Points </br>'+'+' + subtotal +'</span>');
                            const total = subtotal + existLoyalty;
                            $('.loyalty-total').html('Total : '+total);
                            $(".cadre-point").css({"background-color": "#35717B"});
                            this.env.pos.user_point = total
                        }
                    }else{
                        console.log('--------------------->>>>>>>>>>>>>>>>>88888888888',this.env.pos.remiseAdd);
                        const existLoyalty = userInfo.loyalty ;
                        const subtotal = this.env.pos.get_order().get_subtotal();
                        console.log('--------------------->>>>>>>>>>>>>>>>>subtototal',subtotal);
                        $('.loyalty-operation').html( '<span> Points </br>'+'+' + subtotal+'</span>');
                        const total = existLoyalty + subtotal
                        console.log('--------------------->>>>>>>>>>>>>>>>>tototal',total);
                        $('.loyalty-total').html('Total : '+total);
                        $(".cadre-point").css({"background-color": "#35717B"});
                        this.env.pos.user_point = total

                    }
                }else{
                    console.log('--------------------->>>>>>>>>>>>>>>>>ooooooooooooooooooo');
                    $('.loyalty-operation').html( '<span></span>');
                    $('.loyalty-total').html('');
                }

            }
            reset_point(){
                this.add_point()
            }

            changeColor(){
                const userInfo = this.env.pos.get_client();
                if (userInfo){
                    if(userInfo.loyalty >= 100000){
                        $('.control-button-reward').css('background-color','#AACE3A');
                    }
                }
            }
        }

        /* gestion du click avec jquery
        $(".next").click(function(){
                    alert("kissi-----------kisi")
                });
                this.add_point()
        */

    Registries.Component.extend(ProductScreen, LoyaltyOperation);

    return ProductScreen;



});
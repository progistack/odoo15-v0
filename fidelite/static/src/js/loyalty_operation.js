odoo.define('fidelite.LoyaltyOperation', function (require) {
"use strict";

    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const {useBarcodeReader } = require('point_of_sale.custom_hooks');
    const addPoint = 0


    const LoyaltyOperation = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
                //useListener('click-product', this.onSelectClient);
                useListener('click-product', this.add_point_click_product);
                useListener('click-product', this.changeColor);
                useListener('click-customer', this.add_point_click_product);
                useListener('set-numpad-mode', this.add_point_click_product);
                useListener('update-selected-orderline', this.addPointUpdateOrderLine);
                useListener('new-orderline-selected', this.add_point_click_product);
                useListener('click-pay', this.add_point_click_product);
                //useBarcodeReader({'point': this.add_point_click_product });
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
                            const total = Math.round(subtotal + existLoyalty);
                            $('.loyalty-total').html('Total : '+total);
                            $(".cadre-point").css({"background-color": "#35717B"});
                            this.env.pos.user_point = total
                        }
                    }else{
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
                        let linePoint = this.env.pos.get_order().get_selected_orderline();
                        console.log('--------------------->>>>>>>>>>>>>>>>>line pointe');
                        const total = Math.round(existLoyalty + subtotal);
                        this.env.pos.user_point = total;
                        setTimeout(
                          function()
                          {
                              $('.loyalty-operation').html( '<span> Points </br>'+'+' + subtotal +'</span>');
                              $('.loyalty-total').html('Total : '+total);
                              $(".cadre-point").css({"background-color": "#35717B"});
                          }, 50);

                    }
                }else{
                    console.log('--------------------->>>>>>>>>>>>>>>>>ooooooooooooooooooo');
                    $('.loyalty-operation').html( '<span></span>');
                    $('.loyalty-total').html('');
                }

            }

            add_point_click_product() {
                const userInfo = this.env.pos.get_client()
                //console.log('eeeeekkeekkkkkkke--------------',this.env.pos.get_order().orderlines.last().cid);
                if (userInfo){
                    //$('.display-point').html('<p> Points </p>')
                    if (this.env.pos.remiseAdd){
                        if (this.env.pos.get_order().get_selected_orderline()){
                            const existLoyalty = userInfo.loyalty;
                            const order = this.env.pos.get_order().orderlines.models ;
                            let subtotal = 0;
                            let total = existLoyalty + this.env.pos.get_order().get_subtotal();
                            setTimeout(
                                  function()
                                  {
                                      _.each(order, function(line){
                                        subtotal = (line.price * line.quantity) + subtotal ;
                                      });
                                      total =Math.round(subtotal + existLoyalty);
                                      $('.loyalty-operation').html( '<span> Points </br>'+'+' + subtotal +'</span>');
                                      $('.loyalty-total').html('Total : '+total);
                                      $(".cadre-point").css({"background-color": "#35717B"});
                                  }, 50);

                            this.env.pos.user_point = total;

                        }
                    }else{
                        console.log('--------------------->>>>>>>>>>>>>>>>>88888888888--kiiiiii--POS-orders',this.env.pos.get_order());
                        console.log('>>>>>>>>>>>>>>>--kiiiiii--POS-orders',this.env.pos.get_order().orderlines.models);
                        const existLoyalty = userInfo.loyalty ;
                        const order = this.env.pos.get_order().orderlines.models ;
                        let alltotal = 0
                        let total = existLoyalty + this.env.pos.get_order().get_subtotal();
                        //calcul du prix totale de article du client

                        setTimeout(
                          function()
                          {
                              _.each(order, function(line){
                                alltotal = (line.price * line.quantity) + alltotal ;
                              });
                              total = Math.round(existLoyalty + alltotal);
                              $('.loyalty-operation').html( '<span> Points </br>'+'+' + alltotal +'</span>');
                              $('.loyalty-total').html('Total : '+total);
                              $(".cadre-point").css({"background-color": "#35717B"});
                          }, 50);
                       this.env.pos.user_point = total;
                       this.env.pos.orderTotal = alltotal;
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
                    }else{
                        $('.control-button-reward').css('background-color','');
                    }
                }
            }

            addPointUpdateOrderLine(){
                 const userInfo = this.env.pos.get_client();
                 let rewards = this.env.pos.rewards;
                if (userInfo){
                    const rewardsList=[];
                    let minimum_point = 0;
                    if (rewards) {
                          _.each(rewards, function(reward){
                                rewardsList.push({
                                    id:	reward.id,
                                    label: reward.name,
                                });

                                minimum_point = reward.minimum_point;
                               });
                        }
                    if (this.env.pos.remiseAdd){
                        if (this.env.pos.get_order().get_selected_orderline()){
                            console.log('click ----------------',this.env.pos.get_order());
                            console.log('click ----------------product',this.env.pos.get_order().get_selected_orderline().product);
                            let product = this.env.pos.get_order().get_selected_orderline().product ;
                            if(product.barcode == "0123456789"){
                                if(this.env.pos.get_order().get_selected_orderline().quantity == 0){
                                    userInfo.loyalty = userInfo.loyalty + minimum_point
                                    this.env.pos.remiseAdd = false ;
                                    this.env.pos.remiseAjoute==0;
                                }
                            }
                            const existLoyalty = userInfo.loyalty;
                            const order = this.env.pos.get_order().orderlines.models ;
                            let subtotal = 0;
                            let total = existLoyalty + this.env.pos.get_order().get_subtotal();

                            setTimeout(
                                  function()
                                  {
                                      _.each(order, function(line){
                                        subtotal = (line.price * line.quantity) + subtotal ;
                                      });
                                      total =Math.round(subtotal + existLoyalty);
                                      $('.loyalty-operation').html( '<span> Points </br>'+'+' + subtotal +'</span>');
                                      $('.loyalty-total').html('Total : '+total);
                                      $(".cadre-point").css({"background-color": "#35717B"});
                                  }, 50);

                            this.env.pos.user_point = total;

                        }
                    }else{
                        const existLoyalty = userInfo.loyalty ;
                        const order = this.env.pos.get_order().orderlines.models ;
                        let alltotal = 0
                        let total = existLoyalty + this.env.pos.get_order().get_subtotal();
                        //calcul du prix totale de article du client

                        setTimeout(
                          function()
                          {
                              _.each(order, function(line){
                                alltotal = (line.price * line.quantity) + alltotal ;
                              });
                              total = Math.round(existLoyalty + alltotal);
                              $('.loyalty-operation').html( '<span> Points </br>'+'+' + alltotal +'</span>');
                              $('.loyalty-total').html('Total : '+total);
                              $(".cadre-point").css({"background-color": "#35717B"});
                          }, 50);
                       this.env.pos.user_point = total;
                       this.env.pos.orderTotal = alltotal;
                    }
                }else{
                    console.log('--------------------->>>>>>>>>>>>>>>>>ooooooooooooooooooo');
                    $('.loyalty-operation').html( '<span></span>');
                    $('.loyalty-total').html('');
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
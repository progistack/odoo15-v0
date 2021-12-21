odoo.define('fidelite.SelectCustomer', function(require){
    "use strict";
    const { posbus } = require('point_of_sale.utils');
    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    const SelectCustomer = ClientListScreen =>
        class extends ClientListScreen{
            constructor() {
                super(...arguments);
                useListener('save-changes', this.text);
                useListener('click-edit', this.text);
                }

                text(){
                    $(".next").click(function(){
                    alert("kissi-----------kisi")
                });
                }

                changeColor(){
                    const userInfo = this.state.selectedClient;
                    if (userInfo){
                        if(userInfo.loyalty >= 100000){
                            if(this.env.pos.get_order().get_selected_orderline()){
                                $('.control-button-reward').css('background-color','#AACE3A');
                            }

                        }
                    }
                }
                get nextButton1() {
                    if (!this.props.client) {
                        return { command: 'set', text: this.env._t('Set Customer kissi') };
                    } else if (this.props.client && this.props.client === this.state.selectedClient) {
                        return { command: 'deselect', text: this.env._t('Deselect Customer kissi') };
                    } else {
                        return { command: 'set', text: this.env._t('Change Customer kissi') };
                    }
                }

                clickNext1() {
                    console.log('kissi ------------------22');
                    this.state.selectedClient = this.nextButton1.command === 'set' ? this.state.selectedClient : null;
                    this.confirm();
                    this.clientPoints();
                    this.changeColor();
                    console.log('-------------kiddididid',this.clients);
                    console.log('-------------emmememem',this.currentOrder);
                    console.log('-------------joce joce',this.clientPoints());
                    console.log('-------------rebe rebe',this.state.selectedClient);

                }

                clientPoints(){
                    const currentOrder = this.currentOrder;
                    // recuperation des info du client selectione
                    const client = this.state.selectedClient;
                    if (this.state.selectedClient){
                        const point = client.loyalty
                        //si ya ligne commande
                        if(this.env.pos.get_order().get_selected_orderline()){
                            console.log('attributes ******************',point);
                            const subtotal = this.env.pos.get_order().get_subtotal()
                            $('.loyalty-operation').html( '<span> Points </br>'+'+' + subtotal +'</span>');
                            const total = subtotal + point
                            $('.loyalty-total').html('Total : '+total);
                            $(".cadre-point").css({"background-color": "#35717B"});
                            this.env.pos.user_point = total
                        }
                    }else{
                        $('.loyalty-operation').html( '<span></span>');
                        $('.loyalty-total').html('');
                        $(".cadre-point").css({"background-color": ""});
                    }

                }


        }

        Registries.Component.extend(ClientListScreen, SelectCustomer);
        return SelectCustomer;




});
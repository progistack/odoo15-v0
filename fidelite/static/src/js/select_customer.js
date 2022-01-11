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
                }

                changeColor(){
                    let rewards = this.env.pos.rewards;
                    const userInfo = this.state.selectedClient;
                    if (userInfo){
                        let minimum_point = 0;
                        let amount_fexed = 0;
                        let cost_reward = 0;
                        const rewardsList=[];
                        if (rewards) {
                              _.each(rewards, function(reward){
                                    rewardsList.push({
                                        id:	reward.id,
                                        label: reward.name,
                                    });

                                    minimum_point = reward.minimum_point;
                                    amount_fexed = reward.amount_fexed;
                                    cost_reward = reward.cost_reward ;
                                   });
                            }
                        if(userInfo.loyalty >= minimum_point){
                            if(this.env.pos.get_order().get_selected_orderline()){
                                $('.control-button-reward').css('background-color','#AACE3A');
                            }

                        }else{
                            $('.control-button-reward').css('background-color','');
                        }
                    }
                }
                get nextButton1() {
                    if (!this.props.client) {
                        return { command: 'set', text: this.env._t('Set Customer') };
                    } else if (this.props.client && this.props.client === this.state.selectedClient) {
                        return { command: 'deselect', text: this.env._t('Deselect Customer') };
                    } else {
                        return { command: 'set', text: this.env._t('Change Customer') };
                    }
                }

                clickNext1() {
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
                            const total = Math.round(subtotal + point);
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
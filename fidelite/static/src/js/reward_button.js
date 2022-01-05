odoo.define('fidelite.RewardButton', function (require) {
 "use strict";
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   const PaymentScreen = require('point_of_sale.PaymentScreen');
   const rpc = require('web.rpc');
   class CustomRewardButtons extends PosComponent {
       constructor() {
           super(...arguments);
           useListener('click', this.onClick);


       }
       is_available() {
           const order = this.env.pos.get_order();
           return order
       }

    //prix total
        total_price() {
            const articles = this.env.pos.get_order().orderlines.models;
            let total = 0;
            console.log('france----------');
            _.each(articles, function(article){
                total = total + (article.price * article.quantity)
            });
            return total;
       }

       add_point(minimum_point) {
           const userInfo = this.env.pos.get_client();
           if (userInfo){

               const existLoyalty = this.env.pos.user_point;
               $('.loyalty-operation').html( '<span> Points </br>'+'-' + minimum_point+'</span>');
               this.env.pos.user_point =  this.env.pos.user_point - minimum_point;
               $('.loyalty-total').html('Total : '+ this.env.pos.user_point);
               $(".cadre-point").css({"background-color": "#35717B"});
               this.env.pos.user_point_validate_payment = total;
               console.log('---------1000-------',this.env);
               console.log('this....',this.env.pos.get_order());
           }

       }

       async onClick() {
            const userInfo = this.env.pos.get_client()
            let rewards = this.env.pos.rewards;
            console.log('info info info', );
            const test = this.env.pos.set_loyalty(this.env.pos.get_order().get_subtotal());//remplacer total_price par sub_total get_subtotal()
            console.log(">>>>>>>>>>>>777>0000-----",this.env.pos);
            console.log("product------------7-product",this.env.pos.get_order().get_subtotal());
            console.log("0000000000*****-----", this.env.pos.user_point);

            if(userInfo){
                let minimum_point = 0;
                let amount_fexed = 0;
                const rewardsList=[];
                if (rewards) {
                      _.each(rewards, function(reward){
                            rewardsList.push({
                                id:	reward.id,
                                label: reward.name,
                            });

                            minimum_point = reward.minimum_point;
                            amount_fexed = reward.amount_fexed;
                            console.log(">>>>>>>>>>>>>0000-----",userInfo);
                           });
                    }
                if (userInfo.loyalty >= minimum_point ){
                    if (this.env.pos.get_order().get_subtotal() >= amount_fexed){

                        console.log("client....",this.env.pos.get_client().loyalty);

                        const { confirmed, payload} = await this.showPopup("SelectionPopup", {
                               title: 'Veuillez sélectionner la récompense',
                               list: rewardsList,
                           });
                        if (confirmed) {

                            const products = this.env.pos.db.product_by_barcode;
                            const product = products['0123456789'];
                            console.log('*******----------------<<<<<<<<<',product);
                            if (product){
                                product.lst_price = - amount_fexed;
                                console.log('------->>>>>>>',(this.env.pos.get_order().get_subtotal() - amount_fexed));
                                this.env.pos.get_order().add_product(product);
                                userInfo.loyalty = userInfo.loyalty - minimum_point;
                                console.log('----------typeof amount_fexed----------',typeof(amount_fexed));
                                console.log('------->>>>>>>',(this.env.pos.get_order().get_subtotal()));
                                //this.env.bus.on('save-customer', this, userInfo);
                                const sub_total = this.env.pos.get_order().get_subtotal()  ;
                                const existLoyalty = this.env.pos.user_point;
                                let allPoint = userInfo.loyalty + sub_total;
                                this.env.pos.user_point = allPoint;
                                console.log('----------typeof loyalty env----------',(this.env.pos.user_point));

                                setTimeout(
                                  function()
                                  {
                                      $('.loyalty-operation').html( '<span> Points </br>'+'+' + sub_total+' </br> </span>'+'<span> '+'-' + minimum_point+'</span>');
                                      $('.loyalty-total').html('Total: '+ allPoint);
                                      $(".cadre-point").css({"background-color": "#35717B"});
                                  }, 50);


                                this.env.pos.user_point_validate_payment = this.env.pos.user_point_validate_payment - minimum_point;
                                console.log('----------typeof loyalty----------',typeof(this.env.pos.user_point_validate_payment));
                                this.env.pos.remiseAdd = true;
                                this.env.pos.remiseAjoute = 100
                                console.log('---------1000-------',allPoint);
                                console.log('this....pos-----------',this.env.pos);
                                product.lst_price = 0;
                                console.log('----------typeof loyalty env----------',(this.env.pos.user_point));
                            }

                        }
                      }else{

                            var self = this;
                            const { confirmed, payload } = await this.showPopup('ErrorPopup', {
                            title: this.env._t('Pas de récompense disponible'),
                            body: this.env._t("le montant de l'achat doit être superieur ou égal au prix de la remise"),
                            });

                      }
                }else{
                    var self = this;
                    const { confirmed, payload } = await this.showPopup('ErrorPopup', {
                    title: this.env._t('Pas de récompense disponible'),
                    body: this.env._t("Il n'y a pas de récompense disponible pour ce client dans le cadre du programme de fidelité"),
                    });
                    if (confirmed) {
                        console.log(payload, 'payload');
                    }
                }
		    }
       }

   }


  //Add coupon button and set visibility
      CustomRewardButtons.template = 'CustomRewardButtons';
      ProductScreen.addControlButton({
      component: CustomRewardButtons,
      condition: function() {
          return this.env.pos;
          // this.env.pos.selectedClient=true
      },
  });
  Registries.Component.add(CustomRewardButtons);
  return CustomRewardButtons;
});
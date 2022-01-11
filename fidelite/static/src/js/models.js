odoo.define('fidelite.models', function (require) {
  "use strict";

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;

    models.load_models({
        model: 'loyalty.reward',
        fields: ['name','type_reward','cost_reward','minimum_point','discount_product_id','discount_type','loyalty_programme_id','amount_fexed','minimal_amount'],
        loaded: function(self,result){
            self.rewards=[{}]
            self.user_point = 0
            self.orderTotal = 0
            self.user_point_validate_payment = 0
            self.remiseAdd = false
            self.ticket_min_point =0
            self.remiseAjoute =0
            if(result.length){
                console.log("bonjour >>>>>>>>>>>>>>>>>>>>>>>>>>",result)

                _.each(result, function(value){
                    self.set('rewardName',result[0].name);
                    console.log('reward----------------------',result[0].name);
                    console.log('******************',value.name);
                    self.rewards.push({
                    id: value.id,
                    name: value.name,
                    minimum_point: value.minimum_point,
                    amount_fexed: value.amount_fexed,
                    cost_reward: value.cost_reward
                    })
                    console.log('<<<<<<<<<<<<<<<<<<<',self.rewards)

                });
            }
        }
        });

    models.load_models({
        model: 'programme.loyalty',
        fields: ['name_programme','point_franc','loyalty_reward_id'],
        loaded: function(self,result){
            if(result.length){
                console.log("bonjour >>>>>>>>>>>>>>>>>>>>>>>>>>22",result[0])
                self.set('rewardName22',result[0].name);
            }
        }
        });

    models.PosModel = models.PosModel.extend({
        get_list: function () {
            console.log('--------------------odoo',this.rewards)
        },
        set_loyalty: function (loyalty) {
            this.set('loyalty', loyalty);
            this.db.save('loyalty', loyalty || null);
        },
        product_service: function(){
            const product = this.db.get_product_by_id(184)
            return product
        }
    });

    models.Order = models.Order.extend({
        export_for_printing: function () {
            var res = _super_order.export_for_printing.apply(this, arguments);
            res.place = this.pos.get_list();
            return res;
        },

        export_as_JSON: function () {
            var json = _super_order.export_as_JSON.apply(this, arguments);
            var place = this.pos.get_list();
            return json;
        },
    });

});
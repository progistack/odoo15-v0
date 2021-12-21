odoo.define('fidelite.LoyaltyField', function (require) {

    "use strict";

    var models = require('point_of_sale.models');
    const ProductScreen = require('point_of_sale.ClientDetailsEdit');
    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { posbus } = require('point_of_sale.utils');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function(session,attributes)
        {
            var self = this;
            console.log("bonjour1");
            var contact_model = _.find(this.models,function(model)
            {
                return model.model === 'res.partner';
            });
            models.load_fields('res.partner', ['loyalty']);
            console.log("loyal",models.load_fields('res.partner','loyalty'))
            contact_model.fields.push('loyalty');
            _super_posmodel.initialize.apply(this, arguments);
        },

    });


});


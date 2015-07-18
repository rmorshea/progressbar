define(["jquery", "widgets/js/widget"], function($, widget) {

    var ProgressView = widget.DOMWidgetView.extend({
        
        render: function(){
            this.$outer = document.createElement('div');
            this.$inner = document.createElement('div');
            this.$outer.appendChild(this.$inner);
            this.$inner.style.width = "0px";

            this._outer_style_changed();
            this._inner_style_changed();

            this.$el.append(this.$outer);

            this.model.on('change:outer_style', this._outer_style_changed, this);
            this.model.on('change:inner_style', this._inner_style_changed, this);
            this.model.on('change:_inner_attr', this._inner_attr_changed, this);
            this.model.on('change:_outer_attr', this._outer_attr_changed, this);
            this.model.on('change:max_width', this._limit_changed, this);
            this.model.on('change:value', this._value_changed, this);
        },

        _inner_style_changed: function() {
            var inner_style = this.model.get('inner_style');
            for (var key in inner_style) {
                if (inner_style.hasOwnProperty(key)) {
                    this.$inner.style[key] = inner_style[key];
                }
            }
        },

        _outer_style_changed: function() {
            var outer_style = this.model.get('outer_style');
            for (var key in outer_style) {
                if (outer_style.hasOwnProperty(key)) {
                    this.$outer.style[key] = outer_style[key];
                }
            }
        },

        _inner_attr_changed: function() {
            t = this.model.get('_inner_attr');
            this.$inner.style[t[0]] = t[1];
        },

        _outer_attr_changed: function() {
            t = this.model.get('_outer_attr');
            this.$outer.style[t[0]] = t[1];
        },

        _maxwidth_changed:function() {
            var limit = parseInt(this.model.get('max_width').match(/\d+/)[0]);
            var new_width = this.model.get('value')*limit;
            this.$inner.style.width = Math.round(new_width)+"px";
        },

        _value_changed: function() {
            var limit = parseInt(this.model.get('max_width').match(/\d+/)[0]);
            var new_width = this.model.get('value')*limit;
            this.$inner.style.width = Math.round(new_width)+"px";
        }

    });

    return {ProgressView: ProgressView};
});
(function($) {
  $.fn.applyKoBindings = function(view_model) {
    this.each(function(index, element) {
        ko.applyBindings(view_model, element);
    });

    return this;
  };
})(jQuery);
(function($) {
  var show_details = function(){
    alert($(this).data('id'));
  }
  $(document).on('ready', function(){
    $('.detalle').on('click', show_details);
  });
})(grp.jQuery);

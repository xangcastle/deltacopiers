(function($) {
  var show_details = function(){
    var SM = new SimpleModal({"width":600});
      SM.addButton("Action button", "btn primary", function(){
          this.hide();
      });
      SM.addButton("Cancel", "btn");
      SM.show({
        "model":"modal-ajax",
        "title":"Title",
        "param":{
          "url":"ajax-content.php",
          "onRequestComplete": function(){ /* Action on request complete */ }
        }
      });
  }
  $(document).on('ready', function(){
    $('.detalle').on('click', show_details);
  });
})(grp.jQuery);

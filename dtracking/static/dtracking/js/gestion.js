
  var show_details = function(){
    var gestion = $(this).data('id');
    console.log(gestion);
    $.ajax('/dtracking/view_details/',{
      type: 'POST',
      data: {'id': gestion},
      success: function(data){
        console.log(data);
        var modal = $('#grappelli-modal');
        var body = modal.find(".modal-body")
        body.empty();
        $.each(data.media, function(key, value){
          body.append('<img src="' + value.archivo +'" />');
        });
        modal.modal('show');
      },
    })
  }
  $(document).on('ready', function(){
    $('.detalle').on('click', show_details);
  });

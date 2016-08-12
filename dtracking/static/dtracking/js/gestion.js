
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
        $.each(data.media, function(key, value){
          console.log(value);
        });
        modal.modal('show');
      },
    })
  }
  $(document).on('ready', function(){
    $('.detalle').on('click', show_details);
  });

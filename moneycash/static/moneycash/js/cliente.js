
var readonly = function (clase, option) {
    $(clase).prop('readonly', option);
}

var complete_cliente = function () {
  var _self = $(this);
      if($.trim($(_self).val()) != '') {
          $(_self).autocomplete({
              minLength: 2,
              source: "/moneycash/autocomplete_cliente",
              select: function(event, ui) {
                  $('#cliente').val(ui.item.obj.id);
                  $('#code').val(ui.item.obj.code);
                  $('#name').val(ui.item.obj.name);
                  $('#ident').val(ui.item.obj.ident);
                  $('#phone').val(ui.item.obj.phone);
                  $('#email').val(ui.item.obj.email);
                  $('#address').val(ui.item.obj.address);
                  readonly('.datos_cliente input, .datos_cliente textarea', true);
                  var tabla = $('#facturasPendientes tbody').empty();
                  $.each(ui.item.obj.facturas, function(key, value){
                    var fila = '<tr><td>'+value.numero+'</td><td>'+value.fecha+'</td><td>'+value.total+'</td></tr>';
                    tabla.append(fila);
                  });
              }
          });
      }
  }

var limpiar_cliente = function(){
  $('.datos_cliente input, .datos_cliente textarea')
    .val("")
    .attr('readonly', false);
  $('.datos_cliente #code').attr('readonly', true);
}

var editar_cliente = function(){
  $('.datos_cliente input, .datos_cliente textarea')
    .attr('readonly', false);
  $('.datos_cliente #code').attr('readonly', true);
  $('.datos_cliente #name').attr('readonly', true);
  $('.datos_cliente #ident').attr('readonly', true);
}

var detalle_cliente = function(){
  var cliente = $('#cliente');
  if (parseInt(cliente.val()) > 0) {
    var modal = $('#detalleCliente').modal('show');
  }
}

$(document).on('ready', function(){
    $('.datos_cliente #name').on('keyup', complete_cliente);
    $('#borrar_cliente').on('click', limpiar_cliente);
    $('#editar_cliente').on('click', editar_cliente);
    $('#ecuenta').on('click', detalle_cliente)
});

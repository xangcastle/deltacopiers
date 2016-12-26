var factura = function(){
  $.ajax("/moneycash/detalle_factura/", {
    type: "POST",
    data: {'id': $(this).attr('id'), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
    success: function(data){
      console.log(data);
      var form = $('form');
      form.find('#factura').val(data.id);
      form.find('#factura_numero').val(data.numero);
      form.find('#factura_subtotal').val(data.subtotal);
      form.find('#factura_descuento').val(data.descuento);
      form.find('#factura_iva').val(data.iva);
      form.find('#factura_retencion').val(data.retension);
      form.find('#factura_total').val(data.total);
      $('select[name="monedas"]').val(data.moneda);
      form.find('#code').val(data.cliente_data.code);
      form.find('#name').val(data.cliente_data.name);
      form.find('#ident').val(data.cliente_data.ident);
      form.find('#email').val(data.cliente_data.email);
      form.find('#phone').val(data.cliente_data.phone);
      form.find('#address').val(data.cliente_data.address);
      $('#saldo-disponible').val(data.cliente_data.saldo_disponible);
      $('#limite-credito').val(data.cliente_data.limite_credito);
      $('#saldo-actual').val(data.cliente_data.saldo);
      form.find('#tipopago').val(data.tipopago);
      $('title').text("Factura # " + data.numero)
    }
  })
  $('#metodos-pago').show();
  $('#formulario').show();
  $('#listado').hide();
}

var imprimir = function () {
  if ($('#tipopago').val()=="contado") {
    if ( parseFloat($('#pago_total').val())>=parseFloat($('#factura_total').val()) ) {
      $.ajax({
          url:"../imprimir_factura/",
          type:"POST",
          data: {'id': $('#factura').val(), 'moneda': $('select[name="monedas"]').val(), 'tipopago': $('#tipopago').val()},
          success:function (result) {
              $(".impreso").empty().html(result);
              var resultado = $('.impreso').print();
              location.reload();
          }
      });
    }
  }else if ($('#tipopago').val()=="credito") {
    if ( parseFloat($('#saldo-disponible').val())>=parseFloat($('#factura_total').val()) ) {
      $.ajax({
          url:"../imprimir_factura/",
          type:"POST",
          data: {'id': $('#factura').val(), 'moneda': $('select[name="monedas"]').val(), 'tipopago': $('#tipopago').val()},
          success:function (result) {
              $(".impreso").empty().html(result);
              var resultado = $('.impreso').print();
              location.reload();
          }
      });
    }
  }

}

var cambiar_metodo = function(){
  $('.invicible').css('display', 'None');
  $('.'+$('#tipopago').val()).css('display', 'block');
}

$(document).on('ready', function(){
  $('#formulario').hide();
  $('#metodos-pago').hide();
  $('#listado tbody').on('click', 'tr', factura);
  $('#imprimir').on('click', imprimir);
  $('#tipopago').on('change', cambiar_metodo);
});

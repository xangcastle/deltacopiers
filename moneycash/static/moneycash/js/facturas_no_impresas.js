var factura = function(){
  $.ajax("/moneycash/detalle_factura/", {
    type: "POST",
    data: {'id': $(this).attr('id'), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
    success: function(data){
      console.log(data);
      var form = $('form');
      form.find('#factura_numero').val(data.numero);
      form.find('#factura_subtotal').val(data.subtotal);
      form.find('#factura_descuento').val(data.descuento);
      form.find('#factura_iva').val(data.iva);
      form.find('#factura_retencion').val(data.retension);
      form.find('#factura_total').val(data.total);
      form.find('#code').val(data.cliente_data.code);
      form.find('#name').val(data.cliente_data.name);
      form.find('#ident').val(data.cliente_data.ident);
      form.find('#email').val(data.cliente_data.email);
      form.find('#phone').val(data.cliente_data.phone);
      form.find('#address').val(data.cliente_data.address);
      form.find('#tipopago').val(data.cliente_data.tipopago);
    }
  })
  $('#metodos-pago').show();
  $('#formulario').show();
  $('#listado').hide();
}

$(document).on('ready', function(){
  $('#formulario').hide();
  $('#metodos-pago').hide();
  $('#listado tbody').on('dblclick', 'tr', factura);
});

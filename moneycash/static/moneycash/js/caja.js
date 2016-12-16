var totalizar_efectivo = function(){
  var tabla = $('#efectivoTable tbody tr');
  var total = 0.0;
  $.each(tabla, function(key, value){
    var cantidad = $(value).find('.efectivoCantidad');
    var nominacion = $(value).find('.efectivoNominacion');
    if(cantidad.val().length > 0){
      total +=(parseFloat(cantidad.val()) * parseFloat(nominacion.val()));
    }
  })
  $('#efectivoTotal').val(total.toFixed(2));
  return total;
}

var salvar_efectivo = function () {
  $('#pago_efectivo').val($('#efectivoTotal').val());
  $('#efectivoModal').modal('hide');
  totalizar_monto();
}

var totalizar_cheque = function(){
  var tabla = $('#chequeTable tbody tr');
  var total = 0.0;
  $.each(tabla, function(key, value){
    var monto = $(value).find('.chequeMonto');
    if(monto.val().length > 0){
      total += parseFloat(monto.val());
    }
  })
  $('#chequeTotal').val(total.toFixed(2));
  return total;
}

var campos_incompletos = function(selector) {
  var valor = false;
  var objects = $(selector);
  $.each(objects, function(i,o){
    if ($(o).val() == "") {
      $(o).focus();
      valor = true;
    }
  });
  return valor
}

var salvar_cheque = function () {
  if (campos_incompletos('input[name="chequeNumero"]')) {
      var err = $('<div class="alert alert-danger" role="alert">Por favor Complete todos los Campos..</div>');
      $(this).parent().find('.error').empty().append(err);
  } else if (campos_incompletos('input[name="chequeMonto"]')) {
      var err = $('<div class="alert alert-danger" role="alert">Por favor Complete todos los Campos..</div>');
      $(this).parent().find('.error').empty().append(err);
  } else {
    $('#pago_cheque').val($('#chequeTotal').val());
    $('#chequeModal').modal('hide');
    totalizar_monto();
  }
}

var totalizar_transferencia = function(){
  var tabla = $('#transferenciaTable tbody tr');
  var total = 0.0;
  $.each(tabla, function(key, value){
    var monto = $(value).find('.transferenciaMonto');
    if(monto.val().length > 0){
      total += parseFloat(monto.val());
    }
  })
  $(this).parent().find('.error').empty()
  $('#transferenciaTotal').val(total.toFixed(2));
  return total;
}

var salvar_transferencia = function () {
  if (campos_incompletos('input[name="transferenciaReferencia"]')) {
      var err = $('<div class="alert alert-danger" role="alert">Por favor Complete todos los Campos..</div>');
      $(this).parent().find('.error').empty().append(err);
  } else if (campos_incompletos('input[name="transferenciaMonto"]')) {
      var err = $('<div class="alert alert-danger" role="alert">Por favor Complete todos los Campos..</div>');
      $(this).parent().find('.error').empty().append(err);
  } else {
      $(this).parent().find('.error').empty()
      $('#pago_transferencia').val($('#transferenciaTotal').val());
      $('#transferenciaModal').modal('hide');
      totalizar_monto();
  }
}

var totalizar_tarjeta = function(){
  var tabla = $('#tarjetaTable tbody tr');
  var total = 0.0;
  $.each(tabla, function(key, value){
    var monto = $(value).find('.tarjetaMonto');
    if(monto.val().length > 0){
      total += parseFloat(monto.val());
    }
  })
  $('#tarjetaTotal').val(total.toFixed(2));
  return total;
}

var salvar_tarjeta = function () {
  $('#pago_tarjeta').val($('#tarjetaTotal').val());
  $('#tarjetaModal').modal('hide');
  totalizar_monto();
}

var totalizar_monto = function(){
  var moneda = "";
  if ($('select[name="monedas"]').val() == "cordobas") {
    moneda = "CORDOBA";
  } else {
    moneda = "DOLARE";
  }
  var monto = (parseFloat($('#pago_efectivo').val()) +parseFloat($('#pago_cheque').val()) + parseFloat($('#pago_transferencia').val()) + parseFloat($('#pago_tarjeta').val()))
  $('#pago_total').val(monto.toFixed(2));
  $('#montoLetras').val(NumeroALetras(monto, moneda));
  $('#pago_cambio').val((monto - parseFloat($('#factura_total').val())).toFixed(2));
}

$(document).on('ready', function () {
  $(function () {
      $('#fecha').datepicker({
          locale: 'es-NI'
      });
  });
  $('#pago_efectivo').on('click', function() {
    $('#efectivoModal').modal('show');
  });
  $('#pago_cheque').on('click', function() {
    $('#chequeModal').modal('show');
  });
  $('#pago_transferencia').on('click', function() {
    $('#transferenciaModal').modal('show');
  });
  $('#pago_tarjeta').on('click', function() {
    $('#tarjetaModal').modal('show');
  });
  $('.efectivoCantidad').on('change', totalizar_efectivo);
  $('#efectivoOk').on('click', salvar_efectivo);
  $('.chequeMonto').on('change', totalizar_cheque);
  $('#chequeOk').on('click', salvar_cheque);
  $('.transferenciaMonto').on('change', totalizar_transferencia);
  $('#transferenciaOk').on('click', salvar_transferencia);
  $('.tarjetaMonto').on('change', totalizar_tarjeta);
  $('#tarjetaOk').on('click', salvar_tarjeta);
  $('.moneycash_caja').addClass('active');
});

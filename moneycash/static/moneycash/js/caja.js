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

var salvar_cheque = function () {
  $('#pago_cheque').val($('#chequeTotal').val());
  $('#chequeModal').modal('hide');
  totalizar_monto();
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
  $('#transferenciaTotal').val(total.toFixed(2));
  return total;
}

var salvar_transferencia = function () {
  $('#pago_transferencia').val($('#transferenciaTotal').val());
  $('#transferenciaModal').modal('hide');
  totalizar_monto();
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
  var monto = (parseFloat($('.efectivo').html()) +parseFloat($('.cheque').html()) + parseFloat($('.transferencia').html()) + parseFloat($('.tarjeta').html()))
  $('#monto').val(monto.toFixed(2));
  $('#montoLetras').val(NumeroALetras(monto));
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

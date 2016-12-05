
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
                  console.log(ui.item.obj);
                  $('#cliente').val(ui.item.obj.id);
                  $('#code').val(ui.item.obj.code);
                  $('#name').val(ui.item.obj.name);
                  $('#ident').val(ui.item.obj.ident);
                  $('#phone').val(ui.item.obj.phone);
                  $('#email').val(ui.item.obj.email);
                  $('#address').val(ui.item.obj.address);
                  $('#saldo_total').val(ui.item.obj.saldo);
                  readonly('.datos_cliente input, .datos_cliente textarea', true);
                  var tabla = $('#facturasPendientes tbody').empty();
                  $.each(ui.item.obj.facturas, function(key, value){
                    var fila = '<tr><td><input type="checkbox" name="pagar"></td><td name="numero">'+ value.numero + '</td><td>' + value.date +'</td>'
                    fila += '<td><input type="checkbox" name="aplica_ir" data-calculo_ir="'+value.calculo_ir+'" style="display: None"> <label name="valor_ir">0.00</label>'
                    fila += '<input type="text" class="form-control" name="ir" style="display: None;"></td>'
                    fila += '<td><input type="checkbox" name="aplica_al" data-calculo_al="'+value.calculo_al+'" style="display: None"> <label name="valor_al">0.00</label>'
                    fila += '<input type="text" class="form-control" name="al" style="display: None"></td>'
                    fila += '<td name="total">'+value.total+'</td><td><input type="text" class="form-control" name="monto" value="0.00" readonly tr></td><td name="saldo">'+value.total+'</td></tr>';
                    tabla.append(fila);
                  });
                  actualizar_disponible();
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
    var modal = $('#detalleCliente');
    actualizar_disponible();
    modal.modal('show');
  }
}


var actualizar_disponible = function(){
  var disponible = parseFloat($('#pago_total').val());
  var total = 0.0;
  $.each($('input[name="monto"]'), function(i,o){
    total += parseFloat($(o).val());
  });
  $('#abono_total').val(total);
  $('#disponible').val(disponible - total);
}

var calcular_fila = function(){
  var pagar = $(this).parent().parent().find('input[name="pagar"]');
  var aplica_al = $(this).parent().parent().find('input[name="aplica_al"]');
  var aplica_ir = $(this).parent().parent().find('input[name="aplica_ir"]');
  var disponible = parseFloat($('#disponible').val());
  var monto = $(this).parent().parent().find('input[name="monto"]');
  var total = parseFloat($(this).parent().parent().find('td[name="total"]').html());
  var ir = parseFloat(aplica_ir.data('calculo_ir'));
  var al = parseFloat(aplica_al.data('calculo_al'));
  if (pagar.is(':checked')) {
    aplica_ir.css('display', 'block');
    aplica_al.css('display', 'block');
    monto.attr('readonly', false);
    if (aplica_ir.is(':checked') && aplica_al.is(':checked')) {
      monto.val(0.00);
      aplica_ir.parent().find('input[name="ir"]').css({'display': "block", 'max-width': "65px", 'max-height': "28px"});
      aplica_ir.parent().find('label').text(ir);
      aplica_al.parent().find('input[name="al"]').css({'display': "block", 'max-width': "65px", 'max-height': "28px"});
      aplica_al.parent().find('label').text(al);
      actualizar_disponible();
      disponible = parseFloat($('#disponible').val());
      if (disponible < (total-(ir+al))) {
        monto.val(disponible);
      } else {
        monto.val(total-(ir+al));
      }
    } else if (aplica_ir.is(':checked') && !aplica_al.is('checked')) {
      monto.val(0.00);
      aplica_ir.parent().find('input[name="ir"]').css({'display': "block", 'max-width': "65px", 'max-height': "28px"});
      aplica_ir.parent().find('label').text(ir);
      aplica_al.parent().find('input[name="al"]').css({'display': "None"});
      aplica_al.parent().find('label').text('0.00');
      actualizar_disponible();
      disponible = parseFloat($('#disponible').val());
      if (disponible < (total-ir)) {
        monto.val(disponible);
      } else {
        monto.val(total-ir);
      }
    } else if (aplica_al.is(':checked') && !aplica_ir.is('checked')) {
      aplica_al.parent().find('input[name="al"]').css({'display': "block", 'max-width': "65px", 'max-height': "28px"});
      aplica_al.parent().find('label').text(al);
      aplica_ir.parent().find('input[name="ir"]').css({'display': "None"});
      aplica_ir.parent().find('label').text('0.00');
      monto.val(0.00);
      actualizar_disponible();
      disponible = parseFloat($('#disponible').val());
      if (disponible < (total-al)) {
        monto.val(disponible);
      } else {
        monto.val(total-al);
      }
    } else {
      aplica_ir.parent().find('input[name="ir"]').css({'display': "None"});
      aplica_ir.parent().find('label').text('0.00');
      aplica_al.parent().find('input[name="al"]').css({'display': "None"});
      aplica_al.parent().find('label').text('0.00');
      monto.val(0.00);
      actualizar_disponible();
      disponible = parseFloat($('#disponible').val());
      if (disponible < total) {
        monto.val(disponible);
      } else {
        monto.val(total);
      }
    }
  } else {
    aplica_ir.css('display', 'None');
    aplica_ir.parent().find('input[name="ir"]').css({'display': "None"});
    aplica_ir.parent().find('label').text('0.00');
    aplica_al.css('display', 'None');
    aplica_al.parent().find('input[name="al"]').css({'display': "None"});
    aplica_al.parent().find('label').text('0.00');
    monto.attr('readonly', true);
    monto.val(0.00);
  }
  var valor_al = parseFloat(aplica_al.parent().find('label').text());
  var valor_ir = parseFloat(aplica_ir.parent().find('label').text());
  var saldo = total - (parseFloat(monto.val()) + valor_al + valor_ir);
  $(this).parent().parent().find('td[name="saldo"]').html(saldo);
  actualizar_disponible();
}


var validar_modal = function(){
  var modal = $('#detalleCliente');
  var disponible = $('#pago_total');
  var saldo = $('#saldo_total');
  var abono = $('#abono_total');
  var canceladas = [];
  var abonadas = [];
  if (parseFloat(disponible.val()) < parseFloat(abono.val())) {
    var err = $('<div class="alert alert-danger" role="alert">El abono total no puede ser mayor que el Disponible..</div>');
    $('.error').empty().append(err);
  } else {
    $('input[name="pagar"]:checked').each(function(){
        var ab = parseFloat($(this).parent().parent().find('input[name="monto"]').val());
        var sal = parseFloat($(this).parent().parent().find('td[name=saldo]').html());
        if (ab>0 && sal==0) {
          canceladas.push($(this).parent().parent().find('td[name="numero"]').html());
        } else {
          abonadas.push($(this).parent().parent().find('td[name="numero"]').html())
        }
    });
    var concepto = '';
    if (canceladas.length>1) {
      concepto += 'Cancelacion de facturas ';
      concepto += canceladas[0];
      for (var i = 1; i < canceladas.length-1; i++) {
        concepto += ', ' + canceladas[i];
      }
      concepto += ' y ' + canceladas[canceladas.length-1] + '. ';
    } else if (canceladas==1) {
      concepto += 'Cancelacion de factura ' + canceladas[0] + '. ';
    }
    if (abonadas.length>1) {
      concepto += 'Abono a facturas ';
      concepto += abonadas[0];
      for (var i = 1; i < abonadas.length-1; i++) {
        concepto += ', ' + abonadas[i];
      }
      concepto += ' y ' + canceladas[abonadas.length-1] + '.';
    } else if (abonadas.length==1) {
      concepto += 'Abono a factura ' + abonadas[0] + '. ';
    }
    $('#concepto').val(concepto);
    modal.modal('hide');
  }

}

var funka = function (){
  alert('funka');
}

$(document).on('ready', function(){
    $('.datos_cliente #name').on('keyup', complete_cliente);
    $('#borrar_cliente').on('click', limpiar_cliente);
    $('#editar_cliente').on('click', editar_cliente);
    $('#ecuenta').on('click', detalle_cliente);
    $('#detalleCliente').on('change', 'input[name="pagar"]', calcular_fila);
    $('#detalleCliente').on('change', 'input[name="monto"]', calcular_fila);
    $('#detalleCliente').on('change', 'input[name="aplica_ir"]', calcular_fila);
    $('#detalleCliente').on('change', 'input[name="aplica_al"]', calcular_fila);
    $('#clienteOk').on('click', validar_modal);
});

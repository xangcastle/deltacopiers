/*
factura.js
funciones
    completar datos del cliente
    completar info del producto

    calcular factura
        calcular subtotal
        calcular descuento
        calcular iva
        calcular ir
        calcular al
        calcular total
*/

var get_total = function (cantidad, precio) {
    return (parseFloat(cantidad) * parseFloat(precio)).toFixed(2);
}

var borrar = function (clase) {
    $(clase).val('');
}

var invalidar = function(event){
  if(event.data.opt){
      $(this).closest('.grp-tr').addClass('invalid');
  } else {
      $(this).closest('.grp-tr').removeClass('invalid');
  }
}

var readonly = function (clase, option) {
    $(clase).prop('readonly', option);
}

var get_descuento = function (event) {
  event.stopPropagation();
  event.preventDefault();
  if($(this).val().match(/(?:%)$/)) {
    var persent = parseFloat($(this).val().replace('%', ''))/100;
    $(this).val(parseFloat($(this).parents('.grp-tr')
        .find('input[type="text"].producto_precio').val()*persent).toFixed(2));
    }
    calcular_factura();
}

var tachar_cliente = function(event) {
    if(event.data.opt){
        $('.datos_cliente')
            .css({'text-decoration': 'line-through', 'color': 'red'});
    } else {
        $('.datos_cliente')
            .css({'text-decoration': 'none', 'color': 'black'});
    }
}

var limpiar_cliente = function() {
    borrar('.datos_cliente');
    readonly('.datos_cliente', false);
    tachar_cliente(false);
    $('span.borrar').remove();
}

var complete_cliente = function () {
    var _self = $(this);
        if($.trim($(_self).val()) != '') {
            $(_self).autocomplete({
                minLength: 2,
                source: "/ventas/autocomplete_cliente?opt="
                    +$(_self).prop('name'),
                select: function(event, ui) {
                    $('#id_code').val(ui.item.obj.code);
                    $('#id_name').val(ui.item.obj.name);
                    $('#id_identificacion').val(ui.item.obj.identificacion);
                    $('#id_telefono').val(ui.item.obj.telefono);
                    $('#id_email').val(ui.item.obj.email);
                    $('#id_direccion').val(ui.item.obj.direccion);
                    $('.box_cliente .grp-collapse-handler')
                        .empty()
                        .append("Datos del Cliente<span class='borrar'>X</span>");
                    readonly('.datos_cliente', true);
                }
            });
        }
    }

var complete_producto = function () {
    var _self = $(this);
        if($.trim($(_self).val()) != '') {
            $(_self).autocomplete({
                minLength: 2,
                source: "/ventas/autocomplete_producto",
                select: function(event, ui) {
                    var iva = parseFloat((ui.item.obj.precio-0)*0.15);
                    $(_self).parents('.grp-tr').find('.producto_cantidad').val(1);
                    $(_self).parents('.grp-tr').find('.producto_name').val(ui.item.obj.name);
                    $(_self).parents('.grp-tr').find('.producto_precio').val(ui.item.obj.precio);
                    $(_self).parents('.grp-tr').find('.producto_descuento').val(0.0);
                    $(_self).parents('.grp-tr').find('.producto_iva').val(iva.toFixed(2));
                    $(_self).parents('.grp-tr')
                        .find('.producto_total')
                        .val(get_total(1, ui.item.obj.precio)).change();
                        calcular_factura();
                }
            });
        }
    }

var totalizar = function(clase){
    var tabla = $('#detalle_set-group .grp-tr');
    var total = 0.0;
    for(var i=1;i<tabla.length-1;i++){
      var value = tabla[i];
      if($(value).hasClass('invalid')==false){
        total += parseFloat($(value).find('.producto_cantidad').val())
         * parseFloat($(value).find(clase).val());
      }
    }
    return total;
}

var calcular_detalle = function(){
  var tabla = $('#detalle_set-group .grp-tr');
  $.each(tabla, function(key, value){
    var cantidad = parseFloat($(value).find('.producto_cantidad').val());
    var precio = parseFloat($(value).find('.producto_precio').val());
    var descuento = parseFloat($(value).find('.producto_descuento').val());
      $(value).find('.producto_total').val(((cantidad*precio)-(cantidad*descuento)).toFixed(2));
      $(value).find('.producto_iva').val(precio*0.15);
  });
}

var calcular_retencion = function(porcentaje, subtotal, descuento){
  return ((subtotal - descuento) * porcentaje) / 100
}

var calcular_ir = function(subtotal, descuento){
  var total = 0.0;
  if(subtotal > 1000 && $('#id_aplica_ir').is(':checked')){
    total = calcular_retencion(2, subtotal, descuento);
  }
  return total;
}

var calcular_al = function(subtotal, descuento){
  var total = 0.0;
  if(subtotal > 1000 && $('#id_aplica_al').is(':checked')){
    total = calcular_retencion(1, subtotal, descuento);
  }
  return total;
}

var calcular_iva = function(){
  var total = 0.0;
  if($('#id_aplica_iva').is(':checked')){
    total += totalizar('.producto_iva');
  }
  return total
}

var calcular_factura = function(){
  calcular_detalle();
  var subtotal = totalizar('.producto_precio');
  var descuento = totalizar('.producto_descuento');
  var iva = calcular_iva();
  var ir = calcular_ir(subtotal, descuento);
  var al = calcular_al(subtotal, descuento);
  $('#id_subtotal').val(subtotal.toFixed(2));
  $('#id_descuento').val(descuento.toFixed(2));
  $('#id_iva').val(iva.toFixed(2));
  $('#id_ir').val(ir.toFixed(2));
  $('#id_al').val(al.toFixed(2));
  $('#id_total').val(((subtotal+iva)-(descuento+ir+al)).toFixed(2));
}


$(document).on('ready', function(){
    $('#id_name').on('keyup', complete_cliente);
    $('#factura_form').on('keyup', '.producto_code', complete_producto);
    $('.box_cliente').on('mouseover', 'h2 .borrar', {opt: true}, tachar_cliente);
    $('.box_cliente').on('mouseout', 'h2 .borrar', {opt: false}, tachar_cliente);
    $('.box_cliente').on('click', 'h2 .borrar', limpiar_cliente);
    $('#id_aplica_iva').on('change', calcular_factura);
    $('#id_aplica_ir').on('change', calcular_factura);
    $('#id_aplica_al').on('change', calcular_factura);
    $('#detalle_set-group').on('change', '.producto_cantidad', calcular_factura);
    $('#detalle_set-group').on('change', '.producto_descuento', get_descuento);
    $('#detalle_set-group').on('mouseover', '.grp-remove-handler', {opt: true}, invalidar);
    $('#detalle_set-group').on('mouseout', '.grp-remove-handler', {opt: false}, invalidar);
    $('body').on('DOMNodeRemoved', 'div', calcular_factura);
});



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
                  $('#label_cliente').html('<a id="editar_cliente">Editar </a><a id="borrar_cliente">Borrar </a>');
              }
          });
      }
  }

  var complete_producto = function () {
    var _self = $(this);
        if($.trim($(_self).val()) != '') {
            $(_self).autocomplete({
                minLength: 2,
                source: "/moneycash/autocomplete_producto",
                select: function(event, ui) {
                  var modal = $('#detalleModal')
                    load_modal(ui.item.obj.id);
                }
            });
        }
  }

  var load_modal = function (producto, bodega, cantidad, discount){
      bodega || ( bodega = undefined );
      cantidad || ( cantidad = undefined );
      discount || ( discount = undefined );
      var modal = $('#detalleModal');
      $.ajax("/moneycash/detalle_producto/", {
          type: 'POST',
          data: {'id': producto, 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
          success: function(data){
              modal.find('#producto').val(data.id);
              modal.find('.modal-title').html(data.name);
              modal.find('img').attr('src', data.imagen)
              modal.find('#no_part').val(data.no_part);
              modal.find('#price').val(data.price);
              modal.find('#cost').val(data.cost);
              if(cantidad){
                modal.find('#cantidad').val(cantidad);
              }else{
                modal.find('#cantidad').val(1);
              }
              if(discount){
                modal.find('#discount').val(discount);
              }else{
                modal.find('#discount').val(0.0);
              }
              var existencias = modal.find('#existencias tbody');
              existencias.empty();
              $.each(data.existencias, function(key, value){
                var row = $('<tr></tr>').attr('id', value.bodega_id);
                row.append($('<td class="bodega"></td>').html(value.bodega));
                row.append($('<td class="cantidad"></td>').html(value.cantidad));
                if(bodega==value.bodega_id){
                  row.addClass('active');
                  modal.find('#bodega').val(bodega);
                }
                existencias.append(row);
              });
              modal.modal('show');
          }
      });
  }


var select_bodega = function(){
      $('#existencias tbody tr').removeClass('active');
      $(this).addClass('active');
      $('#detalleModal').find('#bodega').val($(this).attr('id'));
}

var insertar_detalle = function(code, name, cantidad, price, discount, total, producto, bodega, bodega_name){
  var tabla = $("#productos tbody");
  try {
    tabla.find('#'+producto).remove();
  } catch (e) {
    console.log(e);
  }
  var row = $('<tr id="'+producto+'"></tr>')
    .append($('<td><input type="text" id="code" class="form-control" value="'+code+'" readonly><input type="hidden" id="producto" name="producto_id" value="'+producto+'" readonly></td>'))
    .append($('<td><input type="text" id="name" class="form-control" value="'+name+'" readonly></td>'))
    .append($('<td><input type="text" id="bodega_name" class="form-control" value="'+bodega_name+'" readonly><input type="hidden" id="bodega" name="bodega_id" value="'+bodega+'" readonly></td>'))
    .append($('<td><input type="text" id="cantidad" name="producto_cantidad" class="form-control" value="'+cantidad+'" readonly></td>'))
    .append($('<td><input type="text" id="price" name="producto_price" class="form-control" value="'+price+'" readonly></td>'))
    .append($('<td><input type="text" id="discount" name="producto_discount" class="form-control" value="'+discount+'" readonly></td>'))
    .append($('<td><input type="text" id="total" class="form-control" value="'+total+'" readonly></td>'));
  tabla.append(row);
  $('#buscador_productos')
    .focus()
    .val('');
}

var limpiar_modal = function(){
  modal = $('#detalleModal input').val('');
}

var validar_modal = function(){
  modal = $('#detalleModal')
  var cantidad = parseFloat(modal.find('#cantidad').val());
  var existencia = parseFloat(modal.find('tr.active').find('.cantidad').html());
  var code = modal.find('#code').val();
  var name = modal.find('#name').val();
  var price = parseFloat(modal.find('#price').val());
  var discount = modal.find('#discount').val();
  var total = ((cantidad * price) - (cantidad * discount)).toFixed(2);
  var producto = modal.find('#producto').val();
  var bodega = modal.find('#bodega').val();
  var bodega_name = modal.find('tr.active').find('.bodega').html();
  var mensaje = ""
  var valido = false;
  if(bodega.length==0){
    valido = false;
    mensaje = "Por favor seleccione una bodega!"
    $('#mensaje')
      .empty()
      .html(mensaje)
      .addClass('alert-danger');
  } else {
    if(cantidad > existencia){
      valido = false;
      mensaje = "La cantidad no puede ser mayor que la existencia!"
      $('#mensaje')
        .empty()
        .html(mensaje)
        .addClass('alert-danger');
    }else{
      $('#mensaje')
        .empty()
        .removeClass('alert-danger');
        valido = true;
    }
  }
  if(valido){
    insertar_detalle(code, name, cantidad, price, discount, total, producto, bodega, bodega_name);
    calcular_factura();
    modal.modal('hide');
    limpiar_modal();
  }

}

var actualizar_detalle = function (){
  var producto = $(this).find('#producto').val();
  var bodega = $(this).find('#bodega').val();
  var cantidad = $(this).find('#cantidad').val();
  var discount = $(this).find('#discount').val();
  load_modal(producto, bodega, cantidad, discount);
}

var totalizar = function(selector){
    var tabla = $('#productos tbody tr');
    var total = 0.0;
    for(var i=0;i<tabla.length;i++){
      var value = tabla[i];
      if($(value).hasClass('invalid')==false){
        total += (parseFloat($(value).find('#cantidad').val())
         * parseFloat($(value).find(selector).val()));
      }
    }
    return total;
}

var calcular_iva = function(subtotal, descuento){
  var total = 0.0;
  if($('#excento_iva').is(':checked')){
    total += 0.0;
  } else {
    total += ((subtotal - descuento)*0.15);
  }
  return total
}

var calcular_retencion = function(subtotal, descuento){
  var total = 0.0;
  var descontado = subtotal-descuento;
  if($('#aplica_ir').is(':checked')&&descontado>1000){
    total += (descontado*0.02);
  }
  if($('#aplica_al').is(':checked')&&descontado>1000){
    total += (descontado*0.01);
  }
  return total
}

var get_descuento = function () {
  if($(this).val().match(/(?:%)$/)) {
    var persent = parseFloat($(this).val().replace('%', ''))/100;
    $(this).val((parseFloat($('#detalleModal').find('#price')
        .val())*persent).toFixed(2));
    }
}

var calcular_factura = function(){
  var subtotal = totalizar('#price');
  var descuento = totalizar('#discount');
  var iva = calcular_iva(subtotal, descuento);
  var retencion = calcular_retencion(subtotal, descuento);
  $('#factura_subtotal').val(subtotal.toFixed(2));
  $('#factura_discount').val(descuento.toFixed(2));
  $('#factura_iva').val(iva.toFixed(2));
  $('#factura_retencion').val(retencion.toFixed(2));
  $('#factura_total').val(((subtotal+iva)-(descuento+retencion)).toFixed(2));
}

var eliminar_detalle = function(){
  var modal = $('#detalleModal');
  var p = modal.find('#producto').val();
  $('#productos tbody').find('#'+p).remove();
  calcular_factura();
  modal.modal('hide');
  limpiar_modal();
}

var grabar_factura = function(){
  var form = $('form');
  $.ajax("/moneycash/grabar_factura/",{
      type: "POST",
      data: form.serialize(),
      success: function(response) {
        console.log(response);
      }
    });
    limpiar_factura();
    $('#mensajes')
      .empty()
      .html('<div class="alert alert-success">Factura Grabada con Exito!</div>');

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

var limpiar_factura = function(){
  limpiar_cliente();
  limpiar_modal();
  $('.datos_totales input').val(0.0);
  $('.datos_factura input, .datos_factura textarea').val("");
  $('#productos tbody').empty();
  $('#mensajes').empty();
}

var funka = function(){
  console.log('funka!');
}

$(document).on('ready', function(){
    $("input").on("focus", function(){$(this).select();});
    $('.datos_cliente #name').on('keyup', complete_cliente);
    $('#buscador_productos').on('keyup', complete_producto);
    $('#existencias tbody').on('click', 'tr', select_bodega);
    $('#modal_ok').on('click', validar_modal);
    $('#modal_delete').on('click', eliminar_detalle);
    $('#productos tbody').on('dblclick', 'tr', actualizar_detalle);
    $('#detalleModal #discount').on('change', get_descuento);
    $('input[type="checkbox"]').on('change', calcular_factura);
    $('#btn_grabar').on('click', grabar_factura);
    $('#btn_borrar').on('click', limpiar_factura);
    $('.datos_cliente').on('click', '#borrar_cliente', limpiar_cliente);
    $('.datos_cliente').on('click', '#editar_cliente', editar_cliente);
});

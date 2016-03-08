$(document).ready(function() {
try {
    $('form').on('submit', function(e) {
        return false;
    });
    $('#id_name, #id_identificacion').on('keyup', function(e) {
        complete_cliente($(this));
    });
    $('#factura_form').on('keyup', '.producto_code', function() {
        complete_producto($(this));
    });
    function get_total(cantidad, precio) {
        return parseFloat(cantidad) * parseFloat(precio);
    }
    function complete_cliente(self) {
        if($.trim($(self).val()) != '') {
            $(self).autocomplete({
                minLength: 2,
                source: "/facturacion/autocomplete_cliente?opt="
                    +$(self).prop('name'),
                select: function(event, ui) {
                    $('#id_code').val(ui.item.obj.code);
                    $('#id_name').val(ui.item.obj.name);
                    $('#id_identificacion').val(ui.item.obj.identificacion);
                    $('#id_telefono').val(ui.item.obj.telefono);
                    $('#id_email').val(ui.item.obj.email);
                    $('#id_direccion').val(ui.item.obj.direccion);
                    $('.grp-collapse-handler').empty().append("<span class='borrar'>X</span>");
                }
            });
        }
    }
    function complete_producto(self) {
        if($.trim($(self).val()) != '') {
            $(self).autocomplete({
                minLength: 2,
                source: "/facturacion/autocomplete_producto",
                select: function(event, ui) {
                    $(self).parents('.grp-tr').find('.producto_cantidad').val(1);
                    $(self).parents('.grp-tr').find('.producto_name').val(ui.item.obj.name);
                    $(self).parents('.grp-tr').find('.producto_precio').val(ui.item.obj.precio);
                    $(self).parents('.grp-tr').find('.producto_descuento').val(0.0);
                    $(self).parents('.grp-tr').find('.producto_iva').val(0.0);
                    $(self).parents('.grp-tr').find('.producto_total').val(get_total(1, ui.item.obj.precio));
                }
            });
        }
    }
} catch (err) {
    console.log(err);
}
});

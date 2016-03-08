$(document).ready(function() {
try {
    var total = 0;
    $('form').on('submit', function(e) {
        return false;
    });
    $('#id_name, #id_identificacion').on('keyup', function(e) {
        complete_cliente($(this));
    });
    $('#factura_form').on('keyup', '.producto_code', function() {
        complete_producto($(this));
    });
    $('.box_cliente').on('mouseover', 'h2 .borrar', function() {
        $('.datos_cliente')
            .css({'text-decoration': 'line-through', 'color': 'red'});
    }).on('mouseout', 'h2 .borrar', function() {
        $('.datos_cliente')
            .css({'text-decoration': 'none', 'color': 'black'});
    }).on('click', 'h2 .borrar', function(e) {
        e.preventDefault;
        borrar('.datos_cliente');
        readonly('.datos_cliente', false);
    });
    $('.grp-table').on('change', '.grp-dynamic-form .cantidad .producto_cantidad'
        , function(e) {
            $(this).parents('.grp-tr')
                .find('.producto_total')
                .val(get_total($(this).val(), $(this).parents('.grp-tr')
                        .find('.producto_precio').val()));
            $('.producto_total').trigger('change');
    });
    $('.grp-table').on('change', '.grp-dynamic-form .total .producto_total'
        , function(e) {
        $('#id_subtotal').val(parseFloat($('#id_subtotal').val())+parseFloat($(this).val()));
    });
    function get_total(cantidad, precio) {
        return parseFloat(cantidad) * parseFloat(precio);
    }
    /*function get_sub_total(clase) {
        var tmp = 0;
        $(clase).each(function(key, value) {
            tmp += parseFloat(value);
            if(key == ($(clase).length -1)) {
                return tmp;
            }
        });
    }*/
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
                    $('.box_cliente .grp-collapse-handler').empty().append("Datos del Cliente<span class='borrar'>X</span>");
                    readonly('.datos_cliente', true);
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
                    $('.producto_total').trigger('change');
                }
            });
        }
    }
    function borrar(clase) {
        $(clase).val('');
    }
    function readonly(clase, option) {
        $(clase).prop('readonly', option);
    }
} catch (err) {
    console.log(err);
}
});

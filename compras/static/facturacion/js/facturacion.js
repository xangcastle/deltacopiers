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
    })
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
        $('.datos_cliente')
            .css({'text-decoration': 'none', 'color': 'black'});
        $('span.borrar').remove();
    });
    $('.grp-table').on('change', '.grp-dynamic-form .cantidad .producto_cantidad'
        , function(e) {
            $(this).parents('.grp-tr')
                .find('.producto_total')
                .val(get_total($(this).val(), $(this).parents('.grp-tr')
                        .find('.producto_precio').val())).change();
            get_descuento($(this));
    });
    $('.grp-table').on('change', '.grp-dynamic-form .grp-td input[type="text"].producto_total'
        , function() {
            if($(this).val().trim() != '') {
                get_sub_total('.grp-dynamic-form .grp-td input[type="text"].producto_cantidad');
            }
    });
    $('.grp-dynamic-form .grp-td input[type="text"].producto_total')
        .trigger('change');
    $('.grp-table').on('change', '.grp-dynamic-form .grp-td input[type="text"].producto_descuento'
        , function(e) {
            get_descuento($(this));
    });
    $('#id_aplica_iva').on('change', function() {
        get_sub_total('.grp-dynamic-form .grp-td input[type="text"].producto_cantidad');
    });
    $('#id_aplica_ir').on('change', function() {
        get_sub_total('.grp-dynamic-form .grp-td input[type="text"].producto_cantidad');
    });
    $('#id_aplica_al').on('change', function() {
        get_sub_total('.grp-dynamic-form .grp-td input[type="text"].producto_cantidad');
    });
    $('.grp-table').on('click'
        , '.grp-dynamic-form .grp-td .grp-tools .grp-remove-handler'
        , function(e) {
            console.log('ddda');
            //get_sub_total('.grp-dynamic-form .grp-td input[type="text"].producto_cantidad');
    });
    function get_descuento(self) {
        if($(self).parents('.grp-tr')
            .find('input[type="text"].producto_precio').val() != '') {
            if($(self).val().match(/(?:%)$/)) {
                var persent = parseFloat($(self).val().replace('%', ''))/100;
                $(self).val(parseFloat($(self).parents('.grp-tr')
                    .find('input[type="text"].producto_precio').val()*persent).toFixed(2))
            }
            var iva = (($(self).parents('.grp-tr').find('input[type="text"].producto_precio').val()-
                        $(self).parents('.grp-tr').find('input[type="text"].producto_descuento').val())*0.15);
            $(self).parents('.grp-tr').find('input[type="text"].producto_iva').val(iva);
            get_sub_total('.grp-dynamic-form .grp-td input[type="text"].producto_cantidad');
        }
    }
    function get_total(cantidad, precio) {
        return (parseFloat(cantidad) * parseFloat(precio)).toFixed(2);
    }
    function get_sub_total(clase) {
        var subtotal = 0, iva = 0
            , descuento = 0, total = 0;
        if($(clase).length > 0) {
            $(clase).each(function(key, value) {
                if($(value).parents('.grp-tr').find('input[type="text"].producto_total').val() != '') {
                    subtotal += parseFloat($(value)
                                    .parents('.grp-tr')
                                    .find('input[type="text"].producto_total').val());
                    if($('#id_aplica_iva').is(':checked')) {
                        iva += (parseFloat($(value)
                                        .parents('.grp-tr')
                                        .find('input[type="text"].producto_iva').val())*
                                        parseFloat($(value).parents('.grp-tr')
                                            .find('input[type="text"].producto_cantidad').val()));
                    } else {
                        iva = 0.00;
                    }
                    descuento += (parseFloat($(value)
                                    .parents('.grp-tr')
                                    .find('input[type="text"].producto_descuento').val())*
                                        parseFloat($(value).parents('.grp-tr')
                                            .find('input[type="text"].producto_cantidad').val()));
                    if(key == ($(clase).length -1)) {
                        var ir = 0.00, al = 0.00;
                        total = ((subtotal-descuento)+iva);
                        $('#id_subtotal').val(subtotal.toFixed(2));
                        $('#id_descuento').val(descuento.toFixed(2));
                        $('#id_iva').val(iva.toFixed(2));
                        if($('#id_aplica_ir').is(':checked')) {
                            ir = (subtotal-descuento)*0.02;
                        }
                        if($('#id_aplica_al').is(':checked')) {
                            al = (subtotal-descuento)*0.01;
                        }
                        $('#id_al').val(al.toFixed(2));
                        $('#id_ir').val(ir.toFixed(2));
                        $('#id_total').val(((total-ir)-al).toFixed(2));
                    }
                }
            });
        } else {
            $('#id_subtotal').val('0');
            $('#id_descuento').val('0');
            $('#id_iva').val('0');
            $('#id_total').val('0');
        }
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
                    $('.box_cliente .grp-collapse-handler')
                        .empty()
                        .append("Datos del Cliente<span class='borrar'>X</span>");
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
                    var iva = parseFloat((ui.item.obj.precio-0)*0.15);
                    $(self).parents('.grp-tr').find('.producto_cantidad').val(1);
                    $(self).parents('.grp-tr').find('.producto_name').val(ui.item.obj.name);
                    $(self).parents('.grp-tr').find('.producto_precio').val(ui.item.obj.precio);
                    $(self).parents('.grp-tr').find('.producto_descuento').val(0.0);
                    $(self).parents('.grp-tr').find('.producto_iva').val(iva.toFixed(2));
                    $(self).parents('.grp-tr')
                        .find('.producto_total')
                        .val(get_total(1, ui.item.obj.precio)).change();
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

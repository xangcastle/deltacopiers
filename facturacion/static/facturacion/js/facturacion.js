$(document).ready(function() {
    $('form').on('submit', function(e) {
        return false;
    });
    $('#id_name').on('keyup', function(e) {
        complete_cliente($(this));
    });
    $('#id_identificacion').on('keyup', function(e) {
        complete_cliente($(this));
    });
    $('#factura_form').on('keyup', '.form-row .code .vTextField', function() {
        complete_producto($(this));
    });
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
                }
            });
        }
    }
    function complete_producto(self) {
        if($.trim($(self).val()) != '') {
            var index = $(this).parents('.grp-dynamic-form').index();
            $(self).autocomplete({
                minLength: 2,
                source: "/facturacion/autocomplete_producto",
                select: function(event, ui) {
                    console.log(ui);
                    /*$('#id_code').val(ui.item.obj.code);
                    $('#id_name').val(ui.item.obj.name);
                    $('#id_identificacion').val(ui.item.obj.identificacion);
                    $('#id_telefono').val(ui.item.obj.telefono);
                    $('#id_email').val(ui.item.obj.email);
                    $('#id_direccion').val(ui.item.obj.direccion);*/
                }
            });
        }
    }
});

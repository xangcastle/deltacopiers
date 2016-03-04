$(document).ready(function() {
    $('form').on('submit', function(e) {
        return false;
    });
    /*$('#id_name').on('keyup', function(e) {
        complete_cliente($(this));
    });
    $('#id_identificacion').on('keyup', function(e) {
        complete_cliente($(this));
    });*/
    $('.buscar_cliente').on('keyup', function(e) {
        complete_cliente($(this));
    });
    function complete_cliente(self) {
        var url = "/facturacion/autocomplete_cliente?opt="+$(self).prop('name');
        $(self).autocomplete({
            minLength: 2,
            source: url,
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
});

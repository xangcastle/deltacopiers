$(document).ready(function() {
    $('form').on('submit', function(e) {
        return false;
    });
    $('#id_name').on('keyup', function(e) {
        complete_usario($(this));
    });
    $('#id_identificacion').on('keyup', function(e) {
        complete_usario($(this));
    });
    function complete_usario(self) {
        var url = "/facturacion/autocomplete_cliente";
        if($(self).prop('id') == 'id_name')
            url +="?opt=name";
        else
            url +="?opt=code";
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

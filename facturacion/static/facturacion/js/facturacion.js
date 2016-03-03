$(document).ready(function(){


    $( document ).ready(function() {
        $('#id_name,#id_identificacion').each(function()
                                                                {
                                                                    $(this).autocomplete({
                                                                        minLength: 2,
                                                                        source: "{% url 'autocomplete_cliente' %}",
                                                                        select: function( event, ui ) {
                                                                            $('#id_code').val(ui.item.obj.code);
                                                                            $('#id_name').val(ui.item.obj.name);
                                                                            $('#id_identificacion').val(ui.item.obj.identificacion);
                                                                            $('#id_telefono').val(ui.item.obj.telefono);
                                                                            $('#id_email').val(ui.item.obj.email);
                                                                            $('#id_direccion').val(ui.item.obj.direccion);
                                                                        }
                                                                    });
                                                                }
                                                               );
    });
});
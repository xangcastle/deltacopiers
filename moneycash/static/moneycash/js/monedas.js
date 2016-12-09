var cordobizar = function(dolares){
  tc = parseFloat($('#tc').val());
  return (parseFloat(dolares) * tc).toFixed(2);
}

var dolarizar = function(cordobas){
  tc = parseFloat($('#tc').val());
  return (parseFloat(cordobas) / tc).toFixed(2);
}

var cordobizar_documento = function(){
  var monedas = $('.moneda');
  $.each(monedas, function(i,o){
    if ($(o).val()=="") {

      var monto = $(o).html();
      if ($('select[name="monedas"]').val()=="cordobas") {
        $(o).html(cordobizar(monto));
      }else {
        $(o).html(dolarizar(monto));
      }

    }else {

      var monto = $(o).val();
      if ($('select[name="monedas"]').val()=="cordobas") {
        $(o).val(cordobizar(monto));
      }else {
        $(o).val(dolarizar(monto));
      }

    }
    console.log(o);
    console.log(monto);
  });
}

$(document).ready(function(){
  $('select[name="monedas"]').on('change', cordobizar_documento);
});

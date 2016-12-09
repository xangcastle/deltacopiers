var cordobizar = function(dolares){
  tc = parseFloat($('#tc').val());
  return (parseFloat(dolares) * tc).toFixed(2);
}

var dolarizar = function(cordobas){
  tc = parseFloat($('#tc').val());
  return (parseFloat(cordobas) / tc).toFixed(2);
}

var cordobizar_documento = function(){
  $.each($('.moneda'), function(i,o){
    var monto = $(o).val()
    if ($('select[name="monedas"]').val()=="cordobas") {
      $(o).val(cordobizar(monto));
    }else {
      $(o).val(dolarizar(monto));
    }
  });
}

$(document).ready(function(){
  $('select[name="monedas"]').on('change', cordobizar_documento);
});

$(function(){
        $('.i-d-quantity').incrementBox({minVal:0,maxVal:999999});
        });
(function($){

        $.fn.extend({
            incrementBox: function(options) {

                var defaults = {
                    minVal:null,
                    maxVal:null,
                    incButton:'.inc',
                    decButton:'.dec'
                }

                var getNumVal = function($element){//get numeric value of an object
                                  var value = Number($element.val());
                                  return isNaN(value) ? 0 : value;
                                }
                var correctValue = function(min, max, value){
                  var checkMin = min!=null && !isNaN(0+min);
                  var checkMax = max!=null && !isNaN(0+max);
                  if(value>max && checkMax){
                    return max;
                  }
                  if(value<min && checkMin){
                    return min;
                  }
                  return value;
                }

                var options =  $.extend(defaults, options);

                return this.each(function() {
                    var o = options;
                    var $obj = $(this);
                      $(o.incButton).click(function(){                       
                        $obj.val( correctValue(o.minVal, o.maxVal, (getNumVal($obj) + 1)) );
                      });
                      $(o.decButton).click(function(){                               
                        $obj.val( correctValue(o.minVal, o.maxVal, (getNumVal($obj) - 1)) );
                      });
                      $obj.blur(function(){
                        $obj.val( correctValue(o.minVal, o.maxVal, getNumVal($obj)) );
                      });                   
                });
            }
        });

    })(jQuery);




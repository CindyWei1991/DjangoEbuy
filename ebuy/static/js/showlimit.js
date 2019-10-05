$(function() {
  $.fn.showlimit=function(){
    return $(this).each(function(index,elem){
        $(elem).keyup(function () {
            var $me = $(this)
            maxlength = parseInt($me.attr("maxlength"),10)
            charCount = $me.val().length;
            if (charCount!=0){
                $(this).siblings(".fielderror").hide();
            }
            $counter = $me.siblings('.limit');
            $counter.text('limit:'+maxlength +'characters. remaining: ' + (maxlength - charCount))
        });
    });
  };
});
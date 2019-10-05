$(document).ready(function(){
  $("body").on("click","button.change",function(){
      // alert($(this).attr('id'));
      var id = $(this).closest("td").attr('id');
      var curr_amount = $("#demo"+id).text(); 
      $("#quantityArea"+id).html("<p><input type=\"number\" min=\"1\" step=\"1\" id=\"test3"+id + "\" ></p>");
      $("#test3"+id).val(curr_amount);
      $("#quantityArea"+id).append("<button type=\"button\" class=\"btn btn-default save\" id = \"saveAmount"+id +"\">save</button>");
  });

  function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
              // Only send the token to relative URLs i.e. locally.
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
      }
  });

  $("body").on("click","button.save",function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var id = $(this).closest("td").attr('id');
      var title = $("#title"+id).text();
      var curr_amount = $("#test3"+id).val();
      var availNow = $("#avail"+id).val();
      if (parseInt(availNow) < parseInt(curr_amount)) {
        $("#error"+id).text("Sorry! We have only "+availNow + " item(s) available now!");
      } else if (parseInt(curr_amount) <= 0) {
        $("#error"+id).text("Please enter positive integer!");
      } else {
      $("#error"+id).text("");
      $("#saveAmount"+id).remove();
      $("#cancel"+id).remove();
      $("#test3"+id).remove();
      $("#quantityArea"+id).append("<h5 id=\"demo"+id+"\">"+curr_amount+"</h5>");
      $("#quantityArea"+id).append("<button type=\"button\" class=\"btn btn-default change\" id = \"change"+id+"\">change</button>");
      var data = {"productTitle":title, "newAmount": curr_amount};
      $.post("/ebuy/updatebag/"+id, data);
      location.reload();
      }
  });
});
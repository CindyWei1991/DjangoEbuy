$(document).ready(function(){
    $("#amountInput").keyup(function(){
      var inputV = parseInt($("#amountInput").val());
      var currV = parseInt($("#currAmount").text());
       if (inputV > currV) {
        $("#addbag").prop("disabled", true);
      } else if (inputV <= 0) {
        $("#addbag").prop("disabled", true);
      } else {
        $("#addbag").prop("disabled", false);
      }
    });
    $("#amountInput").click(function(){
      var inputV = parseInt($("#amountInput").val());
      var currV = parseInt($("#currAmount").text());
       if (inputV > currV) {
        $("#addbag").prop("disabled", true);
      } else if (inputV <= 0) {
        $("#addbag").prop("disabled", true);
      } else {
        $("#addbag").prop("disabled", false);
      }
    });
});
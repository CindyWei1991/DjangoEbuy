$(function() {
    // IMPORTANT: Fill in your client key
    var clientKey = "js-Yqdynxe0z5Td6MciCrRaGphHEBiZCDzB4M9rjnrTtl6z7iRJKIUq8b7MMqMp4l08";
    var shops = ["15237", "15213"];
    var cache = {};
    var container = $("#zipMSG");
    var errorDiv = container.find("div.text-error");
    
    var result = [];
    
    /** Handle successful response */
    function handleResp(data)
    {
      var zipcode1 = $("input[name='zipcode1']").val().substring(0, 5);
      var shop1 = "15237";
      var shop2 = "15213";
      // Check for error
      if (data.error_msg)
        errorDiv.text(data.error_msg);

      else if (data.length ==1) {
        if (zipcode1 == shop1) {
        errorDiv.text("You are close to Ross Park mall.");
        } else if (zipcode1 == shop2) {
        errorDiv.text("You are close to Centre Avenue mall.");
        } else {
        container.find("div.distance").show()
        // Set distance
        .text("No stores were found in your search area. \
          Please adjust your search and try again.");
        }
      } else if (data.length ==2){
        if (data[0].zip_code2 == shops[0])
          container.find("div.distance").show()
        // Set distance
        .html("<div class='radio'><label><input type='radio' name='optradio'>Ross Park("+data[0].distance+" miles)</label></div>");
        else if (data[0].zip_code2 == shops[1])
          container.find("div.distance").show()
        // Set distance
        .html("<div class='radio'><label><input type='radio' name='optradio'>Ross Park("+data[1].distance+" miles)</label></div>");
      } else if (data.length ==3) {
        container.find("div.distance").show()
        // Set distance
        .html("<div class='radio'><label><input type='radio' name='optradio'>Ross Park("+data[0].distance+" miles)</label></div><div class='radio'><label><input type='radio' name='optradio'>Centre Ave("+data[1].distance+" miles)</label></div>")
      }
    }
    
    // Set up event handlers
    container.find("input[name='zipcode1'],select[name='selDist']").on("keyup change", function() {
      var e = document.getElementById("sel1");
      var dist = e.options[e.selectedIndex].text;
      // Get zip code
      var zipcode1 = $("input[name='zipcode1']").val().substring(0, 5);
      var shop1 = "15237";
      var shop2 = "15213";
      var zip_codes = zipcode1 + "," + shop1 + "," + shop2;
      
      if (zipcode1.length == 5 && /^[0-9]+$/.test(zipcode1))
      {
        // Clear error
        errorDiv.empty();
        
          // Build url
          var url = "https://www.zipcodeapi.com/rest/"+clientKey+"/match-close.json/" + zip_codes + "/" + dist + "/mile";
          
          // Make AJAX request
          $.ajax({
            "url": url,
            "dataType": "json"
          }).done(function(data) {
            handleResp(data);
          }).fail(function(data) {
            if (data.responseText && (json = $.parseJSON(data.responseText)))
            {
              // Check for error
              if (json.error_msg)
                errorDiv.text(json.error_msg);
            }
            else
              errorDiv.text('Request failed.');
          });
      }
    }).trigger("change");
  });
var position1=new google.maps.LatLng(40.543676, -80.007708);
var position2 = new google.maps.LatLng(40.453795, -79.945438);
var middle =new google.maps.LatLng(40.4987355, -79.976573);
function initialize()
{
var mapProp = {
  center:middle,
  zoom:10,
  mapTypeId:google.maps.MapTypeId.ROADMAP
  };

var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

var marker=new google.maps.Marker({
  position:position1,
  });


var marker2 = new google.maps.Marker({
  position:position2,
})

marker.setMap(map);
marker2.setMap(map);
}

google.maps.event.addDomListener(window, 'load', initialize);
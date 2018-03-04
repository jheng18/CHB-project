var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('googlemaps'), {
        zoom: 13,
        center: new google.maps.LatLng(41.787163518,-87.593164294),
        mapTypeId: 'roadmap'
    });
    var script = document.createElement('script');

    script.src = 'route1.js';
    document.getElementsByTagName('head')[0].appendChild(script);
    }

window.eqfeed_callback = function(results) {
    for (var i = 0; i < results.features.length; i++) {
        var coords = results.features[i].geometry.location;
        var latLng = new google.maps.LatLng(coords[0],coords[1]);
        var marker = new google.maps.Marker({
            position: latLng,
            map: map
        });
    }
}
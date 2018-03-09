// Reference:
// https:developers.google.com/maps/documentation/javascript/earthquakes?hl=zh-cn
var map, heatmap;
function initMap() {
    map = new google.maps.Map(document.getElementById('googlemaps'), {
        zoom: 13.35,
        center: new google.maps.LatLng(41.792163518,-87.593164294),
        mapTypeId: 'roadmap'
    });

    var script = document.createElement('script');
    script.src = "{% static "visual_crime/route1.js" %}";
    document.getElementsByTagName('head')[0].appendChild(script);
}

function eqfeed_callback(results) {
    var heatmapData = [];
    for (var i = 0; i < results.features.length; i++) {
        var coords = results.features[i].geometry.location;
        var latLng = new google.maps.LatLng(coords[0], coords[1]);
        heatmapData.push(latLng);
    }
    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: map,
        radius: 16
    });
}

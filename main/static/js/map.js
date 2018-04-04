var map; // Google Maps map
var startMarker; // Google Maps Start maerker
var poly; // Google Maps polyline

function initMap() {
    var uluru = {lat: -25.363, lng: 131.044};

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: uluru
    });

    poly = new google.maps.Polyline({
        strokeColor: '#222222',
        strokeOpacity: 1,
        strokeWeight: 3,
        map: map
    });
}

function drawPolyline(googlePolyline) {

    if (googlePolyline != '') {
        let LatLngs = google.maps.geometry.encoding.decodePath(googlePolyline);
        var path = poly.getPath();

        LatLngs.forEach(function(e) {
            path.push(e);
        });
    
        map.setCenter(LatLngs[0]);
    
        startMarker = new google.maps.Marker({
            position: LatLngs[0],
            map: map
        });
    }
}
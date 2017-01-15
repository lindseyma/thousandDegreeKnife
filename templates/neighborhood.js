

var data = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "fillColor": "blue"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-73.98779153823898, 40.718233223261],
                    [-74.004946447098, 40.723575517498],
                    [-74.006771211624, 40.730592217474],
                    [-73.99010896682698, 40.746712376146],
                    [-73.973135948181, 40.73974615047701],
                    [-73.975120782852, 40.736128627654],
                    [-73.973997695541, 40.730787341083],
                    [-73.983317613602, 40.716639396436],
                    [-73.98779153823898, 40.718233223261]
                ]
            ]
        }
    }
    ]
};

var n1 = new google.maps.Polygon({
    paths: data.features.type.coordinates,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 3,
    fillColor: '#FF0000',
    fillOpacity: 0.35



})
n1.setMap(map);

        /*
      
    var mapProp = {
        center: new google.maps.LatLng(40.7128, -74.0059),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    

    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    map.data.addGeoJson(data);
    map.data.setStyle(function (feature) {
        var color = feature.getProperty('fillColor');
        return {
            fillColor: color,
            strokeWeight: 1
        }
    });

google.maps.event.addDomListener(window, 'load', initialize);
*/
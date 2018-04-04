var polyline = document.querySelector("meta[name=polyline]").content;

var JSONPolyline;
$.getJSON("http://localhost:8000/api/rides", function(data) {
        
    let activity = JSON.parse(data.activities[0]);
    drawPolyline(activity.polyline);
});
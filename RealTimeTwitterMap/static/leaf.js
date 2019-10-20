// from leaflet documentation
// id from index.html should be the same id here as well
// lat long and zoom factor, 13 is super zoomed in, and since tweets are
// worldwide, we use 1


var mymap = L.map('mapid').setView([51.512, -0.104], 1);

// using OSM for me

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	maxZoom: 18,
}).addTo(mymap);

// defining source of data , i.e, events, from our topic

var source = new EventSource('/topic/tweets1');

// a listener to keep the events open and continous
// here we can code in what happens to the incoming data, and what is shown
//// on map. listener recieves events in e.

source.addEventListener('message', function(e){
// events are translated to JSON format
    obj = text.parse(e.new);
//console recieves a log
    console.log(obj);
//using JSON, we define lat, long, and other info to be shown when,
// marker is clicked on.
    lat = obj.place.bounding_box.coordinates[0][0][1];
    long = obj.place.bounding_box.coordinates[0][0][0];
    username = obj.user.name;
    tweet = obj.text;
		sentiment = obj.senti;
// a typical default marker to pinpoint the place, and show elements when
//mouse moves over it
    marker = L.marker([lat,long],).addTo(mymap).bindPopup('Username: <strong>' + username + '</strong><br>Sentiment: <strong>' + sentiment + '</strong><br>Tweet: <strong>' + tweet + '</strong><br>');

}, false);

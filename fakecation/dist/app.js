var Latlong = [];
var UploadedFile = {};

document.body.onload = function main() {
  loadMap();
  loadFilePond();

  var confirmButton = document.querySelector("#confirm-button");
  confirmButton.addEventListener("click", confirmButtonHandler, false);
}

function loadMap() {
  var mymap = L.map('mapid').setView([40, -0.33], 2);
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'
  }).addTo(mymap);

  var markers = []

  function createMarker(coords) {
    var id;
    if (markers.length < 1) id = 0;
    else id = markers[markers.length - 1]._id + 1;

    myMarker = L.marker(coords, {
      draggable: false
    });
    myMarker._id = id;

    let btn = document.createElement('button');
    btn.innerText = 'Delete Marker';
    btn.onclick = function () {
      var new_markers = [];
      markers.forEach(function (marker) {
        if (marker._id == id) mymap.removeLayer(marker)
        else new_markers.push(marker)
      });
      markers = new_markers;
      Latlong.forEach(function () {
        var index = Latlong.indexOf(coords);
        if (index > -1) {
          Latlong.splice(index, 1);
        }
      });
    }

    myMarker.bindPopup(btn).openPopup();

    mymap.addLayer(myMarker);
    markers.push(myMarker);
    Latlong.push(coords);
    if (markers.length > 5) {
      mymap.removeLayer(markers[0]);
      markers.splice(0, 1);
      Latlong.splice(0, 1);
    }
  }

  function onMapClick(e) {
    createMarker(e.latlng)
    console.log("New marker at: " + e.latlng);
  }
  mymap.on('click', onMapClick);
}

function loadFilePond() {
  var inputElement = document.querySelector('#filepond');
  var pond = FilePond.create(inputElement);

  pond.on('addfile', (error, file) => {
    if (error) {
      console.log('Oh no');
      return;
    }
    if (file) {
      console.log("File uploaded:", file.file.name);
      UploadedFile = file;
    }
  });

  pond.setOptions({
    maxFiles: 1,
    required: true,
  });
}

function confirmButtonHandler() {
  if (Object.keys(Latlong).length === 0 || Object.keys(UploadedFile).length === 0) {
    console.log("Complete your shit boi");
    console.log(Latlong);
    console.log(UploadedFile);
    return;
  }
  console.log("Data confirmed:");
  console.log(Latlong);
  console.log(UploadedFile);
}



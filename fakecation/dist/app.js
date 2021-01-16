var Latlong = {};
var UploadedFile = {};

document.body.onload = function main() {
  loadMap();
  loadFilePond();

  var button = document.querySelector("#confirm-button");
  button.addEventListener("click", confirmButtonHandler, false);
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
  var popup = L.popup();

  function onMapClick(e) {
    popup
      .setLatLng(e.latlng)
      .setContent("Fake your vacation here!")
      .openOn(mymap);
    Latlong = e.latlng;
    console.log("Location selected: ", Latlong);
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
    required: true
  });
}

function confirmButtonHandler() {
  if (Object.keys(Latlong).length === 0 || Object.keys(UploadedFile).length === 0) {
    console.log("Complete your shit boi");
    return;
  }
  console.log("Data confirmed:");
  console.log(Latlong);
  console.log(UploadedFile);
}
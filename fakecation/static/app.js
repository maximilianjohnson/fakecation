var Latlong = {};
var UserImage = {};


document.body.onload = function main() {
  loadMap();
  loadFilePond();

  var confirmButton = document.querySelector("#confirm-button");
  confirmButton.addEventListener("click", confirmButtonHandler, false);
}

function confirmButtonHandler() {
  if (Object.keys(Latlong).length === 0 || Object.keys(UserImage).length === 0) {
    alert("Enter your location and upload a photo!")
    return;
  }
  console.log("Data confirmed:");
  console.log(Latlong);
  console.log(UserImage);
}

function loadMap() {
  // initializing map
  var mymap = L.map('mapid').setView([40, -0.33], 2);
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'
  }).addTo(mymap);

  // initializing popup and click event on map
  var popup = L.popup();
  function onMapClick(e) {
    popup
      .setLatLng(e.latlng)
      .setContent("Fake your vacation here!")
      .openOn(mymap);
    Latlong = e.latlng;
    console.log("New location added: " + Latlong);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/latlong");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      if (xhr.status == 200) {
        console.log("Request success");
        console.log(xhr.responseText);
      }
    }
    xhr.onabort = function () {
      console.log("Request aborted");
    }
    xhr.timeout = 2000;
    xhr.ontimeout = function () {
      console.log("Request timeout");
    }
    xhr.onerror = function () {
      console.log("Error with request");
    }
    xhr.send(JSON.stringify(Latlong));
  }

  mymap.on('click', onMapClick);
}

function getDbJson() {
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/latlong");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      if (xhr.status == 200) {
        console.log("Request success");
        resolve(xhr.responseText);
      }
    }
    xhr.onabort = function () {
      reject("Request aborted");
    }
    xhr.timeout = 2000;
    xhr.ontimeout = function () {
      reject("Request timeout");
    }
    xhr.onerror = function () {
      reject("Error with request");
    }
    xhr.send(JSON.stringify(Latlong));
  })
}

function loadFilePond() {
  FilePond.registerPlugin(FilePondPluginImagePreview);
  var inputElement = document.querySelector('#filepond');
  var pond = FilePond.create(inputElement, {
    imagePreviewMaxHeight: 100,
  });

  pond.on('addfile', (error, file) => {
    if (error) {
      console.log('Oh no');
      return;
    }
    if (file) {
      console.log("File uploaded:", file.file.name);
      UserImage = file;
    }
  });

  pond.setOptions({
    maxFiles: 1,
    required: true,
    server: 'api/'
  });
}






//For selecting multiple locations

// var markers = []

// function createMarker(coords) {
//   var id;
//   if (markers.length < 1) id = 0;
//   else id = markers[markers.length - 1]._id + 1;

//   myMarker = L.marker(coords, {
//     draggable: false
//   });
//   myMarker._id = id;

//   let btn = document.createElement('button');
//   btn.setAttribute("id", "delete-marker");
//   btn.innerText = 'Delete Marker';
//   btn.onclick = function () {
//     var new_markers = [];
//     markers.forEach(function (marker) {
//       if (marker._id == id) mymap.removeLayer(marker)
//       else new_markers.push(marker)
//     });
//     markers = new_markers;
//     Latlong.forEach(function () {
//       var index = Latlong.indexOf(coords);
//       if (index > -1) {
//         Latlong.splice(index, 1);
//       }
//     });
//     console.log("Marker removed at: " + coords);
//   }

//   myMarker.bindPopup(btn).openPopup();

//   mymap.addLayer(myMarker);
//   markers.push(myMarker);
//   Latlong.push(coords);
//   if (markers.length > 5) {
//     mymap.removeLayer(markers[0]);
//     markers.splice(0, 1);
//     Latlong.splice(0, 1);
//   }
// }

//   function onMapClick(e) {
//     createMarker(e.latlng)
//     console.log("New marker at: " + e.latlng);
//   }
//   mymap.on('click', onMapClick);
// }

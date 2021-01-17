var imageIndex = 0;

document.body.onload = function main() {
  sendBaseImage();
  usernameSelector();
  updateLocation();


  var resetButton = document.querySelector("#reset-button");
  resetButton.addEventListener("click", resetButtonHandler, false);

  var newImageHander = document.querySelector("#new-image-button");
  newImageHander.addEventListener("click", newImageHandler, false);
}

function newImageHandler() {
  imageIndex++;
  sendBaseImage();
}

function usernameSelector() {
  var usernameList = [
    "travelmonkey123",
    "live_laugh_love",
    "born2fly",
    "_sandybech",
    "r0undthew0rld",
    "couchsurfer69",
    "passport.prince",
    "i_love_barthelona",
    "bluewater.whitebeach",
    "tattoos_in_thailand",
    "wanderlusty4lyfe"
  ];
  var username = usernameList[Math.floor(Math.random() * usernameList.length)];
  var element = document.querySelector("#instagram-username");
  element.innerText = username;
}

function updateLocation() {
  var element = document.querySelector("#instagram-location");
  getDbJson().then((json) => {
    element.innerText = json[imageIndex].city_name;
  })
}

function sendBaseImage() {
  getDbJson().then((json) => {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/deepfake");
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
    xhr.send(JSON.stringify(json[imageIndex].filepath));
  });
}

function getDbJson() {
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/results/images");
    xhr.onload = function () {
      if (xhr.status == 200) {
        console.log("Request success");
        resolve(JSON.parse(xhr.responseText));
      }
    }
    xhr.onabort = function () {
      reject("Request aborted");
    }
    xhr.timeout = 200;
    xhr.ontimeout = function () {
      reject("Request timeout");
    }
    xhr.onerror = function () {
      reject("Error with request");
    }
    xhr.send();
  })
}




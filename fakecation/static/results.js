document.body.onload = function main() {
  updateInstagramImage();
  usernameSelector();

  var resetButton = document.querySelector("#reset-button");
  resetButton.addEventListener("click", resetButtonHandler, false);

  var newImageHander = document.querySelector("#new-image-button");
  newImageHander.addEventListener("click", newImageHandler, false);
}

function resetButtonHandler() {

}

function newImageHandler() {

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
  var location
  var element = document.querySelector("#instagram-location");
  element.innerText = location;
}

function updateInstagramImage() {
  var image = document.querySelector("#instagram-image");
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/results/images");
  xhr.onload = function () {
    if (xhr.status == 200) {
      console.log(xhr.responseText);
      console.log("Request success");
    }
  }
  xhr.onabort = function () {
    console.log("Request aborted");
  }
  xhr.timeout = 200;
  xhr.ontimeout = function () {
    console.log("Request timeout");
  }
  xhr.onerror = function () {
    console.log("Error with request");
  }
  xhr.send();
}




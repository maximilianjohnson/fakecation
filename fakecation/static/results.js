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
}




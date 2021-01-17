document.body.onload = function main() {
  updateInstagramImage();

  var resetButton = document.querySelector("#reset-button");
  resetButton.addEventListener("click", resetButtonHandler, false);

  var newImageHander = document.querySelector("#new-image-button");
  newImageHander.addEventListener("click", newImageHandler, false);
}

function resetButtonHandler() {
  Latlong = {};
  UserImage = {};

  //get request to index
}

function newImageHandler() {

}

function updateInstagramImage() {
  var image = document.querySelector("#instagram-image");
  console.log(image);
}




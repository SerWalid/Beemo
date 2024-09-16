var $random = $("#random");

// Array of image filenames in the static/images/images_painting folder
var images = [
  '1.jpg',
  '2.png',
  '3.png',
  '4.jpg' // Add more image filenames as needed
];

// Function to get a random image filename from the array
function getRandomImage() {
  return images[Math.floor(Math.random() * images.length)];
}

// Click event for the random image
$(document).ready(function() {
  $random.click(function() {
    // always reset pokeball as image
    $random.attr("src", "https://res.cloudinary.com/beumsk/image/upload/v1506068916/pokeball.png").css("padding","0");

    // start animation
    $random.addClass("animated");
    setTimeout(function() {
      // replace image with one random image from static folder after the animation (1s length)
      $random.attr('src', baseUrl + getRandomImage());
      $random.removeClass("animated").css("padding", "10px");
      $random.fadeTo(0, 0.2).fadeTo(1000, 1);
    }, 1000);
  });
});

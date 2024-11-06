// Select the elements
const imageDiv = document.querySelector('#image');
const previewImages = document.querySelectorAll('.preview');
const undoButton = document.querySelector('#undo');

// Initial state for undo functionality
const originalText = "Hover over an image below to display here.";
const originalBackground = ''; // Set to an empty background or an original image URL

// Event listener for hover effect
previewImages.forEach(pic => {
  pic.addEventListener('mouseover', function() {
    // Logging the image source and alt text to check if it's triggering correctly
    console.log("Image hovered:", this.src);
    console.log("Image alt text:", this.alt);
    
    // Change the text and background image of the #image div
    imageDiv.textContent = this.alt;  // Display the alt text as the content
    imageDiv.style.backgroundImage = `url(${this.src})`;  // Set the background image of the div
  });
});

// Undo functionality to reset the #image div to its original state
undoButton.addEventListener('click', function() {
  console.log("Undo triggered");

  // Reset the background image and text
  imageDiv.style.backgroundImage = `url(${originalBackground})`;
  imageDiv.textContent = originalText;

  // You can also add console.log() to check that the undo is working properly
  console.log("Reset image background and text");
});

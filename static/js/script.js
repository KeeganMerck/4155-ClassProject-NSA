var selectedImage1Input = document.getElementById("selected_image1");
var selectedImage2Input = document.getElementById("selected_image2");
var selectedImages = [];

function toggleSelection(imageId) {
    if (selectedImages.includes(imageId)) {
        // Image is already selected, unselect it
        var index = selectedImages.indexOf(imageId);
        selectedImages.splice(index, 1);
        document.getElementById(imageId).style.border = "3px solid transparent"; // Remove border
    } else if (selectedImages.length < 2) {
        // Image is not selected, select it
        selectedImages.push(imageId);
        document.getElementById(imageId).style.border = "3px solid red"; // Highlight the selected image
    }

    updateSelectedInputs();
}

function updateSelectedInputs() {
    selectedImage1Input.value = selectedImages[0] || '';
    selectedImage2Input.value = selectedImages[1] || '';
}
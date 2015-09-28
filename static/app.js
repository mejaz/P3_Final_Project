function readMyURL(image) {
	var myImage = new FileReader();

	myImage.onload = function(e) {
		$("#dispItem").attr('src', e.target.result);
	}

	myImage.readAsDataURL(image.files[0]);

}

$('#itemImage').change(function() {
	readMyURL(this);
});

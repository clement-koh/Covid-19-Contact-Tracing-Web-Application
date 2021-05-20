// Adds event listener to all location records to hide / display
$(document).ready(function() {
	$(".LocationNameContainer").click(function() {
		$(this).siblings('.RecordChunk').slideToggle(250);
	})
});

// Function to show details of all location records
function showAllFunction() {
	$(".RecordChunk").slideDown(250);
}

// Function to hide details of all location records
function closeAllFunction() {
	$('.RecordChunk').slideUp(250);
}
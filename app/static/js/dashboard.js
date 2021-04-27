$(document).ready(function() {
	showMessages();
	setTimeout(removeMessages, 4000);
});

function showMessages(){
	$("#errorMsg").slideDown();
	$("#msg").slideDown()
}


function removeMessages() {
	$("#errorMsg").slideUp();
	$("#msg").slideUp()
}
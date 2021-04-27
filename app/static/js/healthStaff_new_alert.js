// Apply autocorrect to the search bar
$( document ).ready(function() {
	/* initiate the autocomplete function on the "search" element, and pass along the countries array as possible autocomplete values: */
	autocomplete(document.getElementById("recipient"), recipientList);
});
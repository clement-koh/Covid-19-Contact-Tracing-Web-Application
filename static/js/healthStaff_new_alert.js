// Apply autocorrect to the search bar
$( document ).ready(function() {
	// Change suggestions depending on grouping selected
	var grouping = document.getElementById("category")
	grouping.addEventListener("change", function() {
		if (grouping.value == "public")
			autocomplete(document.getElementById("recipient"), NRICList);
		else 
			autocomplete(document.getElementById("recipient"), businessNames);
	})

	/* initiate the autocomplete function on the "search" element, and pass along the countries array as possible autocomplete values: */
	autocomplete(document.getElementById("recipient"), NRICList);
});
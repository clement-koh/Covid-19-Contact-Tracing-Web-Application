// Set the ajax to run when page loads
$(document).ready(function() {
	setTimeout(loadContent,0);
});

count = 0;

// Generate HTML block for a day displaying affected area
function generateBlock(data) {

	// Create a HTML block to be displayed
	var block = "<b><i>Visited Areas for " + data.date + "</i></b><p>" + 
				`There are a total of ${data.no_of_cases} active cases in the community. <br />`;

	// Adds message based on number of location affected
	if (Number(data.locations.length) > 0) {
		block += "Below are the locations that have been visited.\
					Please take the necessary precaution when frequenting these locations";
	} else {
		block += "There are no locations visited by active cases today";
	}
	block += "</p><ol>";
	
	// Adds all affected location in the block
	for (var location in data.locations) {
		block += `<li> ${data.locations[location]} </li>`;
	}
	block += "</ol><hr/>";

	// Returns the HTML block
	return block;
}

// Loads the 14 days of record using ajax
function loadContent() {
	// Controlled Async Ajax call to only call the 
	// next's day record if the current is done loading
	$.ajax({
		async: true,
		data : {
			days_ago : count
		},
		type : 'POST',
		url : '/view_affected_location'
	})
	.done(function(data) {
		document.getElementById("dataTable").innerHTML += generateBlock(data);
		count++;
		if (count <= 14) {
			loadContent();
		}
	})
}
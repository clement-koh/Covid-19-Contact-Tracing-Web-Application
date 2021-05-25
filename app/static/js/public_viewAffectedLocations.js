// Set the ajax to run when page loads
$(document).ready(function() {
	setTimeout(loadContent,0);
});

count = 0;

// Generate HTML block for a day displaying affected area
function generateBlock(data) {

	// Create a HTML block to be displayed
	var block = "<b><i>Visited Areas for " + data[0] + "</i></b><p>" + 
				`There are a total of ${data[1]} active cases in the community. <br />`;

	// Adds message based on number of location affected
	if (Number(data[2].length) > 0) {
		block += "Below are the locations that have been visited.\
					Please take the necessary precaution when frequenting these locations";
	} else {
		block += "There are no locations visited by active cases today";
	}
	block += "</p><ol>";
	
	// Adds all affected location in the block
	for (var i = 0; i < data[2].length; i++) {
		block += `<li> ${data[2][i]} </li>`;
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
		} else {
			$(".loader").hide();
		}
	})
}
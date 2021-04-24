$(document).ready(function() {
	setTimeout(loadContent,0);
});

count = 0;

// Generate HTML block for a day displaying affected area
function generateBlock(data) {
	var block = "<b><i>Visited Areas for " + data.date + "</i></b><p>" + 
				`There are a total of ${data.no_of_cases} active cases in the community. <br />`;

	if (Number(data.locations.length) > 0) {
		block += "Below are the locations that have been visited.\
					Please take the necessary precaution when frequenting these locations";
		
	} else {
		block += "There are no locations visited by active cases today";
	}
	block += "</p><ol>";
	
	for (var location in data.locations) {
		block += `<li> ${data.locations[location]} </li>`;
	}
	block += "</ol><hr/>";
	return block;
}

// Loads the 14 days of record using ajax
function loadContent() {
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
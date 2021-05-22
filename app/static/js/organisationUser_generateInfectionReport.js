$(document).ready(function () {
	// display data for the line graph
	$(".loader").hide();
	$("#noOfCases").hide();
	var xValues = getBiweeklyDate();
	var yValues = dailyInfectionCount;

	maxInfection = Math.max(...dailyInfectionCount);
	tableMax = Math.ceil(maxInfection * 1.1);

	new Chart("biweeklyChart", {
		type: "line",
		data: {
			labels: xValues,
			datasets: [
				{
					fill: false,
					lineTension: 0,
					backgroundColor: "rgba(0,0,255,1.0)",
					borderColor: "rgba(0,0,255,0.1)",
					data: yValues
				}
			]
		},
		options: {
			legend: {display: false},
			scales: {
				// yAxis range between 0 to to largest value in data
				yAxes: [{ticks: {min: 0, max: tableMax}}]
			}
		}
	});

	// disable button
	document.getElementById("viewChart").disabled = true;

	// display detailed report
	var today = new Date();
	var day = today.toLocaleDateString("default", {day: "2-digit"});
	var month = today.toLocaleDateString("default", {month: "2-digit"});
	var year = today.toLocaleDateString("default", {year: "numeric"});
	var format = year + "-" + month + "-" + day;

	// set maximum selectable date as today
	document.getElementById("dateSelection").setAttribute("max", format);

	// set default as today
	document.getElementById("dateSelection").valueAsDate = new Date();
});

// get the past 14 days (including today)
function getBiweeklyDate() {
	// get today's date
	var currentDate = new Date();
	var biWeeklyDate = new Array();

	for (count = 1; count < 15; count++) {
		// format date output
		var date = currentDate.toLocaleDateString("en-GB", {
			day: "2-digit",
			month: "short"
		});
		biWeeklyDate.push(date);
		// get the previous date
		currentDate.setDate(currentDate.getDate() - 1);
	}
	// sort date in ascending order
	biWeeklyDate.sort();
	return biWeeklyDate;
}

// toggle to line graph
function viewChart() {
	var displayChart = document.getElementById("displayChart");
	var displayReport = document.getElementById("displayReport");

	// hide/unhide div
	displayChart.style.display = "block";
	displayReport.style.display = "none";

	// disable button
	document.getElementById("viewChart").disabled = true;
	document.getElementById("viewDetailedReport").disabled = false;
}

// toggle to detailed report
function viewDetailedReport() {
	var displayChart = document.getElementById("displayChart");
	var displayReport = document.getElementById("displayReport");

	// hide/unhide div
	displayChart.style.display = "none";
	displayReport.style.display = "block";

	// disable button
	document.getElementById("viewChart").disabled = false;
	document.getElementById("viewDetailedReport").disabled = true;
}

// display detailed report table
function showDetailedReport() {
	var displayTable = document.getElementById("detailedReport");
	var selectedDate = document.getElementById("dateSelection");
	var changeDate = document.getElementById("date");
	var form = document.getElementById("form");

	// disable page refresh on submit
	function handleForm(event) {
		event.preventDefault();
		
		// change table date to the selected date
		if (selectedDate.value != "") {
			var date = new Date(selectedDate.value);
			loadContent(date);
			$("#noOfCases").show();
			var format = date.toLocaleDateString("default", {
				day: "2-digit",
				month: "short",
				year: "numeric"
			});
			changeDate.innerHTML = format;
			
		}
	}
	form.addEventListener("submit", handleForm);
}

function loadContent(selectedDate) {
	// Get current date
	var today = new Date();

	const diffTime = Math.abs(today.getTime() - selectedDate.getTime());
	const days_ago = Math.floor(diffTime / (1000 * 60 * 60 * 24));

	$(".loader").show();

	// Async Ajax call to fetch data
	$.ajax({
		async: true,
		data: {
			days_ago: days_ago
		},
		type: "POST",
		url: "/view_infection_report"
	}).done(function (data) {
		showData(data);
		$(".loader").hide();
	});
}

function showData(data) {
	$("#noOfActiveCase").text(data.no_of_cases);
	$("#locationListing").empty();

	var currentLocation = "";
	locationCount = 0;

	// Show table header
	$("#locationListing").append(
		`<tr><th>Location</th><th>No of cases checked in</th></tr>`
	);

	// Cycle through all locations visited
	for (var i = 0; i < data.locations.length; i++) {
		// Skip to next location if same location
		if (currentLocation == data.locations[i]) {
			continue;
		}

		caseCount = 0;
		currentLocation = data.locations[i];

		// Count number of repeat for this location
		for (var j = 0; j < data.locations.length; j++) {
			if (currentLocation == data.locations[j]) {
				caseCount++;
			}
		}

		// Record location into table
		$("#locationListing").append(
			`<tr><td>${currentLocation}</td><td>${caseCount}</tr>`
		);
		locationCount++;
	}

	// If there are no locations visited
	if (locationCount == 0) {
		// Update header
		$("#detailHeader").text(
			`No locations has been visited by covid-19 positive cases:`
		);

		// Add empty table row
		$("#locationListing").append(`<tr><td>-</td><td>-</tr>`);
	} else if (locationCount == 1) {
		// Update header with number of locations affected
		$("#detailHeader").text(
			`${locationCount} location has been visited by covid-19 positive cases`
		);
	} else {
		// Update header with number of locations affected
		$("#detailHeader").text(
			`${locationCount} locations have been visited by covid-19 positive cases`
		);
	}
}

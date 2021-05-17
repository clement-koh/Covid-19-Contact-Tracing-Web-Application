$(document).ready(function() {
	// display data for the line graph
    var xValues = getBiweeklyDate();
	var yValues = [10,5,1,2,4,7,10,3,13,10,24,24,19,38];

	new Chart("biweeklyChart", {
		type: "line",
		data: {
			labels: xValues,
			datasets: [{
				fill: false,
				lineTension: 0,
				backgroundColor: "rgba(0,0,255,1.0)",
				borderColor: "rgba(0,0,255,0.1)",
				data: yValues
			}]
		},
		options: {
			legend: {display: false},
			scales: {
				// yAxis range between 0 to 100
				yAxes: [{ticks: {min: 0, max: 100}}],
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

});

// get the past 14 days (including today)
function getBiweeklyDate() {
	// get today's date
	var currentDate = new Date();
	var biWeeklyDate = new Array();

	for (count = 1; count < 15; count++) {
		// format date output
		var date = currentDate.toLocaleDateString("default", {day: "2-digit", month: "short", year: "numeric"});
		biWeeklyDate.push(date);
		// get the previous date
		currentDate.setDate(currentDate.getDate() - 1);
	}
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
	function handleForm(event) { event.preventDefault(); }
	form.addEventListener('submit', handleForm);
	
	// change table date to the selected date
	if (selectedDate.value != "") {
		displayTable.style.display = "block";
		var date = new Date(selectedDate.value);
		var format = date.toLocaleDateString("default", {day: "2-digit", month: "short", year: "numeric"});
		changeDate.innerHTML = format;
	}


}
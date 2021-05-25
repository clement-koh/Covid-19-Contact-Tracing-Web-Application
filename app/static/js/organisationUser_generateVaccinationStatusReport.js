$(document).ready(function()
{
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawChart);
	
	// Draw the chart and set the chart values
	function drawChart() 
	{
		// An array containing all the information record
		var total_number = status_info[0];
		var fully_vaccinated = status_info[1];
		var first_dose = status_info[2];
		var not_taken = status_info[3];
		var not_eligible = status_info[4];

		// Convert value into percentage and display percentage into summary in html
		var full_vac = (fully_vaccinated / total_number) * 100;
		document.getElementById('fully_vaccinated').innerHTML = full_vac.toFixed(1);

		var taken_first_vac = (first_dose / total_number) * 100;
		document.getElementById('first_dose').innerHTML = taken_first_vac.toFixed(1);

		var not_taken_vac = (not_taken / total_number) * 100;
		document.getElementById('not_taken').innerHTML = not_taken_vac.toFixed(1);

		var not_eligible_vac = (not_eligible / total_number) * 100;
		document.getElementById('not_eligible').innerHTML = not_eligible_vac.toFixed(1);

		// Pie chart data
		var data = google.visualization.arrayToDataTable([
			['Status', 'Number of People per Status'],
			['Fully Vaccinated', fully_vaccinated],
			['Completed First Dose of Vaccination', first_dose],
			['Not Taken Vaccination', not_taken],
			['Not Eligible for Vaccination', not_eligible],
		]);

		// Design legend and pie chart
		var options = {
			pieSliceText: "percentage",
			legend: {
				position: "labeled",
				maxLines: 1,
				alignment: "center",
				textStyle: {
					color: "black",
					fontSize: 13,
					fontName: "Nunito"
				}
			},
			width: '100%',
			height: 300,
			chartArea: {
				left: 0,
				top: 30,
				width: "100%",
				height: "100%"
			},
			//color of the pie chart
			slices: {
				0: {color: "#00b33c"},
				1: {color: "#ff9933"},
				2: {color: "#3366ff"},
				3: {color: "#ff3300"}
			}
		};

		// Display the chart inside the <div> element with id="piechart"
		var chart = new google.visualization.PieChart(document.getElementById('piechart'));
		chart.draw(data, options);
	}
})

// Display the current date without time
window.onload = function() 
{
	var currentdate = new Date();
	var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
	var currentday = currentdate.getDate();
	var currentyear = currentdate.getFullYear();
	document.getElementById('date').innerHTML = currentday + ' ' + months[currentdate.getMonth()] + ' ' + currentyear;
};
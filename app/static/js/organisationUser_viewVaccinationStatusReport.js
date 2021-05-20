$(document).ready(function()
{
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);
  
  // Draw the chart and set the chart values
  function drawChart() 
  {
    // Insert the number of people for each status here
    var total_number = 4000;
    var fully_vaccinated = 1500;
    var first_dose = 1700;
    var not_taken = 600;
    var not_eligible = 200;

    // convert value into percentage and display percentage into summary in html
    var full_vac = (fully_vaccinated / total_number) * 100;
    document.getElementById('fully_vaccinated').innerHTML = full_vac;

    var taken_first_vac = (first_dose / total_number) * 100;
    document.getElementById('first_dose').innerHTML = taken_first_vac;

    var not_taken_vac = (not_taken / total_number) * 100;
    document.getElementById('not_taken').innerHTML = not_taken_vac;

    var not_eligible_vac = (not_eligible / total_number) * 100;
    document.getElementById('not_eligible').innerHTML = not_eligible_vac;

    //pie chart data
    var data = google.visualization.arrayToDataTable([
    ['Status', 'Number of People per Status'],
    ['Fully Vaccinated', fully_vaccinated],
    ['Completed First Dose of Vaccination', first_dose],
    ['Not Taken Vaccination', not_taken],
    ['Not Eligible for Vaccination', not_eligible],
    ]);

    // Design legend and pie chart
    var options = 
    {
      legend: 
      {
        position: 'right', 
        textStyle: 
        {
          color:'black',
          fontSize: 13, 
          fontName:'Raleway'
        }
      },
      width:900, 
      height:900,
      chartArea:
      {
        left:0,
        top:30
      },
      //color of the pie chart
      slices: 
      {
        0: { color: '#00b33c' },
        1: { color: '#ff9933' },
        2: { color: '#3366ff' },
        3: { color: '#ff3300' },
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


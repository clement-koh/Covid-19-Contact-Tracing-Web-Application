window.addEventListener('load', function (){
   setDate();
});

// block out date selections to only 14 days including current day
function setDate() {
    var reportDate = document.getElementById("report_date");
    // set max to current date
    var maxDate = new Date().toISOString().split("T")[0]; 
    reportDate.max = maxDate;

    // set default date to current date
    reportDate.value = maxDate;

    // set min to 13 days before
    var date = new Date();
    date.setDate(date.getDate() - 13);
    reportDate.min = date.toISOString().split('T')[0];
}
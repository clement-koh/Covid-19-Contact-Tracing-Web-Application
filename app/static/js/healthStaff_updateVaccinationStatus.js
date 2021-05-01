window.addEventListener('load', disableFutureDates);

//disable the input vaccination after the current day
function disableFutureDates() {
    var pickDates = document.getElementsByClassName("vaccination_date");
    var date = new Date();
    date.setDate(date.getDate());
    var today = date.toISOString().split('T')[0];
    // loop every date picker
    for (i = 0; i < pickDates.length; i++) {
        pickDates[i].setAttribute('max', today); 
    }
}
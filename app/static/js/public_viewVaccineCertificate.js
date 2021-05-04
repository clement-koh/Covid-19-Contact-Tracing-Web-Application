$(document).ready(function() {
      // patient's full name
      document.getElementById("patientName").innerHTML = "Drew Bay Smith";
      // date of vaccination completion
      document.getElementById("date").innerHTML = "29 April 2021";
      // disable right click on template image
      $('img').bind('contextmenu', function(e) {
        return false;
      }); 
      // disable drag and drop template image
      document.getElementById('img').ondragstart = function() { return false; };
    });

    function downloadimage() {
      // elements to be included in the printing
      var container = document.getElementById("cert"); 

      html2canvas(container, { allowTaint: true }).then(function (canvas) {
        var link = document.createElement("a");
        document.body.appendChild(link);
        link.download = "certificate.jpg";
        link.href = canvas.toDataURL();
        link.target = '_blank';
        link.click();
      });
    }
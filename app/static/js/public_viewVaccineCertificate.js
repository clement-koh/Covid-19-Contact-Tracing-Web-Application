$(document).ready(function() {
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

      html2canvas(container, { allowTaint: true, scrollY: -window.scrollY, windowWidth: document.documentElement.offsetWidth }).then(function (canvas) {
        var link = document.createElement("a");
        document.body.appendChild(link);
        link.download = "certificate.jpg";
        link.href = canvas.toDataURL();
        link.target = '_blank';
        link.click();
      });
    }
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
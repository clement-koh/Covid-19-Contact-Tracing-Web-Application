function changeAccStatus() {
	var accStatus = document.getElementById("accStatus").textContent;
	var modalBody = document.getElementById("modal-body").children;
	var modalBtn = document.getElementById("modal-footer").children;

	if (accStatus == "Suspend") {
		// change account status button & color on the webpage
		document.getElementById("accStatus").textContent = "Unsuspend";
		document.getElementById("accStatusBtn").classList.remove("btn-danger");
		document.getElementById("accStatusBtn").classList.add("btn-success");
		// change modal body content
		modalBody[2].innerHTML = "You are about to <b>UNSUSPEND</b> this account. Do you want to proceed?";
		// change modal button
		modalBtn[1].innerHTML = "Unsuspend";
		modalBtn[1].classList.remove("btn-danger");
		modalBtn[1].classList.add("btn-success");
	}
	else {
		// change account status button & color on the webpage
		document.getElementById("accStatus").textContent = "Suspend";
		document.getElementById("accStatusBtn").classList.remove("btn-success");
		document.getElementById("accStatusBtn").classList.add("btn-danger");
		// change modal body content
		modalBody[2].innerHTML = "You are about to <b>SUSPEND</b> this account. Do you want to proceed?";
		// change modal button
		modalBtn[1].innerHTML = "Suspend";
		modalBtn[1].classList.remove("btn-success");
		modalBtn[1].classList.add("btn-danger");
	}
}
var statusDropdown;
var checkbox_firstDose;
var checkbox_secondDose;

$(document).ready(function() {
	// Add a change listener
	statusDropdown = $("#status_dropdown")
	checkbox_firstDose = $("#first_dose");
	checkbox_secondDose = $("#second_dose");
	statusDropdown.change(updateOptions);
	checkbox_firstDose.change(forceCheckBox);
	checkbox_secondDose.change(forceCheckBox);
	updateOptions();
})

options = ['not_eligible',
		   	'eligible',
			'first_dose_scheduled',
			'second_dose_scheduled',
			'vaccination_completed']

// Update the option based on the dropdown selected
function updateOptions() {
	var selectedOption = statusDropdown.children("option:selected").val();

	// Uncheck all checkboxes
	checkbox_firstDose.attr("disabled", true);
	checkbox_secondDose.attr("disabled", true);
	checkbox_firstDose.prop("checked", false);
	checkbox_secondDose.prop("checked", false);

	if (selectedOption == options[3]) {
		// Set first_dose as scheduled
		checkbox_firstDose.attr("disabled", false);
		checkbox_firstDose.prop("checked", true);

	} else if (selectedOption == options[4]) {
		checkbox_firstDose.prop("checked", true);
		checkbox_secondDose.prop("checked", true);
		checkbox_firstDose.attr("disabled", false);
		checkbox_secondDose.attr("disabled", false);
	}
}

function forceCheckBox(check) {
	var selectedOption = statusDropdown.children("option:selected").val();

	if (selectedOption == options[3]) {
		checkbox_firstDose.prop("checked", true);
	}

	if (selectedOption == options[4]) {
		checkbox_firstDose.prop("checked", true);
		checkbox_secondDose.prop("checked", true);
	}
}

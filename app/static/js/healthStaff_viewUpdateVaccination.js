$(document).ready(function() {
	// Add a change listener
	$("#status_dropdown").change(updateOptions);
	updateOptions();
})

options = ['not_eligible',
		   	'eligible',
			'first_dose_scheduled',
			'second_dose_scheduled',
			'vaccination_completed']

// Update the option based on the dropdown selected
function updateOptions() {
	var selectedOption = $("#status_dropdown").children("option:selected").val();
	var checkbox_firstDose = $("#first_dose");
	var checkbox_secondDose = $("#second_dose");

	// Uncheck all checkboxes
	checkbox_firstDose.attr("disabled", true);
	checkbox_secondDose.attr("disabled", true);
	checkbox_firstDose.prop("checked", false );
	checkbox_secondDose.prop("checked", false );

	if (selectedOption == options[3]) {
		// Set first_dose as scheduled
		checkbox_firstDose.prop("checked", true );
		checkbox_firstDose.attr("disabled", false);

	} else if (selectedOption == options[4]) {
		checkbox_firstDose.prop("checked", true );
		checkbox_secondDose.prop("checked", true );
		checkbox_firstDose.attr("disabled", false);
		checkbox_secondDose.attr("disabled", false);
	}
}


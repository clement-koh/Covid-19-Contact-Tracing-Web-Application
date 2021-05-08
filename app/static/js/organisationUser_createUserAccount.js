var accountTypeField;
var licenseField;
var businessField;
var organisationField;
var licenseDiv;
var businessDiv;
var organisationDiv;

// Link all variable names with elements in page
function linkVariables() {
	accountTypeField = $("#acc_type");
	licenseField = $("#license_number");
	businessField = $("#businessName");
	organisationField = $("#organisationName");
	licenseDiv = $("#licenseDIV");
	businessDiv = $("#businessDiv");
	organisationDiv = $("#organisationDiv");
}

$(document).ready(function () {
	linkVariables();
	accountTypeField.change(updateFields);
	licenseDiv.hide();
	businessDiv.hide();
	organisationDiv.hide();
	autocomplete(document.getElementById("businessName"), businessNames);
	autocomplete(document.getElementById("organisationName"),organisationNames);
});

function updateFields() {
	value = accountTypeField.children("option:selected").val();

	// Hide all fields
	licenseDiv.slideUp(1000);
	businessDiv.slideUp(1000);
	organisationDiv.slideUp(1000);

	if (value == "Business") {
		// Show Business field
		businessDiv.slideDown(1000, resetFields);
	} else if (value == "Health Staff") {
		// Show License field
		licenseDiv.slideDown(1000, resetFields);
	} else if (value == "Organisation") {
		// Show Organisation Field
		organisationDiv.slideDown(1000, resetFields);
	}
}

function resetFields() {
	// Reset all field values
	licenseField.val("");
	businessField.val("");
	organisationField.val("");
}

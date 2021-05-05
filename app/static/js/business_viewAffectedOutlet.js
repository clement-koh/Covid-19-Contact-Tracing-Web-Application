$(document).ready(function()
{
  $(".LocationNameContainer").click(function()
  {
    $(this).siblings('.RecordChunk').slideToggle(250);
  }
)});

function showAllFunction() 
{
    $(".RecordChunk").slideDown(250);
}

function closeAllFunction() 
{
    $('.RecordChunk').slideUp(250);
}



 

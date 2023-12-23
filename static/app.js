$(document).ready(function() {
    console.log('doc ready...');
    $("input[type=radio]").on("change", function() {
        $("form").submit();
    });
});
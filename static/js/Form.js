$(document).ready(function() {
    function disableBack() { window.history.forward() }

    window.onload = disableBack();
    window.onpageshow = function(evt) { if (evt.persisted) disableBack() }
});

// To-do : Handle the case when user presses back button from index.html
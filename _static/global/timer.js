$(function() {
    var currentDate = new Date();
    var milliseconds = 480000;
    $('div#clocked').countdown(currentDate.valueOf() + milliseconds, function(event) {
            console.log(event.type)
            switch(event.type) {
                case "finish":
                  $('div#clocked').hide();
                case "finished":
                    $('div#clocked').hide();
            }
        });


});

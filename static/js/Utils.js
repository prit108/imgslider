/*
REVAMP TO-DO : 
    1) add instructions
        --> Set A and Set B (extensive, clear cut instructions)
    2) revamp the success page
	    --> add a final stats display on the success page
    (partialy done) 3) add new images according to the set A or set B 
	---> 4)add a data structure to capture each of the moves to be made in each of the games in the set
	    --> add a AJAX request to send mf-key, login details, num_moves, time_elapsed, and moves_list for each game in the set
*/
function get1DIndex(x, y, rowCount) {
    return (y * rowCount + x);
};

function called() {
    console.log("I was called");
}

function splitarray(arr, n) {
    var new_arr = new Array(n);
    for (var i = 0; i < n; i++) {
        new_arr[i] = new Array();
    }

    for (var i = 0; i < n; i++) {
        new_arr[i] = arr[i].split("#");
    }

    return new_arr;
};

var onstate = 0;
var gameCnt = 0;
const gameSetSize = 6;
const SetASize = 3;
var gotoB = false;
const moveCntSize = 1000;
var num_moves = new Array(gameSetSize).fill(0);
var elapsed_time = new Array(gameSetSize);
var solved = new Array(gameSetSize).fill(0);
var moves = new Array();
var image_shown = new Array(gameSetSize);
for (let i = 0; i < gameSetSize; i++) {
    moves.push([]);
}
const timer = ms => new Promise(res => setTimeout(res, ms))

$(document).ready(function() {

    onstate = 0;

    $('#imageSelection').children('li').bind('click', function(e) {
        $('#imageTextfield').val($(this).children('a').children('img').attr('src'));
    });

    $('.loadChooseUI').click(function() {

        ImagePuzzle_Utils.loadChooseUI();
        $('#gameContainer').attr('style', 'display:none');
        $('#chooseContainer').attr('style', 'display:inline');
        $('#setAIntro').attr('style', 'display:inline');
        $('#moveCount').html('0');
        $('#retraceCount').html('0');
        clearInterval(ImagePuzzle_Game.timerIntervalId);
    });

    document.getElementById('submit').addEventListener('click', function(event) {
        if (gameCnt < SetASize) {
            ImagePuzzle_Game.init(gameCnt, 1);
        } else {
            ImagePuzzle_Game.init(gameCnt, 2);
        }
        gameCnt += 1;

    }, false);

    document.getElementById('passSetB').addEventListener('click', function(event) {
        console.log("Not doing Set B");
        gameCnt = gameSetSize + 2;
        $("#giveup").click();
    }, false);

    document.getElementById('gotoSetB').addEventListener('click', function(event) {
        gotoB = true;
        $("#giveup").attr('style', 'display:none');
        $('#gameContainer').attr('style', 'display:none');
        $("#chooseContainer").attr('style', 'display:inline');
        $("#setAIntro").attr('style', 'display:none');
        $("#askB").attr('style', 'display:none');
        $("#setBIntro").attr('style', 'display:inline');
        $("#submit").attr('style', 'display:inline');
    }, false);

    document.getElementById('giveup').addEventListener('click', function(event) {
        //solved[gameCnt - 1] = 0;
        console.log("giveup pressed: ", gameCnt);
        if (gameCnt < SetASize) {
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;
            $('#gameContainer').attr('style', 'display:none');
            $('#moveCount').html('0');
            $('#retraceCount').html('0');
            clearInterval(ImagePuzzle_Game.timerIntervalId);
            /*if (gameCnt == SetASize - 1) {
                $("playAgainLink").attr('style', 'display:inline');
            } else {
               
            }*/
            ImagePuzzle_Game.init(gameCnt, 1);
            gameCnt += 1
        } else if (gameCnt == SetASize) {
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;
            console.log("pop_up_time");
            $("#giveup").attr('style', 'display:none');
            $('#gameContainer').attr('style', 'display:none');
            $("#chooseContainer").attr('style', 'display:inline');
            $("#setAIntro").attr('style', 'display:none');
            $("#setBIntro").attr('style', 'display:none');
            $("#submit").attr('style', 'display:none');
            $("#askB").attr('style', 'display:inline');
        } else if (gameCnt < gameSetSize) {
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;
            $('#gameContainer').attr('style', 'display:none');
            $('#moveCount').html('0');
            $('#retraceCount').html('0');
            clearInterval(ImagePuzzle_Game.timerIntervalId);
            ImagePuzzle_Game.init(gameCnt, 2);
            gameCnt += 1;
        } else if (gameCnt == gameSetSize) { // if all games played proceed to exit screen
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;

            console.log("completed all games, redirecting to success");

            $.ajax({
                type: 'POST',
                url: '/getFinalVar',
                contentType: "application/json;charset=utf-8",
                traditional: "true",
                dataType: "json",
                data: JSON.stringify({
                    nummoves: num_moves,
                    elapsedtime: elapsed_time,
                    issolved: solved,
                    moveslist: moves,
                    imagesrc: image_shown
                }),
            });

            for (var i = 0; i < gameSetSize; i++) {
                console.log("moves", i, num_moves[i]);
                console.log("elapsed_time", i, elapsed_time[i]);
                console.log("moves_list", i, moves[i]);
                console.log("is_solved", i, solved[i]);
            }

            window.location.href = "/success";

        } else {
            $.ajax({
                type: 'POST',
                url: '/getFinalVar',
                contentType: "application/json;charset=utf-8",
                traditional: "true",
                dataType: "json",
                data: JSON.stringify({
                    nummoves: num_moves,
                    elapsedtime: elapsed_time,
                    issolved: solved,
                    moveslist: moves,
                    imagesrc: image_shown
                }),
            });

            for (var i = 0; i < gameSetSize; i++) {
                console.log("moves", i, num_moves[i]);
                console.log("elapsed_time", i, elapsed_time[i]);
                console.log("moves_list", i, moves[i]);
                console.log("is_solved", i, solved[i]);
            }
            console.log(window.location);
            window.location.href = "/success"

        }
    }, false);

    document.getElementById('nextpuzzlebtn').addEventListener('click', function(event) {
        //solved[gameCnt - 1] = 1;
        console.log("giveup pressed: ", gameCnt);
        if (gameCnt < SetASize) {
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;
            $('#gameContainer').attr('style', 'display:none');
            $('#moveCount').html('0');
            $('#retraceCount').html('0');
            clearInterval(ImagePuzzle_Game.timerIntervalId);
            /*if (gameCnt == SetASize - 1) {
                $("playAgainLink").attr('style', 'display:inline');
            } else {
               
            }*/
            ImagePuzzle_Game.init(gameCnt, 1);
            gameCnt += 1
        } else if (gameCnt == SetASize) {
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;
            console.log("pop_up_time");
            $("#giveup").attr('style', 'display:none');
            $('#gameContainer').attr('style', 'display:none');
            $("#chooseContainer").attr('style', 'display:inline');
            $("#setAIntro").attr('style', 'display:none');
            $("#setBIntro").attr('style', 'display:none');
            $("#askB").attr('style', 'display:inline');
        } else if (gameCnt < gameSetSize) {
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;
            $('#gameContainer').attr('style', 'display:none');
            $('#moveCount').html('0');
            $('#retraceCount').html('0');
            clearInterval(ImagePuzzle_Game.timerIntervalId);
            ImagePuzzle_Game.init(gameCnt, 2);
            gameCnt += 1;
        } else { // if all games played proceed to exit screen
            num_moves[gameCnt - 1] = ImagePuzzle_Utils.noOfMoves;
            elapsed_time[gameCnt - 1] = ImagePuzzle_Utils.timetaken;

            console.log("completed all games, redirecting to success");

            $.ajax({
                type: 'POST',
                url: '/getFinalVar',
                contentType: "application/json;charset=utf-8",
                traditional: "true",
                dataType: "json",
                data: JSON.stringify({
                    nummoves: num_moves,
                    elapsedtime: elapsed_time,
                    issolved: solved,
                    moveslist: moves,
                    imagesrc: image_shown
                }),
            });

            for (var i = 0; i < gameSetSize; i++) {
                console.log("moves", i, num_moves[i]);
                console.log("elapsed_time", i, elapsed_time[i]);
                console.log("moves_list", i, moves[i]);
                console.log("is_solved", i, solved[i]);
            }

            window.location.href = "/success";
        }
    }, false);

    /*document.getElementById('restart').addEventListener('click', function(event) {
        $('#restart').attr('style', 'display:none');
    }, false);*/

    /*document.getElementById('help').addEventListener('click', function(event) {

    }, false);*/


    // For the Heuristic Algorithm Solving :)
    document.getElementById('autosolve').addEventListener('click', async function(event) {
        onstate = 1;
        xarr = ImagePuzzle_Game.solnArray;
        var arr = splitarray(xarr, xarr.length);
        var blank_index = new Array();
        console.log(arr);
        for (var i = 0; i < arr.length; i++) {
            for (var j = 0; j < arr[i].length; j++) {
                if (arr[i][j] == '_') {
                    blank_index.push(j);
                }
            }
        }
        var becalled;
        var cx, cy;
        for (var i = 0; i < arr.length - 1; i++) {

            becalled = blank_index[i + 1];
            cy = becalled % ImagePuzzle_Game.rowCount;
            cx = Math.floor(becalled / ImagePuzzle_Game.rowCount);
            // console.log("Becalled : ", becalled);
            // console.log("Current X,Y : ", cx,cy);

            $('#grid tr:eq(' + cx + ') td:eq(' + cy + ')').click();
            await timer(500); // Delay for 1000 ms
        }
    }, false);

    $('#gameContent').on('click', '#grid td', function(e) {

        ImagePuzzle_Game.idCounter = 0,
            ImagePuzzle_Game.score = 0;

        var empty = $("#blankCell").get(0);
        if (!empty || this == empty) return; // abort, abort!

        console.log("New state after move : ");
        //console.log(ImagePuzzle_Utils.initstate);

        var currow = this.parentNode,
            emptyrow = empty.parentNode;
        var cx = this.cellIndex,
            cy = currow.rowIndex,
            ex = empty.cellIndex,
            ey = emptyrow.rowIndex;

        console.log("X,Y Clicked! : ", cx, cy);

        if (cx == ex && Math.abs(cy - ey) == 1 || cy == ey && Math.abs(cx - ex) == 1) {
            // empty and this are next to each other in the grid
            var afterempty = empty.nextSibling,
                afterthis = this.nextSibling;
            currow.insertBefore(empty, afterthis);
            emptyrow.insertBefore(this, afterempty);

            [ImagePuzzle_Utils.initstate[get1DIndex(cx, cy, ImagePuzzle_Game.rowCount)], ImagePuzzle_Utils.initstate[get1DIndex(ex, ey, ImagePuzzle_Game.rowCount)]] = [ImagePuzzle_Utils.initstate[get1DIndex(ex, ey, ImagePuzzle_Game.rowCount)], ImagePuzzle_Utils.initstate[get1DIndex(cx, cy, ImagePuzzle_Game.rowCount)]];
            console.log(ImagePuzzle_Utils.initstate);


            var str = ImagePuzzle_Utils.statetoString(ImagePuzzle_Utils.initstate);
            moves[ImagePuzzle_Game.gameNum].push(str);
            console.log("statestr:", str);

            if (ImagePuzzle_Utils.checkInMap(str)) {
                ImagePuzzle_Utils.retracedMoves++;
                ImagePuzzle_Utils.updateText('retraceCount', ImagePuzzle_Utils.retracedMoves);
            }
            console.log(str);

            ImagePuzzle_Utils.noOfMoves++;

            //play the move sound
            if ($('#mute').val() === 'off') {
                ImagePuzzle_Game.move_snd.play();
            }

            ImagePuzzle_Utils.updateText('moveCount', ImagePuzzle_Utils.noOfMoves);
            /*if(onstate === 1){			
            	$.ajax({
            	type: "POST",
            	contentType: "application/json;charset=utf-8",
            	url: "/getInitState",
            	traditional: "true",
            	data: JSON.stringify(ImagePuzzle_Utils.statetoString(ImagePuzzle_Utils.initstate)),
            	dataType: "json",
            	success: function (data) {
            		ImagePuzzle_Game.solnArray = data;
            		console.log("Solution Array :", ImagePuzzle_Game.solnArray);
            		}
            	});
            }*/
        }

        // Check if puzzle is complete after each move
        $("td").each(function() {

            if ($(this).children().attr("id") == "canvas" + ImagePuzzle_Game.idCounter) {

                ImagePuzzle_Game.score++;
                if (ImagePuzzle_Game.score == ImagePuzzle_Game.target && gameCnt <= SetASize) {

                    //show complete image
                    $("#blankCell").children().show();
                    $("#blankCell").attr('id', $("#blankCell").children().attr('id'));
                    $("#giveup").attr('style', 'display:none');

                    solved[gameCnt - 1] = 1;
                    if ($('#mute').val() === "off") {
                        ImagePuzzle_Game.win_snd.play();
                    }

                    // stop timer in UI
                    clearInterval(ImagePuzzle_Game.timerIntervalId);

                    var endTime = new Date(),
                        duration = ImagePuzzle_Utils.diffBetweenTimes(
                            ImagePuzzle_Utils.getStartTime(),
                            endTime);

                    // ImagePuzzle_Utils.puzzlesSolved++;
                    // ImagePuzzle_Utils.updateText('puzzlesSolved', ImagePuzzle_Utils.puzzlesSolved);

                    console.log("DONE!");

                    // The below commented code wont work since browsers dont allow render after render

                    // $.ajax({
                    // 	type: 'GET',
                    // 	url: "/success",
                    // });
                    // $('#playAgainLink').click();
                    console.log(ImagePuzzle_Utils.noOfMoves);

                    /*$.ajax({
                        type: 'POST',
                        url: '/getFinalVar',
                        contentType: "application/json;charset=utf-8",
                        traditional: "true",
                        dataType: "json",
                        data: JSON.stringify({
                            moves: ImagePuzzle_Utils.noOfMoves,
                            time: ImagePuzzle_Utils.timetaken,
                            retraced: ImagePuzzle_Utils.retracedMoves,
                            dimension: ImagePuzzle_Game.rowCount
                        }),
                    });
                    console.log("after the ajax request");
                    window.location.href = "/success"
					*/

                    // if game is successfully completed, check if required number of games have been played

                    $('#nextpuzzlebtn').attr('style', 'display:inline');


                }
            }

            ImagePuzzle_Game.idCounter++;
        });
    });
});


var ImagePuzzle_Utils = {

    startTime: null,
    notificationIntervalId: null,
    puzzlesSolved: 0,
    noOfMoves: 0,
    initstate: new Array(),
    retracedMoves: 0,
    stateMap: new Map(),
    timetaken: null,

    loadChooseUI: function() {

        $('#indexContainer').attr('style', 'display:none');
        $('#chooseContainer').attr('style', 'display:inline');
    },

    getStartTime: function() {
        return this.startTime;
    },

    setStartTime: function(startTimeTemp) {
        this.startTime = startTimeTemp;
    },

    //remove a value from a array
    //returns an array
    removeItemFromList: function(array, removeItem) {
        array = jQuery.grep(array, function(value) {
            return value != removeItem;
        });

        return array;
    },

    //get a random value from a list of elements
    //returns a random value
    randomChoice: function(list) {
        return list[Math.floor(Math.random() * list.length)];
    },


    //update text of an element
    //Parameters: The element ID, the text
    updateText: function(elementID, text) {
        document.getElementById(elementID).innerHTML = text;
    },


    //briefly show a notification to the user
    //Parameters: elementID to show and the duration 
    //to show in milliseconds
    notify: function(elementID, duration) {

        //set message to show in case it has previously faded out
        $(elementID).fadeTo('fast', 1);

        //ensuring notificationIntervalId is cleared
        if (this.notificationIntervalId) {
            clearInterval(this.notificationIntervalId);
        }

        //set message to fade out
        this.notificationIntervalId = setTimeout(function() {
            $(elementID).fadeTo('fast', 0);
        }, duration);
    },


    //Get the time difference between two javascript date objects
    //Returns a string containing the time.
    diffBetweenTimes: function(beginTime, endTime) {
        var timeTaken = endTime - beginTime;
        return ImagePuzzle_Utils.formatTime(timeTaken);
    },

    formatTime: function(timeTaken) {
        var timeTakenString = "";

        // calc hours
        // if ((timeTaken.getHours() - 1) < 1)	
        // 	timeTakenString += '00:';
        // else if((timeTaken.getHours() - 1) >= 0 && (timeTaken.getHours() - 1) < 10)
        // 	timeTakenString += '0' + (timeTaken.getHours() - 1).toString() + ':';
        // else
        // 	timeTakenString += (timeTaken.getHours() - 1).toString() + ':';

        // calc minutes
        var minutes = Math.floor(timeTaken / 60000);
        if (minutes < 1)
            timeTakenString += "00:";
        else if (minutes >= 0 && minutes < 10)
            timeTakenString += "0" + minutes.toString() + ":";
        else
            timeTakenString += minutes.toString() + ":";

        timeTaken -= minutes * 60000;

        //calc seconds
        var seconds = Math.floor(timeTaken / 1000);
        if (seconds < 1)
            timeTakenString += "00.";
        else if (seconds >= 0 && seconds < 10)
            timeTakenString += "0" + seconds.toString() + ".";
        else
            timeTakenString += seconds.toString() + ".";

        timeTaken -= seconds * 1000;
        //calc decisecond
        if (parseInt(timeTaken.toString()[0]) < 1)
            timeTakenString += "0";
        else
            timeTakenString += timeTaken.toString()[0];

        ImagePuzzle_Utils.timetaken = timeTakenString
        return timeTakenString;
    },

    initTimer: function() {

        ImagePuzzle_Utils.updateText(
            'timer',
            ImagePuzzle_Utils.diffBetweenTimes(
                ImagePuzzle_Utils.startTime,
                new Date()));
    },

    dialog: function(title, body) {

        $('<div><p>' + body + '</p></div>').dialog({
            modal: true,
            title: title,
            buttons: [{
                text: "Ok",
                click: function() {
                    $(this).dialog("close");
                }
            }]
        });
    },

    statetoString: function(state) {
        var temp = "";
        for (var i = 0; i < state.length; i++) {
            if (state[i] == state.length - 1) {
                temp += "_#";
            } else temp += (state[i] + 1).toString() + "#";
        }
        temp = temp.substr(0, temp.length - 1)

        return temp;
    },

    checkInMap: function(str) {
        if (ImagePuzzle_Utils.stateMap.has(str)) return true;

        ImagePuzzle_Utils.stateMap.set(str, 1);
        return false;
    },

};
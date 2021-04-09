
function get1DIndex(x,y,rowCount) {
	return (y*rowCount + x);
};

function called(){
	console.log("I was called");
}

var onstate = 0;

const timer = ms => new Promise(res => setTimeout(res, ms))

$(document).ready(function() {
	
	onstate = 0;

	$('#imageSelection').children('li').bind('click', function(e) {
	    $('#imageTextfield').val($(this).children('a').children('img').attr('src'));
	});
	
	$('.loadChooseUI').click(function(){
		
		ImagePuzzle_Utils.loadChooseUI();
		$('#gameContainer').attr('style', 'display:none');
		$('#chooseContainer').attr('style', 'display:inline');
		$('#moveCount').html('0');
		$('#retraceCount').html('0');
		clearInterval(ImagePuzzle_Game.timerIntervalId);
	});
	
	document.getElementById('submit').addEventListener('click', function(event) {		
		ImagePuzzle_Game.init();
		
	}, false);
	
	document.getElementById('restartButton').addEventListener('click', function(event) {
		
		ImagePuzzle_Utils.loadChooseUI();
		$('#gameContainer').attr('style', 'display:none');
		$('#chooseContainer').attr('style', 'display:inline');
		$('#moveCount').html('0');
		$('#restart').attr('style', 'display:none');
	}, false);

	document.getElementById('restart').addEventListener('click', function(event){
		$('#restart').attr('style', 'display:none');
	}, false);
	
	document.getElementById('help').addEventListener('click', function(event) {
		
	}, false);


	// For the Heuristic Algorithm Solving :)
	document.getElementById('autosolve').addEventListener('click', async function(event){
		onstate = 1;
		arr = ImagePuzzle_Game.solnArray;
		var blank_index = new Array();

		for(var i = 0; i < arr.length; i++) {
			for(var j = 0; j < arr[i].length; j++){
				if(arr[i][j] == '_') {
					blank_index.push(j);
				}
			}
		}
		var becalled;
		var cx, cy;
		for(var i = 0; i < arr.length - 1; i++) {
	
			becalled = blank_index[i+1];
			cy = becalled%ImagePuzzle_Game.rowCount;
			cx = Math.floor(becalled/ImagePuzzle_Game.rowCount);
			// console.log("Becalled : ", becalled);
			// console.log("Current X,Y : ", cx,cy);
	
			$('#grid tr:eq(' + cx + ') td:eq(' + cy + ')').click();
			await timer(500); // Delay for 500 ms
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

	    if (cx==ex && Math.abs(cy-ey)==1 || cy==ey && Math.abs(cx-ex)==1) {
	        // empty and this are next to each other in the grid
	        var afterempty = empty.nextSibling,
	            afterthis = this.nextSibling;
	        currow.insertBefore(empty, afterthis); 
	        emptyrow.insertBefore(this, afterempty);

			[ImagePuzzle_Utils.initstate[get1DIndex(cx,cy,ImagePuzzle_Game.rowCount)], ImagePuzzle_Utils.initstate[get1DIndex(ex,ey,ImagePuzzle_Game.rowCount)]] = [ImagePuzzle_Utils.initstate[get1DIndex(ex,ey,ImagePuzzle_Game.rowCount)],ImagePuzzle_Utils.initstate[get1DIndex(cx,cy,ImagePuzzle_Game.rowCount)]];
			console.log(ImagePuzzle_Utils.initstate);
			

			var str = ImagePuzzle_Utils.statetoString(ImagePuzzle_Utils.initstate);
			

			if(ImagePuzzle_Utils.checkInMap(str)){
				ImagePuzzle_Utils.retracedMoves++;
				ImagePuzzle_Utils.updateText('retraceCount', ImagePuzzle_Utils.retracedMoves);
			}
			// console.log(str);

	        ImagePuzzle_Utils.noOfMoves++;
	
			//play the move sound
			// if($('#mute').val() === 'off'){
			// 	ImagePuzzle_Game.move_snd.play();
			// }
	
			ImagePuzzle_Utils.updateText('moveCount', ImagePuzzle_Utils.noOfMoves);
			if(onstate === 1){			
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
			}
	    }
	    
	    // Check if puzzle is complete after each move
	    $("td").each(function() {
	    	
	    	if ($(this).children().attr("id") == "canvas" + ImagePuzzle_Game.idCounter){
	    		
	    		ImagePuzzle_Game.score++;
	    		
	    		
	    		if (ImagePuzzle_Game.score == ImagePuzzle_Game.target){
	    			
	    			//show complete image
					$("#blankCell").children().show();
					$("#blankCell").attr('id', $("#blankCell").children().attr('id'));
					
					if($('#mute').val() === "off"){
						ImagePuzzle_Game.win_snd.play();
					}
					
					// stop timer in UI
					clearInterval(ImagePuzzle_Game.timerIntervalId);	
					
					var endTime = new Date(),
						duration = ImagePuzzle_Utils.diffBetweenTimes(
		            		ImagePuzzle_Utils.getStartTime(), 
		            		endTime); 
					
					ImagePuzzle_Utils.puzzlesSolved++;
					ImagePuzzle_Utils.updateText('puzzlesSolved', ImagePuzzle_Utils.puzzlesSolved);
					
					$.ajax({
						url: "/success",
						type: 'GET',
						success: function(res) {
							console.log("Success");
						}
					});
					// $('#playAgainLink').click();
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
	retracedMoves : 0,
	stateMap :  new Map(),
	timetaken : null,
	
	loadChooseUI: function(){
		
		$('#indexContainer').attr('style', 'display:none');
		$('#chooseContainer').attr('style', 'display:inline');
	},
	
	getStartTime: function(){
		return this.startTime;
	},
	
	setStartTime: function(startTimeTemp){
		this.startTime = startTimeTemp;
	},
	
	//remove a value from a array
	//returns an array
	removeItemFromList: function(array, removeItem) {
		array =  jQuery.grep(array, function(value) {
			return value != removeItem;
		});

		return array;
	},
	
	//get a random value from a list of elements
	//returns a random value
	randomChoice: function(list) {
		return list[Math.floor(Math.random()*list.length)];
	},
	
	
	//update text of an element
	//Parameters: The element ID, the text
	updateText: function(elementID,text) {
		document.getElementById(elementID).innerHTML = text;
	},

	
	//briefly show a notification to the user
	//Parameters: elementID to show and the duration 
	//to show in milliseconds
	notify: function(elementID,duration){
	
         //set message to show in case it has previously faded out
         $(elementID).fadeTo('fast', 1);
                                
       //ensuring notificationIntervalId is cleared
 		if (this.notificationIntervalId){
 			clearInterval(this.notificationIntervalId);
 		}
 		
	     //set message to fade out
 		this.notificationIntervalId = setTimeout(function() {
	      	$(elementID).fadeTo('fast', 0);
		  }, duration); 
	},
	

	//Get the time difference between two javascript date objects
	//Returns a string containing the time.
	diffBetweenTimes: function(beginTime, endTime){
		var timeTaken = endTime - beginTime;
	 	return ImagePuzzle_Utils.formatTime(timeTaken);
	},
	
	formatTime: function(timeTaken){
		var timeTakenString = "";
		
		// calc hours
		// if ((timeTaken.getHours() - 1) < 1)	
		// 	timeTakenString += '00:';
		// else if((timeTaken.getHours() - 1) >= 0 && (timeTaken.getHours() - 1) < 10)
		// 	timeTakenString += '0' + (timeTaken.getHours() - 1).toString() + ':';
		// else
		// 	timeTakenString += (timeTaken.getHours() - 1).toString() + ':';

		// calc minutes
		var minutes  = Math.floor(timeTaken/60000);
		if (minutes < 1)
			timeTakenString += "00:";
		else if(minutes >= 0 && minutes < 10)
			timeTakenString += "0" + minutes.toString() + ":";
		else
			timeTakenString += minutes.toString() + ":";

		timeTaken -= minutes*60000;
		
		//calc seconds
		var seconds = Math.floor(timeTaken/1000);
		if (seconds < 1)
			timeTakenString += "00.";
		else if(seconds >= 0 && seconds < 10)
			timeTakenString += "0" + seconds.toString() + ".";
		else
			timeTakenString += seconds.toString() + ".";
	
		timeTaken -= seconds*1000;
		//calc decisecond
		if (parseInt(timeTaken.toString()[0]) < 1)
			timeTakenString += "0";
		else
			timeTakenString += timeTaken.toString()[0];

		ImagePuzzle_Utils.timetaken = timeTakenString
	 	return timeTakenString;
	},
	
	initTimer: function(){

		ImagePuzzle_Utils.updateText(
	    		'timer', 
	    		ImagePuzzle_Utils.diffBetweenTimes(
	    				ImagePuzzle_Utils.startTime, 
	    				new Date()));
	},
	
	dialog: function(title, body){

		$('<div><p>' + body + '</p></div>').dialog({
	    	modal: true,
		    title: title,
		    buttons:[{ 
		    	text: "Ok", click: function() {
		    		$(this).dialog("close");
			    }
			}]
		});
	},

	statetoString : function(state){
		var temp = "";
		for(var i = 0; i< state.length; i++){
			if(state[i] == state.length-1){
				temp += '_';
			}
			else temp += (state[i] + 1).toString();
		}

		return temp;
	},

	checkInMap : function(str){
		if(ImagePuzzle_Utils.stateMap.has(str)) return true;
		
		ImagePuzzle_Utils.stateMap.set(str,1);
		return false;
	},

};

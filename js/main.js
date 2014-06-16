/*
The MIT License (MIT)

Copyright (c) 2014 Squarerootfury

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
/**
* The user's answers
*/
var answers = [];
/**
* The result of the test
*/
var resultset = {};
/**
* The distributions to get displayed.
*/
var distros = [];
/**
* The systems version
*/
var Version = "1.3";
/**
* The index to display the current answered question percentage
*/
var QuestionIndex = 0;
/**
* Debug flag
*/
var Debug = false;
/**
* Presenting a object which is the last answered question.
*/
var lastAnsweredQuestion = null;

var Language = [];
$(document).ready(function(){
	$.get( "./content/language.inc.php")
		.done(function( data ) {	  
		  	var obj = JSON.parse(data);			
			Language = obj;
			$("#SystemTitle").html(Language["SystemTitle"]);
			$("Title").html(Language["SystemTitle"]);	
			$(".contact").text(Language["Imprint"]);
			$(".privacy").text(Language["Privacy"]);
			$(".shareButton").text(Language["Share"]);
			$("#StartWelcomeTitle").html(Language["StartWelcomeTitle"]);
			$("#StartText").html(Language["StartText"]);
			$("#startButton").text(Language["StartTest"]);
			$("#shareLinkTitle").text(Language["shareTitle"]);
			$("#ShareDialogTitle").text(Language["Share"]);
			$("#StoredDistros").text(Language["StoredDistros"]);
			$("#StatusTitle").text(Language["StatusTitle"]);
			$("#UsedThirdPartyThings").html(Language["UsedThirdPartyThings"]);
		}	
	);
	SetStatistics();	
	SetOnClickHandler();
});
function AddWarning(){
	$("#content").append("<div class='alert alert-danger'>"+Language["MaintWarning"]+"</div>")
}
/**
* Set the statistic information
*/
function SetStatistics(){
	$("#version").html("Linux Distribution Chooser " + Version);
	$.get( "datalayer.php", { task: "GetListOfDistributions"} )
		.done(function( data ) {	  
		  	var obj = JSON.parse(data);
			for (var i = 0; i < obj.length;i++){
				$("#DistroList").append("<li>"+obj[i]+"</li>");
			}
		}	
	);
	$.get( "datalayer.php", { task: "GetQuestionCount"} )
		.done(function( data ) {	  
		  	var obj = JSON.parse(data);			
			$("#amount").append(Language["AmountOfQuestions"]);
			$("#amount").append(obj);
		}	
	);
	$.get( "datalayer.php", { task: "GetTestCount"} )
		.done(function( data ) {	  
		  	var obj = JSON.parse(data);			
			$("#amountOfTests").append(Language["AmountOfTests"]);
			$("#amountOfTests").append(obj);
		}	
	);
}
/**
* Set the click handlers for system elements
*/
function SetOnClickHandler(){
	$("#startButton").click(function(){
		$("#content").fadeOut(function(){
			DisplayInfo();
		});
	});
	$(".contact").click(function(e){
		e.preventDefault();
		$("#contactDialog").modal();
	});
	$(".privacy").click(function(e){
		e.preventDefault();
		$("#privacyDialog").modal();
	});
	$(".status").click(function(e){
		e.preventDefault();
		$("#statusDialog").modal();
	});
	$("#info").click(function(){
		$("#infoDialog").modal();
		$("#aboutContent").html("Linux Distribution Chooser  "+ Version);		
	});

	$(".shareButton").click(function(){
		$("#shareDialog").modal();
	});
}
/**
* Display the informations before the test.
*/
function DisplayInfo(){
	$("#content").html('');
	
	$("#content").append("<div class='page-header'><h1>"+Language["Hints"]+"</h1></div>");
	if (Debug)
		AddWarning();
	$("#content").append(Language["WelcomeText"]);
	$("#content").append("<a id='startTestButton' class='btn btn-primary btn-lg' role='button'>"+Language["StartTest"]+"</a>");
	$("#content").fadeIn();
	$("#startTestButton").click(function(){
		LoadQuestion(-1);
	});
;}
/**
* Display the answer page
*/
function DisplayResult(){
	answers = answers.filter(function(e){return e});
	$("#content").html('');
	$("#content").append("<div class='page-header'><h1>"+Language["Analysis"]+"</h1></div>");
	$("#content").append("<ul id='answerpanel'></ul>");
	for (var i = 0; i < answers.length;i++){
		$("#answerpanel").append("<li>"+answers[i].Question+": " + answers[i].SelectedAnswer.Text+ "</li>");
	}	
	$("#content").append("<a id =\"backToLastQuestion\" class='btn btn-primary btn-lg' role='button'>Zurück</a>");
	$("#backToLastQuestion").click(function(){
		$("#answerpanel").fadeOut(function(){
				$("#answerpanel").remove();
				$("#content").append("<div id='answerpanel'></div>"); 				
				LoadQuestion(--lastAnsweredQuestion.Id);	
  		});
	});
	$("#content").append("<a id='showDistros' class='btn btn-success btn-lg' role='button'>"+Language["ShowResults"]+"</a>");
	$("#showDistros").click(function(){
		LoadDistributionByAnswer();
	});
}
/**
* Sort the distributions by there fitting answers
*/
function SortDistributionsByRank(){
	distros.sort(Sort);
	var lastPlace = 1;
	for (var i = 1; i < distros.length;i++){
		distros[i].Place = 1;
		if (distros[i].ChoosedBy == distros[i-1].ChoosedBy)
			distros[i].Place = lastPlace;
		else
			distros[i].Place = ++lastPlace;
	}
}
/**
* Sort algorithm by there fitting answers
* @param a the first object
* @param b the second object
* @return 1 or -1 
*/
function Sort(a,b){
	if (a.ChoosedBy < b.ChoosedBy)
		return 1;
	else
		return -1;
}
/**
* Checks if a question is the last one in the database
* @param id the questions id
* @return bool the result of the check
*/
function IsLastQuestion(id){
	$.get( "datalayer.php", { task: "isLastQuestion", id: id} )
		.done(function( data ) {	  
		  	var obj = JSON.parse(data);
			if (data == "true")
				return  true;
			else
				return  false;
		}	
	);	
}
/**
* Display the result of the test
*/
function DisplayDistributions(){
	if (!Debug)
		$.get( "datalayer.php", { task: "IncreaseTestCount"} );
	$("#content").html('');
	$("#content").append("<div class='page-header'><h1>"+Language["YourLinux"]+"</h1></div>");
	$("#content").append("<div class='well'>"+Language["ResultOrderHint"]+"</div>")
	for (var i = 0; i < distros.length;i++){
		//Anzeige für normal
		
		$("#content").append("<div class=\"panel panel-default\"><div class=\"panel-heading\">"+distros[i].Place+ ". "+ distros[i].Name+"</div><div class=\"panel-body\" id =\""+distros[i].Id+"\"><img class='distrologo hidden-xs' src='"+distros[i].ImageLink+"'/>"+distros[i].Description+"</div><div class=\"panel-footer properties hidden-xs\"><a target='_blank' href='"+distros[i].Website+"'>Website</a> | "+Language["License"]+": "+distros[i].License+" | <a target='_blank' href='"+distros[i].TextSource+"'>"+Language["TextSource"]+"</a> | <a target='_blank' href='"+distros[i].ImageSource+"'>"+Language["ImageSource"]+"</a></div></div>");
		if (distros[i].ChoosedBy > 1)
			$("#"+ distros[i].Id).append("<div class='ChoosedBy'>" + distros[i].ChoosedBy + " " + Language["AnswersFit"] + distros[i].Name + " " + Language["To"] +".</div></hr>");
		else
			$("#"+ distros[i].Id).append("<div class='ChoosedBy'>" + distros[i].ChoosedBy + " " +Language["AnswerFit"] + distros[i].Name + " " + Language["To"] +".</div></hr>");
	}
}
/**
* Load the distributions by the given answers and init the Display 
*/
function LoadDistributionByAnswer(){
	
	for (var i = 0; i < answers.length;i++){
		var answerid = answers[i].SelectedAnswer.Id;
		$.get( "datalayer.php", { task: "LoadDistributionByAnswer", id: answerid} )
			.done(function( data ) {	
				var obj = JSON.parse(data);
				for (var x = 0; x < obj.length;x++){
					var found = false;
					for (var y = 0; y < distros.length;y++){
						if (distros[y].Name == obj[x].Name){
							distros[y].ChoosedBy++;
							found = true;
							console.log(obj[x]);
						}		
					}
					if (!found){
						obj[x].ChoosedBy = 1;
						distros.push(obj[x]);
					}	
				}
				SortDistributionsByRank();
				DisplayDistributions();
		    	}
		);
	}
	
}
/**
* Loads a question by a given ID
* @param questionid the question id to load
*/
function LoadQuestion(questionid){
	var question = null;
	var prefix = "";
	$.get( "datalayer.php", { task: "loadQuestion", id: questionid } )
	  .done(function( data ) {
		if (!data)
			DisplayResult();
		else{	
		   	question = JSON.parse(data);
			lastAnsweredQuestion = question;
			//Antwort darstellen
			$("#content").html('');
			
			if (question.IsLastQuestion){
				prefix = Language["LastQuestion"];
			}
			$("#content").append("<div class='page-header'><h2 class='hidden-xs'>"+prefix + question.Question+"</h2><h3 class='visible-xs'>"+prefix +question.Question+"</h3><a href=\"#\"><span id='panicButton' class=\"label label-danger\">"+Language["HelpButton"]+"</span></a></div>");
			$("#panicButton").click(function(){
				$("#panicDialog").modal();
			});
			$.get( "./content/panicDialog.inc.php")
			.done(function( data ) {
				$("#content").append(data);
				$("#panicDialogContent").html(question.SubTitle)
			});			
			$("#content").append("<ul id='answerpanel'></ul>");
			if (!question.IsFirstQuestion)
				$("#content").append("<a id =\"back\" class='btn btn-primary btn-lg' role='button'>"+Language["Back"]+"</a>");
			else
				$("#answerpanel").css("padding-bottom","0px");
			$("#back").click(function(){
				$("#answerpanel").fadeOut(function(){
		  				$("#answerpanel").html('');
						QuestionIndex--;
						LoadQuestion(question.Id -1);	
		  		});
			});			
			for (var i = 0; i < question.Answers.length;i++){
				$("#answerpanel").append("<li><a id = '"+question.Answers[i].Id+"' href='#'>"+question.Answers[i].Text+"</a></li>");
				$("#"+question.Answers[i].Id).click(function(e){
					for (var x = 0; x < question.Answers.length;x++){							
						if (question.Answers[x].Id == e.target.id)
						{
							question.SelectedAnswer = question.Answers[x];
							break;
						}
					}						  			
		  			answers[question.Id] = question;		  		  		
		  			$("#answerpanel").fadeOut(function(){
		  				$("#answerpanel").html('');
						//questionid = ;
						QuestionIndex++;
						LoadQuestion(++question.Id);
		  			});			  			
		  		});
			}
			$.get( "datalayer.php", { task: "GetQuestionCount"} )
				.done(function( data ) {
				  	var obj = 100/(JSON.parse(data)/QuestionIndex);
					DisplayProgressBar(obj);
				}	
			);
		}
	   }
	);	
}
/**
* Displays the progress bar to the user
* @param value the current progress bar value in percent
*/
function DisplayProgressBar(value){
	$("#content").append("<div class=\"progress progress-striped active\"><div class=\"progress-bar progress-bar-success\" role=\"progressbar\" aria-valuenow=\""+value+"\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: "+value+"%;\">"+value+"% "+Language["Answered"]+".</div></div>");
}


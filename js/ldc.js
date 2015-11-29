function LDC(systemVars,language){
	//Properties
	this.systemVars = systemVars;
	this.distributions = [];
	this.distributionsAfterAnswer = [];
	this.questions =[];
	this.answers = [];
	this.language = language;
	//Methods
	this.ApplyTitle = ApplyTitle;
	this.GetSystemValue = GetSystemValue;
	this.Init = Init;
	this.GetDistros = GetDistros;
	this.GetQuestions = GetQuestions;
	this.SwitchLanguage = SwitchLanguage;
	this.SetUpUI = SetUpUI;
	this.InsertQuestions = InsertQuestions;
	this.FilterByAnswer = FilterByAnswer;
	this.ApplySearch = ApplySearch;
	this.PostAnswerClick = PostAnswerClick;
	this.GetResult = GetResult;
	this.ApplyFilterResults = ApplyFilterResults;
	this.CreateResultMatrix = CreateResultMatrix;
	this.SerializeResult = SerializeResult;
	this.UnserializeResult = UnserializeResult;
	this.NotAnEasterEgg = NotAnEasterEgg;
	this.ApplyRelativeResults = ApplyRelativeResults;
	//Go!
	this.Init();
}
function GetSystemValue(needle){
	for (var i = 0; i < this.systemVars.length; i++) {
		if (this.systemVars[i].Val == needle){
			return this.systemVars[i].Text;
		}
	}
	return "";
}
function SetUpUI(){
	ldc.ApplyTitle();	
	$(".ldcui").each(function(index, value) { 
	    var id = $(this).attr('id'); 
	    var value = ldc.GetSystemValue(id);
	    if (id == undefined || value == "")
	    {
	    	//for elements with duplicate context
	    	var classes = $(this).attr("class").split(' ');
	    	id = classes[classes.length -1];
	    	value = ldc.GetSystemValue(id);
	    }	 
	    if (value != "")
			$(this).html(value);
	});
	$("#answeredCount").text("0");
	$("#welcomeTextHeader").trigger("click");
	$("#twitterlink").attr("href","https://twitter.com/share?text="+ldc.GetSystemValue("FindTheRightLinux")+"&url=http://distrochooser.de/?r=tw&hashtags=distrochooser,linux&via=distrochooser") ;
	$("#getresult").click(function(){
		 // Add only the distros to the stats if the result was absolute or the percentage was above 20 %
                 var relevantDistros = [];
                 for(var d=0;d < ldc.distributionsAfterAnswer.length;d++){
                        if (!ldc.distributionsAfterAnswer[d].percentage)
                                     relevantDistros.push(ldc.distributionsAfterAnswer[d]);
                        else if (ldc.distributionsAfterAnswer[d].percentage > 20)
                                        relevantDistros.push(ldc.distributionsAfterAnswer[d]);
                }
		$.post( "./rest.php", { method: "AddResult", args: JSON.stringify(relevantDistros),lang: ldc.language})
		.done(function( data ) {		
			GetResult();
		});			
	});
	$("#startTest").click(function(){
		$("#Heading1").trigger("click");
	});
}
function ApplyTitle(){
	document.title = this.GetSystemValue("Title");
}
function SwitchLanguage(language){
	ldc.language = language;
	ldc.Init();
}
function GetResult(){
	$("#ResultContent").empty();
	$(".shareMenu a ").attr("style","display:initial !important");
    $(".shareMenu a i").attr("style","display:initial !important");
	if (ldc.distributionsAfterAnswer[0].percentage){
		$("#ResultContent").html("<div class='alert alert-info'>"+ldc.GetSystemValue("RelativeResults")+"</div>");
	}
	for (var i = 0; i < ldc.distributionsAfterAnswer.length; i++) {
		var item = "";
		item = "<div class='panel panel-default'>";
		item = item + "<div class='panel-heading'>"+ldc.distributionsAfterAnswer[i].Name;	
		if (ldc.distributionsAfterAnswer[i].percentage) 
			item = item +  ": " + ldc.distributionsAfterAnswer[i].percentage + "%";

		item = item +"</div>";
		item = item + "<div class='panel-body'>";
		item = item + "<a href='"+ldc.distributionsAfterAnswer[i].Homepage+"' target='_blank'><img class='linuxlogo' src='"+ldc.distributionsAfterAnswer[i].Image+"'></img></a>"+ldc.distributionsAfterAnswer[i].Description+"</div>";

		item = item + "<div class='panel-footer properties hidden-xs'><a class='detail' target='_blank' href='"+ldc.distributionsAfterAnswer[i].Homepage+"'>Website</a><a target='_blank' class='detail'  href='./detail.php?id="+ldc.distributionsAfterAnswer[i].Id+"&l="+ldc.language+"'>Details</a></div>";
		item = item + "</div>";
		$("#ResultContent").append(item);
	};	
	if (ldc.distributionsAfterAnswer.length == 0){
		$("#ResultContent").html("<div class='alert alert-info'>"+ldc.GetSystemValue("NoResults")+"</div>");
	}
	var matrix = ldc.CreateResultMatrix();
	$("#matrix").empty();
	var header = "<tr><th></th>";
	for (var i = ldc.distributions.length - 1; i >= 0; i--) {
		header += "<th><div class='verticalText'><a href='./detail.php?id="+ldc.distributions[i].Id+"'>"+ldc.distributions[i].Name+"</a></div></th>";
	};
	header += "</th>";
	$('#matrix').append(header);	
	for (var key in matrix) {
		var row = "<tr>";
		var tooltip = '<a href="#" type="button" class="questionbtn" data-toggle="popover" title="" data-content=\''+key+'\' data-trigger="focus" tabindex="0"><i class="glyphicon glyphicon-question-sign"></i></a>';		
		row +="<td>"+tooltip+"</td>";	
		var horIndex = 2;	
		for (var i = ldc.distributions.length - 1; i >= 0; i--) {	
			var name = $('#matrix th:nth-child('+horIndex+') div').first().text();
			if (matrix[key][i] == name)	
				row +="<td><i class=\"ok glyphicon glyphicon-ok\"></td>";
			else
				row +="<td><i class=\"no glyphicon glyphicon-remove\"></i></td>";
			horIndex++;
		};
		row += "</tr>";
		$('#matrix').append(row);
	}	
	var html = $("#matrix").html();
	$(".questionbtn").popover();
	var result = ldc.SerializeResult();	
	if (result != ""){
		$(".personalShareLink").each(function(){
            $(this).val("http://distrochooser.de/?r=l&answers="+result);
        });
	}else{
		$(".personalShareLink").each(function(){
           	 $(this).val("http://distrochooser.de/?r=l");
        });
	}
	$("#thanksForRating").hide();
	$("#rate").show();
	if ($("#rate").attr("class") === undefined){
		$("#rate").rateYo({
	    rating: 0,
	    fullStar: true,
	  }).on("rateyo.set", function (e, data) {	
	      $.post( "./rest.php", { method: "NewRating", args: "\""+ data.rating+"\"",lang: ldc.language});
	      $(this).fadeOut(function(){
	      		$("#thanksForRating").fadeIn();	 	
	      });	     
	  });
	}
	
	//TODO: Display
	$("#modal").modal();
}
function PostAnswerClick(){
	$("#answeredCount").text(ldc.answers.length);
	ldc.ApplyFilterResults();
	if (ldc.answers.length == ldc.questions.length){
		if (ldc.distributionsAfterAnswer.length == 0){
			$("#getresult").removeClass("btn-success");
			$("#getresult").addClass("btn-danger");			
			if ($("#zerodistros").length == 0){
				var error = this.GetSystemValue("zerodistros");
				$("#rightBar").append("<li id='zerodistros' class='list-group-item'><div iclass='alert alert-danger'>"+error+"</div></li>");
			}			
		}else{
			$("#zerodistros").remove();
			$("#getresult").removeClass("btn-danger");
			$("#getresult").removeClass("btn-primary");
			$("#getresult").addClass("btn-success");
		}	
	}
	else{		
		$("#getresult").removeClass("btn-danger");
		$("#zerodistros").remove();
		$("#getresult").removeClass("btn-success");
		$("#getresult").addClass("btn-primary");
	}   
}
function FilterByAnswer(answer){
	var id =/\d+/.exec(answer)[0];
	var questionId = /\d+/.exec($("#"+answer).parent().parent().parent().attr("id"))[0];
	//Search if an question was already answered
	if (ldc.answers.indexOf(id) == -1){
		if ($("#Question_"+questionId+" ul li a[ldc_selected]").length == 0){
			ldc.answers.push(id);
			//Mark the answer
			var header = $("#Question_"+questionId).parent().parent()[0].children[0].id;
			$("#"+header).append("<h4 class='answered'>"+ldc.GetSystemValue("questionanswered").toUpperCase()+"</h4>");
			$("#"+answer+"").append(" <span id='"+answer+"_Selection' class='glyphicon glyphicon-ok'></span>");
			$("#"+answer).attr("ldc_selected","true");	
			$("#"+answer+"_Selection").hover(function(){
				$(this).css("color","darkred");
				$(this).removeClass("glyphicon-ok");
				$(this).addClass("glyphicon-remove");
			});
			$("#"+answer+"_Selection").mouseout(function(){
				$(this).removeClass("glyphicon-remove");
				$(this).addClass("glyphicon-ok");
				$(this).css("color","");
			});
		}
		else{
			//deselect old question					
			$("#Question_"+questionId+" ul li a[ldc_selected] span").remove();				
			$("#Question_"+questionId+" ul li a[ldc_selected]").removeAttr("ldc_selected");
			ldc.answers.splice(ldc.answers.indexOf(id),1);
			//select new one
			ldc.answers.push(id);
			var header = $("#Question_"+questionId).parent().parent()[0].children[0].id;
			$("#"+header).append("<h4 class='answered'>"+ldc.GetSystemValue("questionanswered").toUpperCase()+"</h4>");
			$("#"+answer+"").append(" <span id='"+answer+"_Selection' class='glyphicon glyphicon-ok'></span>");
			$("#"+answer).attr("ldc_selected","true");	
		}		
	}else{
		var header = $("#Question_"+questionId).parent().parent()[0].children[0].id;
		$("#"+header+" h4").last().remove();
		$("#"+answer+" span").remove();
		$("#"+answer).removeAttr("ldc_selected");
		ldc.answers.splice(ldc.answers.indexOf(id),1);
	}
	//Exclude or Include
	ldc.ApplySearch(id);
}
function ApplySearch(id){
	var newArray = [];
	for (var i = 0; i < ldc.distributions.length; i++) {
		var keepDistro = false;
		var distro = ldc.distributions[i];
		var hittedAnswers = 0;		
		for (var x = 0; x< distro.Answers.length; x++) {			
			if (ldc.answers.indexOf(distro.Answers[x]) != -1){
				//The given answer is in the allowed amount
				hittedAnswers++;
			}
			
		};		
		keepDistro = (hittedAnswers == ldc.answers.length);
		if (keepDistro){
			newArray.push(distro);			
		}
		else{
			//console.log(distro.Name + " will not be added");
		}
	}
	ldc.distributionsAfterAnswer = newArray.slice();
	if (ldc.distributionsAfterAnswer.length == 0){
		//console.log("Entering relative mode");	
		ldc.distributionsAfterAnswer = [];
		ldc.distributionsAfterAnswer = ldc.ApplyRelativeResults();
	}
	else{
		//console.log("Entering absolute mode");	
	}
}
function ApplyRelativeResults(){
	//This methods calculates relative results, when there are no 100 % results
	var results = [];
	var count = ldc.answers.length;
	for (var i = ldc.distributions.length - 1; i >= 0; i--) {
		var hits = 0;
		var distro = ldc.distributions[i];
		for (var x = 0; x< distro.Answers.length; x++) {			
			if (ldc.answers.indexOf(distro.Answers[x]) != -1){
				hits++;
			}			
		};	
		if (hits != 0){			
			var percentage = Math.round(100/(count/hits),2);
			var copiedObject = jQuery.extend({}, distro)
			copiedObject.percentage = percentage;			
			results.push(copiedObject);						
		}
	};
	results.sort(compare);
	return results;
}
function compare(a,b) {
  if (a.percentage < b.percentage)
     return 1;
  if (a.percentage > b.percentage)
    return -1;
  return 0;
}
function ApplyFilterResults(){	
	$("#hitCount").html(ldc.distributionsAfterAnswer.length);
	$("#allCount").html(ldc.distributions.length);	
}
function InsertQuestions(){
	for (var i = 0; i < ldc.questions.length; i++) {
		var element= ldc.questions[i];
		var html = htmlInject.replace(new RegExp("{{ID}}", "g"),element.Id);	
		html = html.replace(new RegExp("{{TITLE}}", "g"),(i+1)+". "+element.Text);
		html = html.replace(new RegExp("{{QUESTION}}", "g"),element.Help);
		var subHtml = "<ul >";
		for (var x = 0; x < element.Answers.length; x++) {
			subHtml = subHtml + "<li><a id='Answer_"+element.Answers[x].Id+"'>"+element.Answers[x].Text+"</a></li>";
		}
		var lastQuestion = (i < ldc.questions.length -1) ? false : true;
		subHtml = subHtml + "</ul>";
		if (!lastQuestion){
			var href ="#";

			subHtml += "<a href='#collapse"+i+"' class='btn btn-primary next ldcui' id='nextQuestion'>"+ldc.GetSystemValue("nextQuestion")+"</a>";
		}
		else{
			subHtml +="<a href='#collapse"+i+"' class='btn btn-success ldcui' id='finishTest'>"+ldc.GetSystemValue("getresult")+"</a>";
		}
		html = html.replace(new RegExp("{{CONTENT}}", "g"),subHtml)
		
		$("#accordion").append(html);
		if (!lastQuestion){
			$(".next").click(function(){				
				$(this).parent().parent().parent().next().children().first().trigger("click");
			});
		}		
		else{
			$("#finishTest").click(function(){
			// Add only the distros to the stats if the result was absolute or the percentage was above 20 %
			var relevantDistros = [];
			for(var d=0;d < ldc.distributionsAfterAnswer.length;d++){
				if (!ldc.distributionsAfterAnswer[d].percentage)
					relevantDistros.push(ldc.distributionsAfterAnswer[d]);
				else if (ldc.distributionsAfterAnswer[d].percentage > 20)
					relevantDistros.push(ldc.distributionsAfterAnswer[d]);
			}
                	$.post( "./rest.php", { method: "AddResult", args: JSON.stringify(relevantDistros),lang: ldc.language})
                		.done(function( data ) {
                        		GetResult();
                		});
		        });

		}
		for (var x = 0; x < element.Answers.length; x++) {
			$("#Answer_"+element.Answers[x].Id).click(function(){				
				ldc.FilterByAnswer($(this).attr("id"));
				ldc.PostAnswerClick();				
			});
		}
	};
	$("#loadingHint").fadeOut(function(){
			$("#accordion").fadeIn();
	});	

	$("[data-parent='#accordion']").click(function(){
		if ($(this).attr("href") == "#collapseOne"){
			$("#homelink").fadeOut();
			$("#rightBar").fadeOut();
		}
		else{
			$("#homelink").fadeIn();
			$("#rightBar").fadeIn();
		}
		
	});
}
function Init(){		
    var text = "There are no easter eggs..or maybe..it's classified"; 
	$.post( "./rest.php", { method: "GetSystemVars", args: "[]",lang: this.language })
	.done(function( data ) {
		ldc.systemVars = $.parseJSON(data);		
		ldc.GetDistros();
		ldc.GetQuestions();
		ldc.SetUpUI();	
	});	
}
function NotAnEasterEgg()
{
	$("#homelink").children().first().attr("src","./assets/0002.gif");
	$(".largelogo").attr("src","./assets/0002.gif");
}
function GetDistros(){
	$.post( "./rest.php", { method: "GetDistributions", args: "[]",lang: this.language })
	.done(function( data ) {
		var result = $.parseJSON(data);
		var distributions = [];		
		for (var i = 0; i < result.length; i++) {
			distributions.push(result[i]);
		};	
		ldc.distributions = distributions;
		ldc.distributionsAfterAnswer = ldc.distributions.slice();
		ldc.ApplyFilterResults();
		ldc.UnserializeResult();	
	});
}
function GetQuestions(){
	$.post( "./rest.php", { method: "GetQuestions", args: "[]",lang: this.language })
	.done(function( data ) {
		var result = $.parseJSON(data);
		var questions = [];		
		//console.log(data);
		for (var i = 0; i < result.length; i++) {
			questions.push(result[i]);
		};	
		ldc.questions = questions;
		//console.log(ldc.questions);
		$("#answerCount").text(ldc.questions.length);
		ldc.InsertQuestions();		
	});
}
function CreateResultMatrix(){
	var matrix = {};
	for (var i = ldc.questions.length - 1; i >= 0; i--) {
		var row = ldc.questions[i];	
		for (var y = row.Answers.length - 1; y >= 0; y--) {
			var fittingDistros = [];
			var answer = row.Answers[y].Id;
			if (ldc.answers.indexOf(answer) != -1 || ldc.answers.length == 0){
				for (var x = ldc.distributions.length - 1; x >= 0; x--) {
					var answersDistro = ldc.distributions[x].Answers;					
					if (answersDistro.indexOf(answer) != -1){					
						if (fittingDistros.indexOf(ldc.distributions[x].Name) == -1)
							fittingDistros[ldc.distributions.indexOf(ldc.distributions[x])] = (ldc.distributions[x].Name);
					}
					matrix[row.Text + ": " + row.Answers[y].Text] = fittingDistros;					
				};
			}			
		};		
	};
	return matrix;	
}
function SerializeResult(){
	var result = "";
	for (var i = 0; i < ldc.answers.length; i++) {
		result += ldc.answers[i]; 
		if (i != ldc.answers.length -1)
			result += ",";
	};
	return result;
}
function UnserializeResult(){
	var answers = getUrlVars("answers");
	if (answers.answers === undefined){
		ldc.answers =  [];
	}
	else{
		ldc.answers = answers.answers.split(",");
	}
	for (var i = 0; i < ldc.answers.length; i++) {	
		var id =/\d+/.exec(ldc.answers[i])[0];	
		var answer = "Answer_"+id;
	
		var questionId = /\d+/.exec($("#"+answer).parent().parent().parent().attr("id"))[0];
		var header = $("#Question_"+questionId).parent().parent()[0].children[0].id;
		$("#"+header).append("<h4 class='answered'>"+ldc.GetSystemValue("questionanswered").toUpperCase()+"</h4>");
		$("#"+answer+"").append(" <span id='"+answer+"_Selection' class='glyphicon glyphicon-ok'></span>");
		$("#"+answer).attr("ldc_selected","true");	
		$("#"+answer+"_Selection").hover(function(){
			$(this).css("color","darkred");
			$(this).removeClass("glyphicon-ok");
			$(this).addClass("glyphicon-remove");
		});
		$("#"+answer+"_Selection").mouseout(function(){
			$(this).removeClass("glyphicon-remove");
			$(this).addClass("glyphicon-ok");
			$(this).css("color","");
		});
		ldc.ApplySearch(id);
	};	
	ldc.PostAnswerClick();
	ldc.ApplyFilterResults();
}

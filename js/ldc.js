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
	$("#twitterlink").attr("href","https://twitter.com/share?text="+ldc.GetSystemValue("FindTheRightLinux")+"&url=http://distrochooser.0fury.de/?r=tw&hashtags=distrochooser,linux") ;
	$("#getresult").click(function(){
		$.post( "./rest.php", { method: "AddResult", args: JSON.stringify(ldc.distributionsAfterAnswer),lang: ldc.language})
		.done(function( data ) {		
			GetResult();
		});	
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
	for (var i = 0; i < ldc.distributionsAfterAnswer.length; i++) {
		var item = "";
		item = "<div class='panel panel-default'>";
		item = item + "<div class='panel-heading'>"+ldc.distributionsAfterAnswer[i].Name+"</div>";
		item = item + "<div class='panel-body'>";
		item = item + "<img class='linuxlogo' src='"+ldc.distributionsAfterAnswer[i].Image+"'></img>"+ldc.distributionsAfterAnswer[i].Description+"</div>";

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
		var tooltip = '<a href="#" type="button" class="questionbtn" data-toggle="popover" title="" data-content="'+key+'" data-trigger="focus" tabindex="0"><i class="glyphicon glyphicon-question-sign"></i></a>';		
		row +="<td>"+tooltip+"</td>";	
		var horIndex = 2;	
		for (var i = ldc.distributions.length - 1; i >= 0; i--) {	
			var name = $('#matrix th:nth-child('+horIndex+') div').first().html();
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
	var questionId = /\d+/.exec($("#"+answer).parent().parent().attr("id"))[0];
	//Search if an question was already answered
	//console.log(answer);
	//TODO: funzr noch nicht richtig apt-get problematik
	if (ldc.answers.indexOf(id) == -1){
		if ($("#Question_"+questionId+" ul a[ldc_selected]").length == 0){
			ldc.answers.push(id);
			//Mark the answer
			var header = $("#Question_"+questionId).parent().parent()[0].children[0].id;
			$("#"+header).append("<h4 class='answered'>"+ldc.GetSystemValue("questionanswered").toUpperCase()+"</h4>");
			$("#"+answer+" li").append(" <span id='"+answer+"_Selection' class='glyphicon glyphicon-ok'></span>");
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
	}else{
		//TODO: Das verwirft alte antwroten...
		var header = $("#Question_"+questionId).parent().parent()[0].children[0].id;
		$("#"+header+" h4").last().remove();
		$("#"+answer+" li span").remove();
		$("#"+answer).removeAttr("ldc_selected");
		ldc.answers.splice(ldc.answers.indexOf(id),1);
	}
	console.log("id: "+id);
	//Eins von denen baut scheiße
	
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
	}
	ldc.distributionsAfterAnswer = newArray.slice();
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
			subHtml = subHtml + "<a   id='Answer_"+element.Answers[x].Id+"'><li>"+element.Answers[x].Text+"</li></a>";
		}
		subHtml = subHtml + "</ul>";
		html = html.replace(new RegExp("{{CONTENT}}", "g"),subHtml)
		$("#accordion").append(html);
		for (var x = 0; x < element.Answers.length; x++) {
			$("#Answer_"+element.Answers[x].Id).click(function(){				
				ldc.FilterByAnswer($(this).attr("id"));
				ldc.PostAnswerClick();				
			});
		}
	};	
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
    console.log(text);
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
		var answer = "Answer_"+ldc.answers[i];
		var id =/\d+/.exec(answer)[0];
		var questionId = /\d+/.exec($("#"+answer).parent().parent().attr("id"))[0];
		var header = $("#Question_"+questionId).parent().parent()[0].children[0].id;
		$("#"+header).append("<h4 class='answered'>"+ldc.GetSystemValue("questionanswered").toUpperCase()+"</h4>");
		$("#"+answer+" li").append(" <span id='"+answer+"_Selection' class='glyphicon glyphicon-ok'></span>");
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

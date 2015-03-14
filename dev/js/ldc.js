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
	    if (value != "")
			$(this).html(value);
	});
	$("#answeredCount").text("0");
	$("#welcomeTextHeader").trigger("click");
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
		item = item + "<div class='panel-body'>"+ldc.distributionsAfterAnswer[i].Description+"</div>";

		item = item + "<div class='panel-footer properties hidden-xs'><a target='_blank' href='"+ldc.distributionsAfterAnswer[i].Homepage+"'>Website</a></div>";
		item = item + "</div>";
		$("#ResultContent").append(item);
	};	
	if (ldc.distributionsAfterAnswer.length == 0){
		$("#ResultContent").text(ldc.GetSystemValue("NoResults"));
	}
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
	console.clear();
	console.log("Nothing to do here!");
	$.post( "./rest.php", { method: "GetSystemVars", args: "[]",lang: this.language })
	.done(function( data ) {
		ldc.systemVars = $.parseJSON(data);		
		ldc.GetDistros();
		ldc.GetQuestions();
		ldc.SetUpUI();	
	});	
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
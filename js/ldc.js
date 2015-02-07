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
	this.Exclude = Exclude;
	this.Include = Include;
	this.PostAnswerClick = PostAnswerClick;
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
}
function ApplyTitle(){
	document.title = this.GetSystemValue("Title");
}
function SwitchLanguage(language){
	ldc.language = language;
	ldc.Init();
}
function PostAnswerClick(){
	$("#answeredCount").text(ldc.answers.length);
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
	var questionId = /\d+/.exec($("#Answer_1").parent().parent().attr("id"))[0];
	//Search if an question was already answered
	if (ldc.answers.indexOf(id) == -1){
		if ($("#Question_1 ul a[ldc_selected]").length == 0){
			ldc.answers.push(id);
			//Mark the answer
			$("#"+answer+" li").append(" <span class='glyphicon glyphicon-ok'></span>");
			$("#"+answer).attr("ldc_selected","true");			
		}		
	}else{
		$("#"+answer+" li span").remove();
		$("#"+answer).removeAttr("ldc_selected");
		ldc.answers.splice(ldc.answers.indexOf(id));
	}


	//Exclude
	ldc.Exclude(id);
	//Include
	ldc.Include(id);
}
function Exclude(id){
	for (var i = 0; i < ldc.distributionsAfterAnswer.length; i++) {
		var keepDistro = false;
		var distro = ldc.distributionsAfterAnswer[i];
		for (var x = 0; x< distro.Answers.length; x++) {			
			if (distro.Answers[x]== id){
				keepDistro = true;
				break;
			}
		};		
		if (!keepDistro){
			ldc.distributionsAfterAnswer.splice(i,1);
		}
	}
}
function Include(id){
	for (var i = 0; i < ldc.distributions.length; i++) {
		var distro = ldc.distributions[i];
		if (ldc.distributionsAfterAnswer.indexOf(distro) == -1){
			var readd = true;
			for (var x = 0; x < ldc.answers.length;x++){
				if (distro.Answers.indexOf(ldc.answers[x]) == -1){
					readd = false;
					break;
				}
			}
			if (readd){
				ldc.distributionsAfterAnswer.push(distro);
			}
		}	
	}
}
function InsertQuestions(){
	for (var i = 0; i < ldc.questions.length; i++) {
		var element= ldc.questions[i];
		console.log(element);
		var html = htmlInject.replace(new RegExp("{{ID}}", "g"),element.Id);	
		html = html.replace(new RegExp("{{TITLE}}", "g"),element.Text);
		html = html.replace(new RegExp("{{QUESTION}}", "g"),element.Help);
		var subHtml = "<ul>";
		for (var x = 0; x < element.Answers.length; x++) {
			subHtml = subHtml + "<a href = '#' id='Answer_"+element.Answers[x].Id+"'><li>"+element.Answers[x].Text+"</li></a>";
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
	});
}
function GetQuestions(){
	$.post( "./rest.php", { method: "GetQuestions", args: "[]",lang: this.language })
	.done(function( data ) {
		var result = $.parseJSON(data);
		var questions = [];		
		for (var i = 0; i < result.length; i++) {
			questions.push(result[i]);
		};	
		ldc.questions = questions;
		$("#answerCount").text(ldc.questions.length);
		ldc.InsertQuestions();
	});
}
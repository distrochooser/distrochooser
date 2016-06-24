<html  id="app">
<head>
<title>{{ ldc.Title }}</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
<link rel="stylesheet" href="https://bootswatch.com/cosmo/bootstrap.min.css">
</head>
<body>
<noscript>
	jkfalsf
</noscript>
<div class="container">
<div class="row">

<?php include "./static/about.php";?>
<div class="col-lg-3">
	<div class="row">
		<!--<a class ="hidden-xs" id ="homelink" href="index.php"><img src="./assets/ldc2.png"></img></a>-->					
			<div class="visible-lg">			
			<a class="btn btn-primary button-left-nav ldcui privacy" id="privacyMenuEntry" href="./static/privacy.php">Datenschutz</a>					  
			<span class="spacer"></span>
			<a class="btn btn-primary button-left-nav ldcui contact" id="contactMenuEntry" href="./static/contact.php">Kontakt</a>					  
			<span class="spacer"></span>				
  		<a class="btn btn-primary button-left-nav ldcui contact" id="about"  data-toggle="modal" data-target="#myModal">Über den Distrochooser</a>     
			<span class="spacer"></span>	

			<a class="btn btn-primary button-left-nav" target="_blank" href="http://0fury.de"><img class="vendor" alt="0fury.de" src="./assets/0fury.ico"><span class="ldcui" id="Vendor">Ein Projekt von</span>  0fury.de</a>				  
				
			<a title="Zur deutschen Version wechseln" href="?l=1"><img class="flag" src="./assets/langs/de.png" alt="Deutsch"></a>
			<a title="Switch to english version" href="?l=2"><img class="flag" src="./assets/langs/gb.png" alt="English"></a>
			<p>
		{{ ldc.version }}
</p>
						</div>
			<div class="hidden-lg">					
				<!--<ul class="nav nav-pills" role="tablist">				 
				</ul>-->
				<nav class="navbar navbar-default">
				  <div class="container-fluid">
				    <div class="navbar-header">
				      <a class="navbar-brand" href="index.php">
				        <img alt="Brand" src="./assets/mobile.png" class="brand"> 
				      </a>		
				      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#example-navbar-collapse">
				         <span class="sr-only">Toggle navigation</span>
				         <span class="icon-bar"></span>
				         <span class="icon-bar"></span>
				         <span class="icon-bar"></span>
				      </button>		  			      
				    </div>	
				      <div class="collapse navbar-collapse" id="example-navbar-collapse">
				      <ul class="nav navbar-nav">
				         <li role="presentation"> <a class="ldcui sshare" href="#" id="share">Teilen</a></li>
						 <li role="presentation"> <a class="ldcui sprivacy" id="privacy" href="./static/privacy.php">Datenschutz</a></li>
						 <li role="presentation"> <a class="ldcui scontact" id="contact" href="./static/contact.php">Kontakt</a></li>
				      </ul>
				   </div> 				
				  </div>
				</nav>
			</div>
	</div>


</div>
<div class="col-lg-6 main">
<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="false">
	<div v-for="question in ldc.questions" class="panel panel-default">
		<div class="panel-heading" role="tab" id="header{{question.Id}}">
			<h4 class="panel-title">
				<a class="question-header"  role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse{{question.Id}}" aria-expanded="true" aria-controls="collapse{{question.Id}}">
					{{ question.Text }} 
				</a>
			</h4>	
			<a href="#" class="glyphicon glyphicon-star mark-important" v-bind:class="{'important':question.Important,'hidden':question.Answers.length == 0}" data-id="{{question.Id}}" v-on:click="makeImportant($event)"></a>
			</div>
			<div id="collapse{{question.Id}}" class="panel-collapse collapse question" role="tabpanel" aria-labelledby="header{{question.Id}}">
				<div class="panel-body">
					{{ question.HelpText }}
					<div v-if="question.Answers.lenght != 0">
					<ul>
						<li v-for="answer in question.Answers" v-bind:class="{ 'selected': answer.Selected}">
							<a href="#" data-id="{{answer.Id}}" v-on:click="addAnswer($event)" v-bind:class="{'singleanswer': question.SingleAnswer,'mutlianswer': !question.SingleAnswer}">{{ answer.Text }}</a>
						</li>
						</div>
					</ul>
				</div>
			</div>
		</div>
		<div class="panel panel-default" v-bind:class="{'hidden':answeredQuestionsCount==0}">
		<div class="panel-heading" role="tab" id="header-result">
			<h4 class="panel-title">
				<a class="result-header" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse-result" aria-expanded="true" aria-controls="collapse-result">
				Ergebnis
				</a>
			</h4>	
		 </div>
			<div id="collapse-result" class="panel-collapse collapse question" role="tabpanel" aria-labelledby="header-result">
				<div class="panel-body">
				<div class="rating" v-if="commentSent==false">
					<p class="ldcui rating-text">Wie zufrieden bist Du mit dem Ergebnis?</p>
					 <div id="rating-stars"></div>
					<textarea v-model="comment" debounce="300" class="form-control"></textarea>
					 <button id="submit-comment" v-on:click="publishRating($event)" >Absenden</button>
				</div>
				<div class="rating-sent" v-if="commentSent==true">
					Danke für die Bewertung!
				</div>
					<div v-for="distro in distributions | orderBy 'Percentage' -1">
							<div class="panel panel-default distribution" style="border-color:{{ distro.Color }}">
								<div class="panel-heading" style="background-color:{{ distro.Color }}">{{ distro.Name }}: {{ distro.Percentage }}%</div>
								<div class="panel-body">
								  <img class="distro-logo" src="{{ distro.Image }}"/>{{{ distro.Description }}}
								</div>
							</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	
</div>
<div class="col-md-1">
</div>
<div class="col-lg-2">
<div class="row right-box">				
  <ul class="list-group"  v-bind:class="{'hidden':answeredQuestionsCount==0}">
    <li class="list-group-item"><a class="hidden-xs" id="homelink" href="index.php"><img src="./assets/ldc2alpha.png" alt="Linux Distribution Chooser" style="
     width: 100%;
     "></a></li>
     <li class="list-group-item">
      <span class="badge"><span id="answeredCount" class="ldcui">{{ answeredQuestionsCount }}</span>/ <span class="ldcui" id="answerCount">{{ questionsCount }}</span></span>
      <span class="ldcui" id="answered">Beantwortet</span>
    </li>
    <li class="list-group-item">
      <span class="badge"><span id="hitCount" class="ldcui">{{ distributionsCount }}</span>/ <span class="ldcui" id="allCount">{{ allDistributionsCount }}</span></span>
      <span class="ldcui" id="Suitable">Passend</span>
    </li>
    <li class="list-group-item">
      <a class="btn btn-primary ldcui" id="getresult">Auswerten</a>
    </li>        
  </ul>
</div>
</div>
</div>
</div>

<script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.1.1/jquery.rateyo.min.css">
<!-- Latest compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.1.1/jquery.rateyo.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/flipclock/0.7.8/flipclock.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flipclock/0.7.8/flipclock.min.css">
<script 
src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.25/vue.min.js"></script>
<script src="./ldc.js"></script>
<link href="./ldc.css" rel='stylesheet' type='text/css'>
<script>
	$(document).ready(function(){
		$('.question-header:first').trigger("click");
		$("#getresult").click(function(){
			$(".question:last").collapse("show")
			location.href="#collapse-result";
		});
		$("#rating-stars").rateYo({
			rating: 0.0
		});
		$('#myModal').on('show.bs.modal', function (e) {
			TestCount();
		})
		
	});
</script>

</body>
</html>
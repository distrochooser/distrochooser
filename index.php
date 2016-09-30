<html  id="app">
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta charset="UTF-8">
	<meta name="description" lang = "de"  content ="Die Linux Auswahlhilfe hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden.">
	<meta name="description" lang = "en"  content ="The Linux Distribution Chooser helps you to find the suitable Distribution for you!">
	<meta name="keywords" content="Linux, Linux Chooser, Linux Distribution Chooser, Linux Auswahlhilfe, Linux Auswahl, Alternative to Windows, Linux Comparison, Linux Vergleich, Vergleich, Auswahlhilfe, Alternative zu Windows">
	<meta name="google-site-verification" content="nqtoKAtXX7xTNyddaEGkkYtgpc0pc0b-wigel0Acy5c" />
	<meta name="msvalidate.01" content="8165DC81CC6E5D6805201B58C5596403" />
	<meta name="generator" content="LDC 2016">

	<title>Distrochooser</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
	<link rel="stylesheet" href="https://bootswatch.com/lumen/bootstrap.min.css">
	<link href="./ldc.css" rel='stylesheet' type='text/css'>
</head>
<body>
	<div class="loader visible" v-bind:class="{'visible':!loaded,'hidden':loaded}">
		<p>	
			<span  class="text">	
				<?php echo (isset($_GET["l"]) && $_GET["l"] === "en") ? "The Linux Distribution Chooser helps you to find the suitable Distribution for you!": "Die Linux Auswahlhilfe hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden." ;?>	
			</span>
		</p>
	</div>
	<div class="container main-container hidden"  v-bind:class="{'hidden':!loaded,'visible':loaded}">
		<div class="row">

			<?php include "./static/about.php";?>
			<div class="col-lg-3">
				<div class="row">
					<!--<a class ="hidden-xs" id ="homelink" href="index.php"><img src="./assets/ldc2.png"></img></a>-->					
					<div class="visible-lg">			

						<a class="btn btn-primary button-left-nav ldcui contact" id="about"  data-toggle="modal" data-target="#about">{{ text('About') }}r</a>     
						<span class="spacer"></span>	

						<a class="btn btn-primary button-left-nav" target="_blank" href="http://0fury.de"><img class="vendor" alt="0fury.de" src="./assets/0fury.ico">
						<span class="ldcui" id="Vendor">Ein Projekt von</span>  0fury.de</a>				  

						<a title="Zur deutschen Version wechseln" href="?l=1"><img class="flag" src="./assets/langs/de.png" alt="Deutsch"></a>
						<a title="Switch to english version" href="?l=2"><img class="flag" src="./assets/langs/gb.png" alt="English"></a>

						<footer class="visible-lg">
							<a class="ldcui privacy" id="privacyMenuEntry" href="./static/privacy.php"></a>	
							<a class="ldcui contact" id="contactMenuEntry" href="./static/contact.php"></a>		

						</footer>
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
							<li role="presentation"> 
								<a class="flags" title="Zur deutschen Version wechseln" href="?l=1">
									<img class="flag" src="./assets/langs/de.png" alt="Deutsch">
								</a>

								<a class="flags" title="Switch to english version" href="?l=2">
									<img class="flag" src="./assets/langs/gb.png" alt="English">
								</a>
							</li>
							<li role="presentation"> 
							</li>
							<li role="presentation"> <a class="ldcui sprivacy" id="privacy" href="./static/privacy.php"></a></li>
							<li role="presentation"> <a class="ldcui scontact" id="contact" href="./static/contact.php"></a></li>
						</ul>
					</div> 				
				</div>
			</nav>
		</div>
	</div>


</div>
<div class="col-lg-6 main">
	<div class="alert alert-danger" v-if="isOldTest">
		{{ text("oldTest"); }}
	</div>
	<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="false">
		<div v-for="question in ldc.questions" class="panel panel-default">
			<div class="panel-heading" role="tab" id="header{{question.Id}}">
				<h4 class="panel-title">
					<a class="question-header" ldc-header="{{question.Id}}" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse{{question.Id}}" aria-expanded="true" aria-controls="collapse{{question.Id}}" v-bind:class="{'answered':question.Answered}" >
						<span v-if="question.Number !== -1">{{ question.Number }}. </span>{{ question.Text }} 
					</a>
				</h4>	
				<a href="#" class="glyphicon glyphicon-star mark-important" v-bind:class="{'important':question.Important,'hidden':question.Answers.length == 0}" data-id="{{question.Id}}" v-on:click="makeImportant($event)"></a>
			</div>
			<div id="collapse{{question.Id}}" class="panel-collapse collapse question" role="tabpanel" aria-labelledby="header{{question.Id}}">
				<div class="panel-body">
					{{{ question.HelpText }}}
					<div v-if="question.Answers.lenght != 0">
						<ul v-bind:class="{'multi':!question.SingleAnswer,'single':question.SingleAnswer,'image':!question.IsText }">
							<li v-if="!question.IsText" v-for="answer in question.Answers" v-bind:class="{ 'selected': answer.Selected,'imageAnswer':!question.IsText }">

								<a href="#" data-id="{{answer.Id}}" v-on:click="addAnswer($event)" v-bind:class="{'singleanswer': question.SingleAnswer,'mutlianswer': !question.SingleAnswer}">				
									<img v-if="answer.IsText == false" v-bind:src="answer.Image" class="image" data-id="{{answer.Id}}"  v-bind:class="{ 'selected': answer.Selected }"  title="{{ answer.Text }}">				
								</a>
							</li>
							<li v-if="question.IsText" v-for="answer in question.Answers" v-bind:class="{ 'selected': answer.Selected,'imageAnswer':!question.IsText }">				
								<a href="#" data-id="{{answer.Id}}" v-on:click="addAnswer($event)" v-bind:class="{'singleanswer': question.SingleAnswer,'mutlianswer': !question.SingleAnswer}">				
									{{ answer.Text }}
								</a>
							</li>
						</div>
					</ul>
					<a href="#" class="btn btn-primary {{ question.Id }}-next" data-id="{{ question.Id }}-next" v-on:click="nextTrigger($event)" >
						{{ question.ButtonText }}
					</a>
				</div>
			</div>
		</div>			
		<a href="ResultAnchor"></a>
		<div class="panel panel-default">
			<div class="panel-heading" role="tab" id="header-result">
				<h4 class="panel-title">
					<a class="result-header ldcui" id="Result" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse-result" aria-expanded="true" aria-controls="collapse-result" v-on:click="addResult">

					</a>
				</h4>	
			</div>
			<div id="collapse-result" class="panel-collapse collapse question result-collapse" role="tabpanel" aria-labelledby="header-result">
				<div class="panel-body" v-if="distributionsCount > 0">
					<a href="#" id="rating-anchor"></a>

					<div class="rating" v-if="commentSent==false">
						<p class="ldcui rating-text" id="ResultRatingHeader">Wie zufrieden bist Du mit dem Ergebnis?</p>
						<div class="share-link" v-if="currentTestLoading">
							<i class="fa fa-spin fa-circle-o-notch"></i>
						</div>
						<div class="share-link" v-if="!currentTestLoading">
							<input type="text" class="form-control" value="{{shareLink}}">
						</div>
						<div id="rating-stars"></div>
						<textarea v-model="comment" debounce="300" class="form-control" placeholder="{{ text('comment') }}"></textarea>
						<button id="submit-comment" v-on:click="publishRating($event)" class="btn btn-primary ldcui"></button>
						<div class="social" v-if="currentTestLoading">
							<i class="fa fa-spin fa-circle-o-notch"></i>
						</div>
						<div class="social" v-if="!currentTestLoading">
							<div>
								<a href="https://twitter.com/share?url={{shareLink}}&hashtags=distrochooser,linux&via=distrochooser"><i class="fa fa-twitter"></i></a>
								<a href="https://www.facebook.com/sharer/sharer.php?u={{shareLink}}"><i class="fa fa-facebook"></i></a>
								<a href="https://plus.google.com/share?url={{shareLink}}"><i class="fa fa-google-plus"></i></a>
								<a href="https://github.com/squarerootfury/distrochooser"><i class="fa fa-github"></i></a>
							</div>
						</div>
					</div>
					<div>
					</div>
					<div class="you" style="display:none;">
						{{{ text }}}
					</div>				
					<div class="rating-sent" v-if="commentSent==true">
						Danke für die Bewertung!
					</div>
					<div v-for="distro in distributions | orderBy 'Percentage' -1">
						<div class="panel panel-default distribution">
							<div class="panel-heading" >
								{{ distro.Name }}: {{ distro.Percentage }}%
								<a class="link" href="{{ distro.Website }}">Website</a>
								<a class="link" href="./detail.php?id={{distro.Id}}&l={{ getLanguageKey() }}">Details</a>
							</div>
							<div class="panel-body">
								<p>
									<img class="distro-logo" v-bind:src = "distro.Image" />{{{ distro.Description }}}
								</p>
								<div class="form-group">
									<h4 class="panel-title">
										Warum {{ distro.Name }}?
									</h4>
									<p class="tags">
										<span v-for="tag in distro.Tags" track-by="$index">
											<i class="fa" v-bind:class="{'fa-question':!isTagChoosed(tag),'fa-check':isTagChoosed(tag)}" v-bind:title="text('doesntfit')"  v-if="!isTagChoosed(tag)"></i>
											<i class="fa" v-bind:class="{'fa-check':isTagChoosed(tag)}" v-if="isTagChoosed(tag)" v-bind:title="text('fits')"></i>
											{{ getTagTranslation(tag)}}													
										</span>
									</p>
								</div>
							</div>
							<div class="panel-footer">
								<a class="link" href="{{ distro.TextSource }}">Text</a>
								<a class="link" href="{{ distro.ImageSource }}">Logo</a>
							</div>
						</div>
					</div>
					<div class="panel-body" v-if="distributionsCount == 0">
						<a href="#" id="rating-anchor"></a>
						<p>{{ noResultText }}</p>
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
						width: 100%;v
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
							<a class="btn btn-primary ldcui" id="getresult" v-on:click="addResult" >{{ text('getresult') }}</a>
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
	<script 
	src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.25/vue.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.2.2/Chart.min.js"></script>
	<script src="https://cdn.jsdelivr.net/vue.resource/0.9.1/vue-resource.min.js"></script>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">
	<script src="./ldc.js"></script>
	<script src="./ui.js"></script>
	<script>
		$(document).ready(function(){
			$('.question-header:first').trigger("click");
			$("#getresult").click(function(){
				$(".question:last").collapse("show")
			});
			$(".question:last").on('shown.bs.collapse', function () {
				window.scrollTo(0, $("#rating-anchor").position().top);
			});
			$("#rating-stars").rateYo({
				rating: 0.0
			});
		});
	</script>

</body>
</html>
<?php
	$header = [
		"cdn" => [
			"js" => [],
			"css" => [
				"https://bootswatch.com/lumen/bootstrap.min.css",
				"https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.1.1/jquery.rateyo.min.css",
				"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
			]
		],
		"local" => [
			"js" => [],
			"css" => [
				"./3rdparty/bootstrap.min.css",
				"./3rdparty/gfonts.css",
				"./3rdparty/font-awesome.min.css",
				"./3rdparty/jquery.rateyo.min.css"
			]
		]
	];
	$footer = [
		"cdn" => [
			"js" => [
				"https://code.jquery.com/jquery-2.2.4.min.js",
				"https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js",
				"https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.1.1/jquery.rateyo.min.js",
				"https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.25/vue.js",
				"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.2.2/Chart.min.js",
				"https://cdn.jsdelivr.net/vue.resource/0.9.1/vue-resource.min.js"
			],
			"css" => []
		],
		"local" => [
			"js" => [
				"./3rdparty/jquery-2.2.4.min.js",
				"./3rdparty/bootstrap.min.js",
				"./3rdparty/jquery.rateyo.min.js",
				"./3rdparty/vue.js",
				"./3rdparty/Chart.min.js",
				"./3rdparty/vue-resource.min.js"
			],
			"css" => []
		]
	];
	function echoStyles($data){
		$source = "local";//((isset($_SERVER['HTTP_DNT']) && $_SERVER['HTTP_DNT'] == 1) || isset($_GET["nocdn"])) ? "local" : "cdn" ;
		$jsPattern = "<script src=\"%s\"></script>\n";
		$cssPattern = "<link rel=\"stylesheet\" href=\"%s\">\n";
		foreach($data[$source] as $prop => $files){
			if (count($files) > 0){
				if ($prop === "js"){
					foreach($files as $file){
						echo sprintf($jsPattern,$file);
					}
				}else{
					foreach($files as $file){
						echo sprintf($cssPattern,$file);
					}
				}
			}
		}
	}

?>
<html id="app">
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta charset="UTF-8">
	<meta name="description" lang = "de"  content ="Der Distrochooser hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden.">
	<meta name="description" lang = "en"  content ="The distrochooser helps you to find the suitable Distribution for you!">
	<meta name="keywords" content="Linux, Distrochooser, Linux Chooser, Linux Distribution Chooser, Linux Auswahlhilfe, Linux Auswahl, Alternative to Windows, Linux Comparison, Linux Vergleich, Vergleich, Auswahlhilfe, Alternative zu Windows">
	<meta name="theme-color" content="#158cba">
	<meta property="og:title" content="Distrochooser" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://distrochooser.de" />
	<meta property="og:image" content="https://distrochooser.de/assets/tux.png" />
	<meta property="og:image:type" content="image/png" />
	<meta property="og:image:width" content="500" />
	<meta property="og:image:height" content="253" />
	<meta property="og:description" content="<?php echo  isset($_GET["l"]) && $_GET["l"] === "2" ? "The distrochooser helps you to find the suitable Distribution for you!" : "Der Distrochooser hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden.";?>" />
	<meta property="og:locale" content="<?php echo isset($_GET["l"]) && $_GET["l"] === "2" ? 'en_GB' : 'de_DE';?>" />
	<meta property="og:locale:alternate" content="<?php echo isset($_GET["l"]) && $_GET["l"] === "2" ? 'de_DE' : 'en_GB';?>" />

	<meta name="twitter:card" content="summary" />
	<meta name="twitter:site" content="@distrochooser" />
	<meta name="twitter:title" content="Distrochooser" />
	<meta name="twitter:description" content="<?php echo  isset($_GET["l"]) && $_GET["l"] === "2" ? "The distrochooser helps you to find the suitable Distribution for you!" : "Der Distrochooser hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden.";?>" />
	<meta name="twitter:image" content="https://distrochooser.de/assets/tux.png" />
	<meta name="google-site-verification" content="nqtoKAtXX7xTNyddaEGkkYtgpc0pc0b-wigel0Acy5c" />
	<meta name="msvalidate.01" content="8165DC81CC6E5D6805201B58C5596403" />
	<meta name="generator" content="LDC 2017">
	<link rel="icon" href=favicon.ico type="image/x-icon" >
	<title>Distrochooser</title>
	<?php
		echoStyles($header);
	?>
	<script>
		window.vm = null;
	</script>
	<link href="./ldc.css" rel='stylesheet' type='text/css'>
</head>
<body>
	<div class="loader visible" v-bind:class="{'visible':!loaded,'hidden':loaded}">
		<p class="hidden-xs">
			<span class="loader-image-wrapper"><img src="./assets/mobile.png"></span>
		</p>
		<noscript>
			<div class="well noscript">
				Der Distrochooser benutzt JavaScript, um zu funktionieren. JavaScript ist ein integraler Bestandteil des Internets (geworden). Ohne JavaScript ist eine Software wie der Distrochooser schlicht nicht möglich.
				<hr>
				The Distrochooser needs enabled JavaScript. JavaScript had become an important part of web technologies. A software like the Distrochooser is not possible without JavaScript.
				<hr>
				<a href="https://distrochooser.de/static/privacy.html">Datenschutz | Privacy</a>
				<br>
				<a href="https://distrochooser.de/static/contact.html">Kontakt | Contact</a>
			</div>
		</noscript>
	</div>
	<div class="container main-container hidden"  v-bind:class="{'hidden':!loaded,'visible':loaded}">
		<div class="row">
			<?php include "./static/about.html";?>
			<div class="col-lg-3">
				<div class="row">
					<div class="visible-lg">

						<a class="btn btn-primary button-left-nav contact" id="about"  data-toggle="modal" data-target="#about">{{ text('about') }}</a>
						<span class="spacer"></span>

						<a class="btn btn-primary button-left-nav" target="_blank" href="http://0fury.de"><img class="vendor" alt="0fury.de" src="./assets/0fury.ico">
						<span>{{ text('Vendor') }}</span>  0fury.de</a>

						<a title="Zur deutschen Version wechseln" href="?l=1"><img class="flag" src="./assets/langs/de.png" alt="Deutsch"></a>
						<a title="Switch to english version" href="?l=2"><img class="flag" src="./assets/langs/gb.png" alt="English"></a>
						<ul class="list-group col-lg-9 other-users">
								<li class="list-group-item" v-for="result in otherUserResults" v-if="result.stars > 0 || result.comment !== ''">
									<div>
											<i class="fa fa-user"></i> {{ text('a') }} {{result.os}}-User {{ text('comments') }}:
									</div>
									<i v-for="star in result.stars"class="fa fa-star" aria-hidden="true"></i>
									<span class="result-comment" :title="result.comment ">{{ result.comment === "" ? "" : "“" + (result.comment >= 200 ? result.comment.substring(0,200) +"..." : result.comment )+ "“"}}</span>
								</li>
								</li>
						</ul>
						<footer class="visible-lg">
							<a href="./static/privacy.html">{{ text('privacy') }}</a>
							<a href="./static/contact.html">{{ text('contact') }}</a>
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
							<li role="presentation"> <a class="sprivacy" id="privacy" href="./static/privacy.php">{{ text('privacy') }}</a></li>
							<li role="presentation"> <a class="scontact" id="contact" href="./static/contact.php">{{ text('contact') }}</a></li>
						</ul>
					</div>
				</div>
			</nav>
		</div>
	</div>


</div>
<div class="col-lg-6 main">
	<div class="alert alert-warning" v-if="isOldTest">
		{{ text("oldTest"); }}
	</div>
	<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="false">
		<div v-for="question in questions" class="panel panel-default">
			<div class="panel-heading" role="tab" :id="'header' + question.Id">
				<h4 class="panel-title">
					<a class="question-header" :ldc-header="question.Id" role="button" data-toggle="collapse" data-parent="#accordion" :href="'#collapse' + question.Id" aria-expanded="true" :aria-controls="'collapse' +question.Id" v-bind:class="{'answered':question.Answered}" >
						<span v-if="question.Number !== -1">{{ question.Number }}. </span>{{ question.Text }}
					</a>
				</h4>
				<a href="#" class="fa fa-star mark-important" v-bind:class="{'important':question.Important,'hidden':question.Answers.length=== 0}" :data-id="question.Id" v-on:click.prevent="makeImportant(question)"></a>
			</div>
			<div :id="'collapse' + question.Id" class="panel-collapse collapse question" role="tabpanel" :aria-labelledby="'header' +question.Id">
				<div class="panel-body">
					<p v-html = "question.Number === -1 ? '' : question.HelpText"></p>
					<img class="largelogo" src="./assets/tux.png" v-if="question.Id === 'welcome'">
					<div id="StartText" v-if="question.Id === 'welcome'">
						<span v-html="text('introText')"></span>
						<ul class="list">
							<li>{{ text('can-skip-questions') }} </li>
							<li>{{ text('can-get-result-anytime') }} </li>
							<li>{{ text('can-get-result-anyorder') }}</li>
							<li v-html="text('can-delete')"></li>
							<li v-html="text('can-mark-important')"></li>
						</ul>
					</div>
					<div v-if="question.Answers.length !== 0" class="answer-parent">
						 <div :class="question.SingleAnswer ? 'radio' : 'checkbox'" v-for="answer in question.Answers">
							<p v-if="question.SingleAnswer">
								<input :id="answer.Id" :checked='answer.Selected ' :name="question.Id + '_a'" :data-id="answer.Id" type="radio" v-on:click="updateAnsweredFlag($event,answer,question)"> 
								<label  class="answer-text"  :for="answer.Id" v-bind:class="{ 'selected': answer.Selected }">
									{{ answer.Text }}
								</label>
								<i v-on:click.prevent="showTooltip(translateExcludedTags(answer))" v-if="displayFilters && answer.NoTags.length > 0" class="fa fa-question-circle visible-xs visible-sm" :title = "translateExcludedTags(answer)"></i>				
								<i v-if="displayFilters && answer.NoTags.length > 0" class="fa fa-question-circle hidden-xs hidden-sm" :title = "translateExcludedTags(answer)"></i>				
							</p>
							<p v-if="!question.SingleAnswer">
								<input :id="answer.Id" v-model="answer.Selected" :data-id="answer.Id" :name="question.Id + '_a'" type="checkbox" v-on:change="updateAnsweredFlag($event,answer,question)"> 
								<label class="answer-text" :for="answer.Id" v-bind:class="{ 'selected': answer.Selected }">
									{{ answer.Text }}
								</label>
								<i v-on:click.prevent="showTooltip(translateExcludedTags(answer))" v-if="displayFilters && answer.NoTags.length > 0" class="fa fa-question-circle visible-xs visible-sm" :title = "translateExcludedTags(answer)"></i>
								<i v-if="displayFilters && answer.NoTags.length > 0" class="fa fa-question-circle hidden-xs hidden-sm" :title = "translateExcludedTags(answer)"></i>
							</p>
						</div>
					</div>
					<a href="#" :class="'btn btn-primary ' +question.Id + '-next'" :data-id="question.Id + '-next'" v-on:click.prevent="nextTrigger(question.Id)" >
						{{ lastQuestionNumber=== question.Number ? text("getresult") : (question.Number === -1 ? text("StartTest")   :text("nextQuestion"))}}
					</a>

					<a href="#" class="clear-answer" v-if="question.Answered" v-on:click.prevent="removeAnswers(question)"><i class="fa fa-trash remove-answer"></i> {{ text("clear"); }}</a>
				</div>
			</div>
		</div>
		<div class="panel panel-default" v-show="answered.length > 0">
			<div class="panel-heading" role="tab" id="header-result">
				<h4 class="panel-title">
					<a class="result-header" id="Result" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse-result" aria-expanded="true" aria-controls="collapse-result" v-on:click="addResult">
						{{ text('Result') }}
					</a>
				</h4>
			</div>
			<div id="collapse-result" class="panel-collapse collapse question result-collapse" role="tabpanel" aria-labelledby="header-result">
				<div class="panel-body">
					<a href="#" id="rating-anchor"></a>

					<div class="rating" v-if="commentSent==false && !currentTestLoading">
						<p class="rating-text" id="ResultRatingHeader">{{ text('ResultRatingHeader') }}</p>
						<div class="share-link" v-if="currentTestLoading">
							<i class="fa fa-spin fa-circle-o-notch"></i>
						</div>
						<div class="share-link" v-if="!currentTestLoading">
							<input type="text" class="form-control" :value="shareLink">
						</div>
						<div id="rating-stars"></div>
						<textarea v-model="comment" class="form-control" :placeholder="text('comment')"></textarea>
						<button id="submit-comment" v-on:click="publishRating($event)" class="btn btn-primary">{{ text('submit-comment') }}</button>
						<div class="social" v-if="currentTestLoading">
							<i class="fa fa-spin fa-circle-o-notch"></i>
						</div>
						<div class="social" v-if="!currentTestLoading">
							<div>
								<a :href="'https://twitter.com/share?url=' + shareLink + '&hashtags=distrochooser,linux&via=distrochooser'"><i class="fa fa-twitter"></i></a>
								<a :href="'https://www.facebook.com/sharer/sharer.php?u=' + shareLink"><i class="fa fa-facebook"></i></a>
								<a :href="'https://plus.google.com/share?url=' + shareLink"><i class="fa fa-google-plus"></i></a>
								<a href="https://github.com/cmllr/distrochooser"><i class="fa fa-github"></i></a>
							</div>
						</div>
						<div class="donation" v-if="!currentTestLoading && donationEnabled">
							<span>
								{{ text("donation") }} <i class="fa fa-heart" style="color:#ca1717"></i>
							</span>
							<?php include "./static/donate.html";?>
						</div>
					</div>
					<div>
					</div>
					<div class="you" style="display:none;" v-html="text"></div>
					<div class="rating-sent" v-if="commentSent==true">
						{{ text("thanksForRating") }} 
					</div>
					<div v-for="distro in distributions">
						<div class="panel panel-default distribution" v-show="!distro.Excluded">
							<div class="panel-heading" >
								{{ distro.Name }}: {{ distro.Percentage }}%
								<a class="link" :href="distro.Website">Website</a>
							</div>
							<div class="panel-body">
								<p>
									<img class="distro-logo" v-bind:src = "distro.Image" v-if="currentTest !== -1"/>
									<p v-html="distro.Description"></p>
									<hr>
								</p>
								<div class="form-group">
									<h4 class="panel-title full-width-header">
										 {{ text('why') }} {{ distro.Name }}?
									</h4>
									<p class="tags">
										<span v-for="tag in distro.Tags" track-by="$index" v-if="getTagTranslation(tag) !== tag">
											<i class="fa" v-bind:class="{'fa-question':!isTagChoosed(tag),'fa-check':isTagChoosed(tag)}" v-bind:title="text('doesntfit')"  v-if="!isTagChoosed(tag)"></i>
											<i class="fa" v-bind:class="{'fa-check':isTagChoosed(tag)}" v-if="isTagChoosed(tag)" v-bind:title="text('fits')"></i>
									
											{{ getTagTranslation(tag)}}		
										</span>
									</p>
								</div>
							</div>
							<div class="panel-footer panel-distro-footer">
								<a class="link" :href="distro.TextSource">Text</a>
								<a class="link" :href="distro.ImageSource">Logo</a>
							</div>
						</div>
					</div>
					<div v-for="excluded in excludedDistros" v-if="displayExcluded">
						<div class="panel panel-default distribution">
							<div class="panel-heading" >
								{{ excluded.Name }}: {{ text('excluded') }}
								<a class="link" :href="excluded.Website">Website</a>
							</div>
							<div class="panel-body">
								<img class="distro-logo" v-bind:src = "excluded.Image" v-if="currentTest !== -1" />
								<p v-html="excluded.Description"></p>
								<hr>
								<div class="form-group">
									<h4 class="panel-title">
										{{ text('why') }} {{ text('not') }} {{ excluded.Name }}?
									</h4>
									<p class="tags">
										<span v-for="tag in excluded.Tags" track-by="$index" v-if="(typeof currentTags['!' + tag] !== 'undefined')">
											<i class="fa fa-times" v-bind:title="text('doesntfit')" ></i>
											{{ getTagTranslation(tag)}}
											<span class="exclude-reason">
												<b>{{ text('why') }}?</b> "{{  getExcludingAnswer(tag) }}"
											</span>
										</span>
									</p>
								</div>
							</div>
							<div class="panel-footer panel-distro-footer">
								<a class="link" :href="excluded.TextSource">Text</a>
								<a class="link" :href="excluded.ImageSource">Logo</a>
							</div>
						</div>
					</div>
					<div class="panel-body" v-if="distributionsCount=== 0">
						<a href="#" id="rating-anchor"></a>
						<p>{{ text("NoResults") }}</p>
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
				<ul class="list-group fixed-box"  v-bind:class="{'hidden':answeredQuestionsCount==0}">
					<li class="list-group-item"><a class="hidden-xs" id="homelink" href="index.php"><img src="./assets/ldc2alpha.png" alt="Linux Distribution Chooser" style="
						width: 100%;v
						"></a></li>
						<li class="list-group-item">
							<span class="badge"><span id="answeredCount">{{ answeredQuestionsCount }}</span>/ <span id="answerCount">{{ questionsCount }}</span></span>
							<span id="answered">{{ text('answered') }}</span>
						</li>
						<li class="list-group-item">
							<div class="checkbox">
								<label>
									<input type="checkbox" v-model="displayExcluded">  {{ text('displayExcluded') }}
								</label>
							</div>
							<div class="checkbox">
								<label>
									<input type="checkbox" v-model="displayFilters">  {{ text('displayFilters') }}
								</label>
							</div>
						</li>
						<li class="list-group-item">
							<a class="btn btn-primary" id="getresult" v-on:click="displayResults" >{{ text('getresult') }}</a>
						</li>
						<li class="list-group-item" v-if="currentTestLoading">
							<i class="fa fa-cog fa-spin fa-fw"></i>  {{ this.text("calculating"); }}
						</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
	<?php
		echoStyles($footer);
	?>
	<script src="./ldc.js"></script>
	<script src="./ui.js"></script>
	<script>
		$(document).ready(function(){
			$('.question-header:first').trigger("click");
			$("#rating-stars").rateYo({
				rating: 0.0,
				halfStar: false,
    			fullStar: true
			});
		});
	</script>
</body>
</html>

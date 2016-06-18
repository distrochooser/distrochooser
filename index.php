<html  id="app">
<head>
<title>{{ ldc.Title }}</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
</head>
<body>
<noscript>
	jkfalsf
</noscript>
<div class="container">
<p>Beantwortet: {{ answeredQuestionsCount }}</p>
<ul v-for="distro in distributions">
	{{ distro.Name }} {{ distro.Percentage }}
</ul>
<ul v-for="question in ldc.questions">
	<span v-if="question.Important">
		Wichtig - 	<a href="#" data-id="{{question.Id}}" v-on:click="makeImportant($event)">Unwichtig machen</a>
	</span>
	<span v-if="question.Important === false">
		<a href="#" data-id="{{question.Id}}" v-on:click="makeImportant($event)">Wichtig</a>
	</span>
	<li >
		{{ question.Text }}  - {{ question.HelpText }}
		<ul>
			<li v-for="answer in question.Answers" v-bind:class="{ 'selected': answer.Selected}">
				<a href="#" data-id="{{answer.Id}}" v-on:click="addAnswer($event)" v-bind:class="{'singleanswer': question.SingleAnswer,'mutlianswer': !question.SingleAnswer}">{{ answer.Text }}</a>
			</li>
		</ul>
	</li>
</ul>
<script 
src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.25/vue.min.js"></script>
<script src="./ldc.js"></script>
<link href="./ldc.css" rel='stylesheet' type='text/css'>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
</body>
</html>
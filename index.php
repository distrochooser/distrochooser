<div id="app">
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
	      		<li v-for="answer in question.Answers" v-bind:class="{ 'selected': answer.Selected }">
	      			<a href="#" data-id="{{answer.Id}}" v-on:click="addAnswer($event)">{{ answer.Text }}</a>
	      		</li>
	      	</ul>
	    </li>
    </ul>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.25/vue.min.js"></script>
<script src="./ldc.js"></script>
    <link href="./ldc.css" rel='stylesheet' type='text/css'>
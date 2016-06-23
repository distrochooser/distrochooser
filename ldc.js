var ldc = function(){
	this.backend = "https://distrochooser.de/rest.php";
  this.Title = "Linux Auswahlhilfe",
	this.distributions = [
		{
			"Name":"Ubuntu",
			"Description":{
				"de":"foobar",
				"en":"foobar en"
			},
			"Color":"orange",
			"Homepage":{
				"de":"fjlaksf",
				"en":"jklfasjlf"
			},
			"Tags":[
				"beginner",
        "guinstall"
			],
      "Percentage":0
		},
    {
      "Name":"Arch",
      "Description":{
        "de":"foobar",
        "en":"foobar en"
      },
      "Color":"orange",
      "Homepage":{
        "de":"fjlaksf",
        "en":"jklfasjlf"
      },
      "Tags":[
        "expert","shellinstall"
      ],
      "Percentage":0
    }
	];
	this.questions = [
		{
      "Id":"5ab",
      "Text":"Anfänger",
      "HelpText":"",
      "Important":false,
      "SingleAnswer":false,
      "Answers":[
        {
          "Id":"xf61b",
          "Text":"Ja",
          "Tags":[
            "beginner"
          ],
          "Selected":false
        }
      ]
    },{
      "Id":"5ab2",
      "Text":"Shell oder GUI",
      "HelpText":"",
      "Important":false,
      "SingleAnswer":false,
      "Answers":[
        {
          "Id":"xf61bxxx",
          "Text":"GUI",
          "Tags":[
            "guinstall"
          ],
          "Selected":false
        },
         {
          "Id":"xf61bxx2x",
          "Text":"Shell",
          "Tags":[
            "shellinstall"
          ],
          "Selected":false
        }
      ]
    },
    {
      "Id":"5a2b",
      "Text":"Administrationserfahrung",
      "HelpText":"BLa bla bla",
      "Important":false,
      "SingleAnswer":true,
      "Answers":[
        {
          "Id":"xf261b",
          "Text":"Ja, ich kenne mich aus",
          "Tags":[
            "expert"
          ],
          "Selected":false
        },
        {
          "Id":"xf261b2",
          "Text":"Nein, brutaler Noob",
          "Tags":[
            "beginner"
          ],
          "Selected":false
        }
      ]
    }
	];
};
//Do some init stuff
ldc = new ldc();

vm = new Vue({
  el: '#app',
  data: {
    ldc: ldc, //ldc data instance
    debug: true, //debug mode?
    answered: 0, //the count of answered questions
    tags: {}, //the answered tags
    results: ldc.distributions //the resulting distros
  },
  computed: {
    answeredQuestionsCount: function(){
      this.answered =  this.answeredQuestions();
      return this.answered.length;
    },
    questionsCount: function(){
      return ldc.questions.length;
    },
    currentTags: function(){
      //get the currently answered tags
      this.tags = {};
      for (var i = 0; i < ldc.questions.length;i++){
        var q = ldc.questions[i];
        for(var x = 0;  x < q.Answers.length;x++){
          if (q.Answers[x].Selected === true){
            for(var y = 0 ; y < q.Answers[x].Tags.length; y++){
              var weight = 1;
              var tag = q.Answers[x].Tags[y];
              if (Object.keys(this.tags).indexOf(tag) === -1){
                this.tags[tag] = weight;
              }else{
                this.tags[tag]++;
              }
              if (q.Important){
                this.tags[tag] *=2;
              }
            }
          }
        }
      }
      return this.tags;
    },
    distributionsCount : function (){
      return this.distributions.length;
    },
    allDistributionsCount : function (){
      return ldc.distributions.length;
    },
    distributions : function(){
      //Reset percentages if needed
      if (Object.keys(this.currentTags).length === 0){  
        for (var i = 0; i < ldc.distributions.length;i++){
          ldc.distributions[i].Percentage = 0;
        }
        return ldc.distributions;
      }
      this.results = [];
      var pointSum = 0;
       for (var tag in this.currentTags) {
          var weight = this.currentTags[tag];
          pointSum += weight;
        }
      for (var i = 0; i < ldc.distributions.length;i++){
        var distro = ldc.distributions[i];
        var points = 0;
        var hittedTags = 0;
        for (var tag in this.currentTags) {
          var weight = this.currentTags[tag];
          //get percentage
          if (distro.Tags.indexOf(tag) !== -1){
            points += weight;
            hittedTags++;
          }
        }
        if (points > 0){
          distro.Percentage = Math.round(100 / (pointSum/points),2);
        }else{
          distro.Percentage = 0;
        }
      
        if (distro.Percentage > 0){
          this.results.push(distro);
        } 
      }
      return this.results;
    }
  },
  methods: {
    answeredQuestions: function(){
      var answered = [];
      for (var i = 0; i < ldc.questions.length;i++){
        for(var x = 0;  x < ldc.questions[i].Answers.length;x++){
          if (ldc.questions[i].Answers[x].Selected){
            answered.push(ldc.questions[i]);
            break;
          }
        }
      }
      return answered;
    },
  	getAnswer : function(id){
  		for (var i = 0; i < ldc.questions.length;i++){
  			for(var x = 0;  x < ldc.questions[i].Answers.length;x++){
  				if (ldc.questions[i].Answers[x].Id === id){
  					return ldc.questions[i].Answers[x];
  				}
  			}
  		}
  		return null;
  	},
    getQuestionByAnswer : function(id){
      for (var i = 0; i < ldc.questions.length;i++){
        for(var x = 0;  x < ldc.questions[i].Answers.length;x++){
          if (ldc.questions[i].Answers[x].Id === id){
            return ldc.questions[i];
          }
        }
      }
      return null;
    },
    getQuestion : function(id){
      for (var i = 0; i < ldc.questions.length;i++){
        if (ldc.questions[i].Id === id){
            return ldc.questions[i]   
        }
      }
      return null;
    },
  	selectAnswer : function (id){
  		var answer = this.getAnswer(id);
  		if (answer !== null && !answer.Selected){
  			answer.Selected = true;
  			return answer.Selected;
  		}
  		else if (answer.Selected){
        answer.Selected = false;
  			return answer.Selected;
  		}
      else{
        return false;
      }
  	},
    makeImportant : function (args){
      var question = this.getQuestion(args.srcElement.attributes[2].value);
      if (question !== null){
          if (question.Important){
            question.Important = false;
          }else{
            question.Important = true;
          }
        return question.Important;
      }else{
        return false;
      }
    },
  	addAnswer : function(args){
      var id = args.srcElement.attributes[2].value;
      //prevent multiple answers on singleanswer question
      var parent = this.getQuestionByAnswer(id);
      if (parent !== null && parent.SingleAnswer === true){
        for(var a = 0; a < parent.Answers.length;a++){
            if (parent.Answers[a].Selected === true && parent.Answers[a].Id !== id){
              this.nomultipleAnswersAllowed();
              return false;
            }
        }
      }
  		var answer = this.selectAnswer(args.srcElement.attributes[2].value);
  		return answer;
  	},
    nomultipleAnswersAllowed : function(){
      alert("das ist nicht erlaubt");
    }
  }
})
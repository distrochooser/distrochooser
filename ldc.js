Vue.http.options.emulateJSON = true;
vm = new Vue({
  el: '#app',
  data: {
    debug: true, //debug mode?
    answered: 0, //the count of answered questions
    currentTags: {}, //the answered tags
    results: null, //the resulting distros
    comment: "", //the user's comment for the result
    commentSent: false,
    testCount: 0,
    visitorCount: 0,
    loaded: false,
    i18n: null,
    firstQuestionNumber:1,
    lastQuestionNumber: -1,
    currentTestLoading: false,
    currentTest: -1,
    deniedWhy: [],
    isOldTest:false,
    donationEnabled:false,
    displayExcluded:true,
    displayFilters: true,
    otherUserResults:[],
    givenAnswers:[], //stores the currently given answers to avoid double iteration at getCurrentTags()
    modalOpen:false,
    version: "3.0 (2016)",
    backend:"https://beta.distrochooser.de/rest.php?json&ldc3",
    lang:"de",
    rawDistros: [],
    questions: [
      {
        "Id":"welcome",
        "Text":"",
        "HelpText":"",
        "Important":false,
        "SingleAnswer":false,
        "Answers":[
        ],
        "Number":-1,
        "ButtonText":""
      }
    ],
    langs: ["de","en"]
  },
  created: function(){
    console.log("  _     ___     ___   ____");
    console.log(" | |   |   \\   / __| |__ /");
    console.log(" | |__ | |) | |(__    |_ \\ ");
    console.log(" |____ |___/   \\___| |___/ ");
    console.log("Starting Linux Distribution Chooser "+this.version);
    console.log("Started: " + new Date());
    this.init();
    this.getStatistics();
    setTimeout(this.getRatings, 10000);
  },
  computed: {
    langCode: function(){
      var index = this.langs.indexOf(this.lang);
      return index !== -1 ? index + 1 : 1; 
    },
    shareLink : function(){
      var baseUrl = "https://beta.distrochooser.de/?l="+this.langCode;

      if (this.currentTest === -1){
        return baseUrl;
      }
      return baseUrl+ "&test="+this.currentTest;
    },
    ratingSent : function (){
        return false;
    },
    answeredQuestionsCount: function(){
      this.answered =  this.answeredQuestions();
      return this.answered.length;
    },
    questionsCount: function(){
      var count = 0;
      for(var i = 0; i < this.questions.length;i++){
        if (this.questions[i].Answers.length !== 0){
          count++;
        }
      }
      return count;
    },
    excludedDistros : function(){
      var distros =  [];
      for(var i=0;i<this.rawDistros.length;i++){
        if (this.rawDistros[i].Excluded){
          distros.push(this.rawDistros[i]);
        }
      }
      return distros;
    },
    distributions : function(){
      //Reset percentages if needed
      if (Object.keys(this.currentTags).length === 0){
        for (var i = 0; i < this.rawDistros.length;i++){
          this.rawDistros[i].Percentage = 0;
        }
        return this.rawDistros;
      }
      this.results = [];
      this.deniedWhy = {};
      var pointSum = 0;
       for (var tag in this.currentTags) {
          var weight = this.currentTags[tag];
          var isNoTag = tag.indexOf("!") !== -1;
          if (!isNoTag){
            pointSum += weight; //Do not count no-tags
          }
        }
      for (var i = 0; i < this.rawDistros.length;i++){
        var distro = this.rawDistros[i];
        var points = 0;
        var hittedTags = 0;
        this.rawDistros[i].Excluded = false; //reset flag
        for (var tag in this.currentTags) {
          var weight = this.currentTags[tag];
          var isNoTag = tag.indexOf("!") !== -1;
          var needle = tag.replace("!","");

          //get percentage
          if (distro.Tags.indexOf(needle) !== -1){
            if (isNoTag){
              this.rawDistros[i].Excluded = true;
              if (Object.keys(this.deniedWhy).indexOf(needle) === -1){
                this.deniedWhy[needle] = 1;
              }else{
                this.deniedWhy[needle]++;
              }
              points = 0;
              //break;
            }
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
      this.commentSent = false;
      this.results.sort( function compare(a,b) {
        if (a.Percentage > b.Percentage)
          return -1;
        if (a.Percentage < b.Percentage)
          return 1;
        return 0;
      });
      return this.results;
    }
  },
  methods: {
    showTooltip:function(tooltip){
      alert(tooltip);
    },
    translateExcludedTags:function(answer){
      var result = this.text('excludes') +": \n";
      var _t = this;
      answer.NoTags.forEach(function(t){
        result += _t.text(t) + "\n";
      });
      return result.trim();
    },
    text:function(value){
      return this.i18n !== null &&typeof this.i18n[value] !== 'undefined'? this.i18n[value].Text:'';
    },
    isTagChoosed:function(tag){
       for (var key in this.currentTags) {
         if (key === tag){
           return true;
         }
      }
      return false;
    },
    getExcludingAnswer: function(tag){
      if (this.givenAnswers.length === 0){
        return "";
      }
      var tag = tag.replace("!","");
      var text = "";
      var question ="";
      for(var a in this.givenAnswers){
        var answer = this.givenAnswers[a];
       /* answer.Tags.forEach(function(t){
          if (t === tag){
            text = answer.Text;
          }
        });*/
        answer.NoTags.forEach(function(t){
          if (t === tag && text === ""){
            text = answer.Text;
          }
        });
        if (text !== ""){
            question = this.getQuestionByAnswer(answer.Id);
            break;
        }
      }
      return question.Number+ ". " + question.Text + ": " + text;
    },
    updateCurrentTags: function(){
      //get the currently answered tags
      this.currentTags = {};
      for (var i = 0; i < this.givenAnswers.length;i++){
         var answer = this.givenAnswers[i];
         for(var y = 0 ; y < answer.Tags.length; y++){
            var tag = answer.Tags[y];
            if (Object.keys(this.currentTags).indexOf(tag) === -1){
              this.currentTags[tag] = 1;
            }else{
              this.currentTags[tag]++;
            }
            if (answer.Important){
              this.currentTags[tag] *=2;
            }
          }
          for(var y = 0 ; y < answer.NoTags.length; y++){
            var tag = "!"+answer.NoTags[y];
            if (Object.keys(this.currentTags).indexOf(tag) === -1){
              this.currentTags[tag] = 1;
            }else{
              this.currentTags[tag]++;
            }
            if (answer.Important){
              this.currentTags[tag] *=2;
            }
          }
      }
      return this.currentTags;
    },
    init : function(){
        this.getLanguage();
        this.loaded = false;
        var _t = this;
        this.$http.post(this.backend,{method:'get',args: "[]", lang:  this.langCode}).then(function(data){
          var result = data.json();
          console.log("Hello #"+result.visitor);
          _t.rawDistros = result.distributions;
          _t.results = result.distributions;
          _t.i18n = result.systemVars;
          _t.questions = _t.questions.concat(result.questions);
          _t.questions[0].Text = _t.text("welcomeTextHeader");
          _t.questions[0].HelpText = _t.text("welcomeText");
          _t.loaded = true;      
          _t.lastQuestionNumber = result.questions.length;
          _t.displayRatings(result.lastRatings);
          console.log("Finished: " + new Date());
          _t.getOldTest();
        });
    },
    getStatistics: function(){
    	this.$http.post(this.backend,{method:'GetMonthStats',args: "", lang:  this.langCode}).then(function(data){
          this.testCount = JSON.parse(data.body);
        });
    },
    getRatings: function(){
      var _t = this;
      this.$http.post(this.backend,{method:'GetLastRatings',args: "", lang:  this.langCode}).then(function(data){
          this.otherUserResults = [];
          var got =  JSON.parse(data.body).reverse();
          _t.displayRatings(got);
        });
    },
    displayRatings(ratings){
      for(var rating in ratings){
            var tuple = {};
            tuple.comment = ratings[rating].Comment;
            tuple.stars = Math.ceil(ratings[rating].Rating);
            tuple.os = "Windows";
            if (ratings[rating].UserAgent.indexOf("Linux") !== -1){
              tuple.os = "Linux";
            }else if (ratings[rating].UserAgent.indexOf("ac") !== -1){
              tuple.os = "macOS";
            }else if (ratings[rating].UserAgent.indexOf("unix") !== -1){
              tuple.os = "Unix";
            }else if (ratings[rating].UserAgent.indexOf("Android") !== -1){
              tuple.os = "Android";
            }else if (ratings[rating].UserAgent.indexOf("iPhone") !== -1){
              tuple.os = "iPhone";
            }
            this.otherUserResults.unshift(tuple);
      }
    },
    getOldTest: function(){
        var parts = this.getUrlParts();
        if (typeof parts["answers"] !== 'undefined'){
          this.isOldTest = true;
        }else{
          if (typeof parts["test"] !== 'undefined'){
            var test = parseInt(parts["test"]);
            //Load old test results
            var _t = this;
            this.$http.post(this.backend,{method:'GetTest',args: test, lang:  this.langCode}).then(function(data){
                  var obj = JSON.parse(data.body);
                  var answers = JSON.parse(obj.Answers);
                  var important = JSON.parse(obj.Important);
                  for(var a =0; a < answers.length;a++){
                    this.selectAnswer(answers[a]);
                  }
                  for (var i = 0; i < _t.questions.length;i++){
                    var count = important.filter(function(q){
                      return q === _t.questions[i].Id;
                    });
                    _t.questions[i].Important = count.length !== 0;
                  }
            });
          }
        }
    },
    answeredQuestions: function(){
      var answered = [];
      for (var i = 0; i < this.questions.length;i++){
        for(var x = 0;  x < this.questions[i].Answers.length;x++){
          if (this.questions[i].Answers[x].Selected){
            answered.push(this.questions[i]);
            break;
          }
        }
      }
      return answered;
    },
  	getAnswer : function(id){
  		for (var i = 0; i < this.questions.length;i++){
  			for(var x = 0;  x < this.questions[i].Answers.length;x++){
  				if (this.questions[i].Answers[x].Id === id){
  					return this.questions[i].Answers[x];
  				}
  			}
  		}
  		return null;
  	},
    getQuestionByAnswer : function(id){
      for (var i = 0; i < this.questions.length;i++){
        for(var x = 0;  x < this.questions[i].Answers.length;x++){
          if (this.questions[i].Answers[x].Id === id){
            return this.questions[i];
          }
        }
      }
      return null;
    },
    getQuestion : function(id){
      for (var i = 0; i < this.questions.length;i++){
        if (this.questions[i].Id === id){
            return this.questions[i]
        }
      }
      return null;
    },
  	selectAnswer : function (id){
  		var answer = this.getAnswer(id);
      var question = this.getQuestionByAnswer(id);
      this.addAnswerToList(answer);
  		if (answer !== null && !answer.Selected){
  			answer.Selected = true;
        question.Answered = true;
  			return answer.Selected;
  		}
  		else if (answer.Selected){
        answer.Selected = false;
        question.Answered = false;
        for (var i=0;i<question.Answers.length;i++){
          if (question.Answers[i].Selected === true){
            question.Answered = true;
            break;
          }
        }
  			return answer.Selected;
  		}
      else{
        return false;
      }
  	},
    makeImportant : function (question){
      if (question !== null){
        if (question.Important){
          question.Important = false;
        }else{
          question.Important = true;
        }
        this.setGivenAnswerImportantFlag(question,question.Important);
        return question.Important;
      }else{
        return false;
      }
    },
    removeAnswers: function(question){
      for(var i=0;i<question.Answers.length;i++){
        question.Answers[i].Selected = false;
        this.removeAnswerFromList(question.Answers[i]);
      }
      question.Answered = false;
    },
    getGivenAnswerIndex: function(answer){
      var index = -1;
      this.givenAnswers.forEach(function(a,i,array){
        if (a.Id === answer.Id){
          index = i;
        }
      });
      return index;
    },
    removeAnswerFromList: function(answer){
      var index = this.getGivenAnswerIndex(answer);
      if (index !== -1){
        this.givenAnswers.splice(index,1);
      }
    },
    addAnswerToList: function(answer,important){
      var index = this.getGivenAnswerIndex(answer);
      if (index === -1) {
        //no duplicates
        answer.Important = important;
        this.givenAnswers.push(answer);
      }
    },
    setGivenAnswerImportantFlag: function(question,state){
      for (var i = 0; i < question.Answers.length;i++){
        var index = this.getGivenAnswerIndex(question.Answers[i]);
        if (index !== -1){
          this.givenAnswers[index].Important = state;
        }
      }
    },
  	updateAnsweredFlag : function(args,answer,question){
      var _t = this;
      if (question.SingleAnswer){
        question.Answers.forEach(function(a){
          if (answer.Id !== a.Id){
             a.Selected = false;
          }
          if (!a.Selected){
            _t.removeAnswerFromList(a);
          }
        });
        answer.Selected = true;
        question.Answered = true;
        this.addAnswerToList(answer,question.Important);
      }else{
        var answered = 0;
        question.Answers.forEach(function(a){
          if (a.Selected){
             answered++;
            _t.addAnswerToList(a,question.Important);
          }else{
            _t.removeAnswerFromList(a);
          }
        });
        question.Answered =  answered >0;
      }
  	},
    publishRating : function(args){
      var rating = $("#rating-stars").rateYo().rateYo("rating");
      var _this = this;
      var c = this.comment;
      this.$http.post(this.backend,{method:'NewRatingWithComment',args: "["+rating+",\""+c+"\","+(this.currentTest != -1 ? this.currentTest : "")+"]", lang:  this.langCode}).then(function(data){
          this.commentSent = true;
          this.getRatings();
      });
    },
    displayResults: function(){
      if ($("#Result").attr("aria-expanded") !== "true"){ //no recalculation if already open
        $("#Result").trigger("click");
        this.addResult();
      }
      window.scroll(0, $("#Result").offset().top - 50);
    },
    addResult: function (){
      var answers  = [];
      var important = [];
      this.updateCurrentTags()
      for(var i = 0; i < this.answered.length;i++){
          var question = this.answered[i];
          for(var x = 0; x < question.Answers.length;x++){
              if (question.Answers[x].Selected){
                answers.push(question.Answers[x].Id);
              }
          }
          if (question.Important){
            important.push(question.Id)
          }
      }
      $("#rating-stars").rateYo();
      this.currentTestLoading = false;
      this.$http.post(this.backend,{method:'AddResultWithTags',args: "["+JSON.stringify(this.rawDistros)+","+JSON.stringify(this.currentTags)+","+JSON.stringify(answers)+","+JSON.stringify(important) +"]", lang:  this.langCode}).then(function(data){
        this.currentTest = parseInt(data.body);
    	  this.getStatistics();
      });
    },
    getUrlParts: function(){
        var vars = {};
        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
        function(m,key,value) {
          vars[key] = value;
        });
        return vars;
    },
    getLanguage: function(){
      var langcode = this.getLanguageKey();
      var browserLang = navigator.language || navigator.userLanguage; 
      if (this.langs.indexOf(browserLang) !== -1 && langcode === null){
        this.lang = browserLang;
      }else{
        if (langcode === null){
          this.lang = "en"; //falback if the browser language is not currently configured and there is no language key given
        }else{
          this.lang = parseInt(langcode) === 1 ? 'de' : 'en';
        }
      }
    },
    getLanguageKey: function(){
      var parts = this.getUrlParts();
      var langcode = 1;
      if (typeof parts["l"] !== 'undefined'){
        return parts["l"];
      }
      return null;
    },
    nextTrigger: function(id){
      var needleIndex = -1;
      var needle = id;
      for(var i=0;i<this.questions.length;i++){
            if (i < this.questions.length && this.questions[i].Id === needle){
              needleIndex = i;
              break;
            }
      }
      if (needleIndex === this.questions.length -1){
        this.displayResults();
      }else{
        $("[ldc-header='"+this.questions[needleIndex+1].Id+"']").trigger("click",function(){
          window.scroll(0,$("[ldc-header='"+this.questions[needleIndex+1].Id+"']").top);
        });
      }
    },
    getTagTranslation : function(value){
      var anti = value.indexOf("!") !== -1;
      var text =  this.text(value.replace("!",""));
      return text !== "" ? (anti ? this.text("NotComplied") +": " : "") + text : value;
    }
  }
});
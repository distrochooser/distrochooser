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
    statistics: null,
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
    version: "3.0 (2017)",
    backend:"https://beta.distrochooser.de/distrochooser-backend-php",
    lang:"de",
    rawDistros: [],
    questions: [
      {
        "id":"welcome",
        "text":"",
        "help":"",
        "important":false,
        "single":false,
        "answers":[
        ],
        "number":-1
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
    this.getRatings();
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
        if (this.questions[i].answers.length !== 0){
          count++;
        }
      }
      return count;
    },
    excludedDistros : function(){
      var distros =  [];
      for(var i=0;i<this.rawDistros.length;i++){
        if (this.rawDistros[i].excluded){
          distros.push(this.rawDistros[i]);
        }
      }
      return distros;
    },
    distributions : function(){
      //Reset percentages if needed
      if (Object.keys(this.currentTags).length === 0){
        for (var i = 0; i < this.rawDistros.length;i++){
          this.rawDistros[i].percentage = 0;
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
        this.rawDistros[i].excluded = false; //reset flag
        for (var tag in this.currentTags) {
          var weight = this.currentTags[tag];
          var isNoTag = tag.indexOf("!") !== -1;
          var needle = tag.replace("!","");

          //get percentage
          if (distro.tags.indexOf(needle) !== -1){
            if (isNoTag){
              this.rawDistros[i].excluded = true;
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
          distro.percentage = Math.round(100 / (pointSum/points),2);
        }else{
          distro.percentage = 0;
        }

        if (distro.percentage > 0){
          this.results.push(distro);
        }
      }
      this.commentSent = false;
      this.results.sort( function compare(a,b) {
        if (a.percentage > b.percentage)
          return -1;
        if (a.percentage < b.percentage)
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
      answer.notags.forEach(function(t){
        result += _t.text(t) + "\n";
      });
      return result.trim();
    },
    text:function(value){
      return this.i18n !== null &&typeof this.i18n[value] !== 'undefined'? this.i18n[value].val:'';
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
        answer.notags.forEach(function(t){
          if (t === tag && text === ""){
            text = answer.text;
          }
        });
        if (text !== ""){
            question = this.getQuestionByAnswer(answer.id);
            break;
        }
      }
      return question.number+ ". " + question.text + ": " + text;
    },
    updateCurrentTags: function(){
      //get the currently answered tags
      this.currentTags = {};
      for (var i = 0; i < this.givenAnswers.length;i++){
         var answer = this.givenAnswers[i];
         for(var y = 0 ; y < answer.tags.length; y++){
            var tag = answer.tags[y];
            if (Object.keys(this.currentTags).indexOf(tag) === -1){
              this.currentTags[tag] = 1;
            }else{
              this.currentTags[tag]++;
            }
            if (answer.important){
              this.currentTags[tag] *=2;
            }
          }
          for(var y = 0 ; y < answer.notags.length; y++){
            var tag = "!"+answer.notags[y];
            if (Object.keys(this.currentTags).indexOf(tag) === -1){
              this.currentTags[tag] = 1;
            }else{
              this.currentTags[tag]++;
            }
            if (answer.important){
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
        this.$http.get(this.backend + "/get/"+this.lang+"/").then(function(data){
          var result = data.json();
          console.log("Hello #"+result.visitor);
          _t.rawDistros = result.distros;
          _t.results = result.distros;
          _t.i18n = result.i18n;
          _t.questions = _t.questions.concat(result.questions);
          _t.questions[0].text = _t.text("welcomeTextHeader");
          _t.questions[0].help = _t.text("welcomeText");
          _t.loaded = true;      
          _t.lastQuestionNumber = result.questions.length;
          _t.displayRatings(result.lastRatings);
          console.log("Finished: " + new Date());
          _t.getOldTest();
        });
    },
    getStatistics: function(){
    	this.$http.get(this.backend + "/getstats/").then(function(data){
          this.statistics = data.json();
        });
    },
    getRatings: function(){
      var _t = this;
      this.$http.get(this.backend + "/getratings/" + this.lang +"/").then(function(data){
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
            this.$http.get(this.backend +"/test/" + test +"/").then(function(data){
                  var obj = data.json();
                  var answers = JSON.parse(obj.answers);
                  var important = JSON.parse(obj.important);
                  for(var a =0; a < answers.length;a++){
                    this.selectAnswer(answers[a]);
                  }
                  for (var i = 0; i < _t.questions.length;i++){
                    var count = important.filter(function(q){
                      return q === _t.questions[i].id;
                    });
                    _t.questions[i].important = count.length !== 0;
                  }
            });
          }
        }
    },
    answeredQuestions: function(){
      var answered = [];
      for (var i = 0; i < this.questions.length;i++){
        for(var x = 0;  x < this.questions[i].answers.length;x++){
          if (this.questions[i].answers[x].selected){
            answered.push(this.questions[i]);
            break;
          }
        }
      }
      return answered;
    },
  	getAnswer : function(id){
  		for (var i = 0; i < this.questions.length;i++){
  			for(var x = 0;  x < this.questions[i].answers.length;x++){
  				if (this.questions[i].answers[x].id === id){
  					return this.questions[i].answers[x];
  				}
  			}
  		}
  		return null;
  	},
    getQuestionByAnswer : function(id){
      for (var i = 0; i < this.questions.length;i++){
        for(var x = 0;  x < this.questions[i].answers.length;x++){
          if (this.questions[i].answers[x].id === id){
            return this.questions[i];
          }
        }
      }
      return null;
    },
    getQuestion : function(id){
      for (var i = 0; i < this.questions.length;i++){
        if (this.questions[i].id === id){
            return this.questions[i]
        }
      }
      return null;
    },
  	selectAnswer : function (id){
  		var answer = this.getAnswer(id);
      var question = this.getQuestionByAnswer(id);
      this.addAnswerToList(answer);
  		if (answer !== null && !answer.selected){
  			answer.selected = true;
        question.answered = true;
  			return answer.selected;
  		}
  		else if (answer.selected){
        answer.selected = false;
        question.answered = false;
        for (var i=0;i<question.answers.length;i++){
          if (question.answers[i].selected === true){
            question.answered = true;
            break;
          }
        }
  			return answer.selected;
  		}
      else{
        return false;
      }
  	},
    makeImportant : function (question){
      if (question !== null){
        if (question.important){
          question.important = false;
        }else{
          question.important = true;
        }
        this.setGivenAnswerImportantFlag(question,question.important);
        return question.important;
      }else{
        return false;
      }
    },
    removeAnswers: function(question){
      for(var i=0;i<question.answers.length;i++){
        question.answers[i].selected = false;
        this.removeAnswerFromList(question.answers[i]);
      }
      question.answered = false;
    },
    getGivenAnswerIndex: function(answer){
      var index = -1;
      this.givenAnswers.forEach(function(a,i,array){
        if (a.id === answer.id){
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
        answer.important = important;
        this.givenAnswers.push(answer);
      }
    },
    setGivenAnswerImportantFlag: function(question,state){
      for (var i = 0; i < question.answers.length;i++){
        var index = this.getGivenAnswerIndex(question.answers[i]);
        if (index !== -1){
          this.givenAnswers[index].important = state;
        }
      }
    },
  	updateAnsweredFlag : function(args,answer,question){
      var _t = this;
      if (question.SingleAnswer){
        question.answers.forEach(function(a){
          if (answer.id !== a.id){
             a.selected = false;
          }
          if (!a.selected){
            _t.removeAnswerFromList(a);
          }
        });
        answer.selected = true;
        question.answered = true;
        this.addAnswerToList(answer,question.important);
      }else{
        var answered = 0;
        question.answers.forEach(function(a){
          if (a.selected){
             answered++;
            _t.addAnswerToList(a,question.important);
          }else{
            _t.removeAnswerFromList(a);
          }
        });
        question.answered =  answered >0;
      }
  	},
    publishRating : function(args){
      var rating = $("#rating-stars").rateYo().rateYo("rating");
      var _this = this;
      this.$http.post(this.backend + "/addrating/"+this.lang + "/",{
        test: _this.currentTest,
        rating: rating,
        comment: _this.comment
      }).then(function(data){
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
          for(var x = 0; x < question.answers.length;x++){
              if (question.answers[x].selected){
                answers.push(question.answers[x].id);
              }
          }
          if (question.important){
            important.push(question.id)
          }
      }
      $("#rating-stars").rateYo();
      this.currentTestLoading = false;
      this.$http.post(this.backend + "/addresult/",{
          distros: JSON.stringify(this.rawDistros),
          tags: JSON.stringify(this.currentTags),
          answers: JSON.stringify(answers),
          important: JSON.stringify(important) 
        }).then(function(data){
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
            if (i < this.questions.length && this.questions[i].id === needle){
              needleIndex = i;
              break;
            }
      }
      if (needleIndex === this.questions.length -1){
        this.displayResults();
      }else{
        $("[ldc-header='"+this.questions[needleIndex+1].id+"']").trigger("click",function(){
          window.scroll(0,$("[ldc-header='"+this.questions[needleIndex+1].id+"']").top);
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
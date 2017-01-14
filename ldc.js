loadingText();
function loadingText(preset){
    if (typeof preset !== 'undefined'){
      $(".text").text(preset);
    }else{
      var texts = ["Feeding penguins","Did I left the oven on?","Loading distributions","Blaming Windows","Installing Xorg","Running apt-get","Cloning sourcecode","Eating cookies","Disabling UEFI","Loading translation"];
      var index = Math.floor((Math.random() * texts.length) );
      $(".text").text(texts[index]);
    }
}
var ldc = function(){
	this.backend = "https://distrochooser.de/rest.php?json&ldc3";
  this.Title = "Linux Auswahlhilfe",
  this.version = "3.0 (2016)";
  this.lang = "de";
	this.distributions = [];
  this.systemVars = null;
	this.questions = [
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
	];
};
//Do some init stuff
ldc = new ldc();
Vue.http.options.emulateJSON = true;
vm = new Vue({
  el: '#app',
  data: {
    ldc: ldc, //ldc data instance
    debug: true, //debug mode?
    answered: 0, //the count of answered questions
    currentTags: {}, //the answered tags
    results: ldc.distributions, //the resulting distros
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
    otherUserResults:[],
    givenAnswers:[] //stores the currently given answers to avoid double iteration at getCurrentTags()
  },
  created: function(){
    console.log("  _     ___     ___   ____");
    console.log(" | |   |   \\   / __| |__ /");
    console.log(" | |__ | |) | |(__    |_ \\ ");
    console.log(" |____ |___/   \\___| |___/ ");
    console.log("Nice to see you! You are a developer? Contribute to https://github.com/cmllr/ldc.js and start improving the project.")
    console.log("Starting Linux Distribution Chooser "+ldc.version);
    console.log("Started: " + new Date());
    this.StartInit();
    this.NewVisitor();
    this.GetStatistics();
    this.GetRatings();
    setTimeout(this.GetRatings, 5000);
  },
  ready:function(){
    window.title = this.text("Title");
  },
  computed: {
    langCode: function(){
      return ldc.lang === "de" ? 1 : 2;
    },
    shareLink : function(){
      var baseUrl = "https://beta.distrochooser.de/?l="+this.langCode;

      if (this.currentTest === -1){
        return baseUrl;
      }
      return baseUrl+ "&test="+this.currentTest;
    },
    noResultText : function(){
      var text =  this.text("NoResults");
      return text;
    },
    startTestButtonText: function(){
      var text =  this.text("StartTest");
      return text;
    },
    nextButtonText: function(){
      var text =  this.text("nextQuestion");
      return text;
    },
    getResultButtonText : function(){
      var text =  this.text("getresult");
      return text;
    },
    ratingSent : function (){
        return false;
    },
    resultText : function(){
        return this.text("Result");
    },
    answeredQuestionsCount: function(){
      this.answered =  this.answeredQuestions();
      return this.answered.length;
    },
    questionsCount: function(){
      var count = 0;
      for(var i = 0; i < ldc.questions.length;i++){
        if (ldc.questions[i].Answers.length !== 0){
          count++;
        }
      }
      return count;
    },
    excludedDistros : function(){
      var distros =  [];
      for(var i=0;i<ldc.distributions.length;i++){
        if (ldc.distributions[i].Excluded){
          distros.push(ldc.distributions[i]);
        }
      }
      return distros;
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
      this.deniedWhy = {};
      var pointSum = 0;
       for (var tag in this.currentTags) {
          var weight = this.currentTags[tag];
          var isNoTag = tag.indexOf("!") !== -1;
          if (!isNoTag){
            pointSum += weight; //Do not count no-tags
          }
        }
      for (var i = 0; i < ldc.distributions.length;i++){
        var distro = ldc.distributions[i];
        var points = 0;
        var hittedTags = 0;
        ldc.distributions[i].Excluded = false; //reset flag
        for (var tag in this.currentTags) {
          var weight = this.currentTags[tag];
          var isNoTag = tag.indexOf("!") !== -1;
          var needle = tag.replace("!","");

          //get percentage
          if (distro.Tags.indexOf(needle) !== -1){
            if (isNoTag){
              ldc.distributions[i].Excluded = true;
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

      return this.results;
    }
  },
  methods: {
    preventDefault:function($event){
      $event.preventDefault();
    },
    text:function(value){
      if (ldc.systemVars === null){
        return "";
      }
      for (var i = 0; i < ldc.systemVars.length; i++) {
          if (ldc.systemVars[i].Val === value){
              return ldc.systemVars[i].Text;
          }
      }
      return "";
    },
    isTagChoosed:function(tag){
       for (var key in this.currentTags) {
         if (key === tag){
           return true;
         }
      }
      return false;
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
    StartInit : function(){
        this.getLanguage();
        this.loaded = false;
        loadingText();
        this.$http.post(ldc.backend,{method:'GetDistributions',args: "[]", lang:  this.langCode}).then(function(data){
        loadingText();
        var result = JSON.parse(data.body);
          ldc.distributions = [];
          for(var i = 0; i < result.length;i++){
            loadingText(result[i].Name);
            //translate the 2.x API for 3.x
            var distro = {};
            distro.Id = result[i].Id;
            distro.Name = result[i].Name;
            distro.Image = result[i].Image;
            distro.Color = result[i].Color;
            distro.Description = result[i].Description;
            distro.Website = result[i].Homepage;
            distro.Percentage = 0;
            distro.TextSource = result[i].TextSource;
            distro.ImageSource = result[i].ImageSource;
            distro.Tags = [];
            distro.Excluded = result[i].Excluded;
            try {
              distro.Tags = JSON.parse(result[i].Tags);
            } catch (error) {
              console.log(result[i].Tags);
              console.log(error);
              console.log(distro);
            }
            ldc.distributions.push(distro);
          }
          this.GetSystemVars();
      });
    },
    GetSystemVars : function(){
        loadingText();
        this.$http.post(ldc.backend,{method:'GetSystemVars',args: "[]", lang:  this.langCode}).then(function(data){
              loadingText();
              ldc.systemVars = JSON.parse(data.body);
              document.title = this.text("Title");
              this.i18n = ldc.systemVars;
              this.GetQuestionsFromAPI();
        });
    },
    GetStatistics: function(){
      loadingText();
    	this.$http.post(ldc.backend,{method:'AllMonthStats',args: "", lang:  this.langCode}).then(function(data){
          this.testCount = JSON.parse(data.body);
          loadingText();
        });
    },
    GetRatings: function(){
      this.$http.post(ldc.backend,{method:'GetLastRatings',args: "", lang:  this.langCode}).then(function(data){
          this.otherUserResults = [];
          var got =  JSON.parse(data.body).reverse();
          for(var rating in got){
            loadingText();
            var tuple = {};
            tuple.comment = got[rating].Comment;
            tuple.stars = Math.ceil(got[rating].Rating);
            tuple.os = "Windows";
            if (got[rating].UserAgent.indexOf("Linux") !== -1){
              tuple.os = "Linux";
            }else if (got[rating].UserAgent.indexOf("ac") !== -1){
              tuple.os = "macOS";
            }else if (got[rating].UserAgent.indexOf("unix") !== -1){
              tuple.os = "Unix";
            }else if (got[rating].UserAgent.indexOf("Android") !== -1){
              tuple.os = "Android";
            }else if (got[rating].UserAgent.indexOf("iPhone") !== -1){
              tuple.os = "iPhone";
            }
            this.otherUserResults.unshift(tuple);
          }
        });
    },
    GetQuestionsFromAPI : function(){
       this.$http.post(ldc.backend,{method:'GetQuestions',args: "[]", lang:  this.langCode}).then(function(data){
            loadingText();
            ldc.questions[0].ButtonText = this.startTestButtonText;
            ldc.questions[0].Text = this.text("welcomeTextHeader");
            ldc.questions[0].HelpText = this.text("welcomeText");
            var result = JSON.parse(data.body);
            this.lastQuestionNumber = result.length;
            for(var i = 0; i < result.length;i++){
                loadingText();
                //translate the 2.x API for 3.x
                var question = {};
                question.Id = "q"+result[i].Id;
                question.Number = i+1;
                question.Text = result[i].Text;
                question.HelpText = result[i].Help;
                question.Important = false;
                question.Answered = false;
                question.SingleAnswer = result[i].IsSingle;
                question.Answers = [];
                question.IsText = result[i].IsText;
                for(var x=0;x < result[i].Answers.length;x++){
                  var answer = {};
                  var current = result[i].Answers[x];
                  answer.Id = "a"+result[i].Answers[x].Id;
                  answer.Text = result[i].Answers[x].Text;
                  try {
                    var tags = result[i].Answers[x].Tags;
                    var noTags = result[i].Answers[x].NoTags;
                    answer.Tags = JSON.parse(tags);
                    if (noTags === ""){
                        answer.NoTags = [];
                    }
                    else{
                        answer.NoTags = JSON.parse(noTags); //tags which deny inpossible results, e.g hddinstall and live cd
                    }
                  } catch (error) {
                      console.log(error);
                  }
                  answer.Selected = false;
                  answer.IsText = result[i].Answers[x].IsText === "1";
                  answer.Image =  answer.IsText ? '' : './assets/answers/'+answer.Id+'.png';
                  question.Answers.push(answer);
                }
                if (question.Number < this.lastQuestionNumber){
                  question.ButtonText = this.nextButtonText;
                }
                else{
                  question.ButtonText = this.getResultButtonText;
                }
                ldc.questions.push(question);
              }
              loadingText();
              this.loaded = true;
              console.log("Finished: " + new Date());
              this.GetOldTest();
          });
    },
    GetOldTest: function(){
        var parts = this.getUrlParts();
        loadingText();
        if (typeof parts["answers"] !== 'undefined'){
          this.isOldTest = true;
        }else{
          if (typeof parts["test"] !== 'undefined'){
            var test = parseInt(parts["test"]);
            //Load old test results
            this.$http.post(ldc.backend,{method:'GetTest',args: test, lang:  this.langCode}).then(function(data){
                  var obj = JSON.parse(data.body);
                  var answers = JSON.parse(obj.Answers);
                  var important = JSON.parse(obj.Important);
                  for(var a =0; a < answers.length;a++){
                    this.selectAnswer(answers[a]);
                  }
                  for (var i = 0; i < ldc.questions.length;i++){
                    var count = important.filter(function(q){
                      return q === ldc.questions[i].Id;
                    });
                    ldc.questions[i].Important = count.length !== 0;
                  }
                  loadingText();
            });
          }
        }
    },
    NewVisitor: function(){
      this.$http.post(ldc.backend,{method:'NewVisitor',args: "\""+document.referrer+"\"", lang:  this.langCode, dnt: navigator.doNotTrack !== null}).then(function(response){
          console.log("Hello #"+response.body);
          loadingText("Hello #"+response.body);
      });
    },
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
      var question = this.getQuestionByAnswer(id);

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
    makeImportant : function (args,question){
      args.preventDefault();
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
    removeAnswers: function(event,question){
      event.preventDefault();
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
      this.$http.post(ldc.backend,{method:'NewRatingWithComment',args: "["+rating+",\""+c+"\","+(this.currentTest != -1 ? this.currentTest : "")+"]", lang:  this.langCode}).then(function(data){
          this.commentSent = true;
          this.GetRatings();
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

      this.currentTestLoading = true;
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
      this.$http.post(ldc.backend,{method:'AddResultWithTags',args: "["+JSON.stringify(ldc.distributions)+","+JSON.stringify(this.currentTags)+","+JSON.stringify(answers)+","+JSON.stringify(important) +"]", lang:  this.langCode}).then(function(data){
        this.currentTest = parseInt(data.body);
    	  this.GetStatistics();
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
      var installed = ["de","en"];
      ldc.lang = parseInt(langcode) === 1 ? 'de' : 'en';
    },
    getLanguageKey: function(){
      var parts = this.getUrlParts();
      var langcode = 1;
      if (typeof parts["l"] !== 'undefined'){
        langcode = parts["l"];
      }
      return langcode;
    },
    nextTrigger: function(id){
      var needleIndex = -1;
      var needle = id;
      for(var i=0;i<ldc.questions.length;i++){
            if (i < ldc.questions.length && ldc.questions[i].Id === needle){
              needleIndex = i;
              break;
            }
      }
      if (needleIndex === ldc.questions.length -1){
        this.displayResults();
      }else{
        $("[ldc-header='"+ldc.questions[needleIndex+1].Id+"']").trigger("click",function(){
          window.scroll(0,$("[ldc-header='"+ldc.questions[needleIndex+1].Id+"']").top);
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

function TranslateLanguage(lang){
    if (lang === "de"){
      return 1;
    }
    return 2;
}
function TranslateLanguageCode(lang){
  if (lang === 1){
    return "de";
  }
  else{
    return "en";
  }
}
function GetSystemValue(ldc,needle){
        if (ldc.systemVars === null){
          return "";
        }
        for (var i = 0; i < ldc.systemVars.length; i++) {
                if (ldc.systemVars[i].Val == needle){
                        return ldc.systemVars[i].Text;
                }
       	}
        return "";
}
function UI(){
   $(".ldcui").each(function(index, value) {
          var id = $(this).attr('id');
          var value = GetSystemValue(ldc,id);
          if (id == undefined || value == "")
          {
              //for elements with duplicate context
              var classes = $(this).attr("class").split(' ');
              id = classes[classes.length -1];
              value = GetSystemValue(ldc,id);
          }
          if (value != "")
                      $(this).html(value);
      });
}
function loadingText(){
    var texts = ["Feeding penguins","Fixing Windows","loading","Rearanging molecules"];
    var index = Math.floor((Math.random() * texts.length) );
    $(".text").text(texts[index]+"...");
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
    tags: {}, //the answered tags
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
    otherUserResults:[]
  },
  created: function(){
    console.log("Starting Linux Distribution Chooser "+ldc.version);
    console.log("Started: " + new Date());
    this.StartInit();
    this.NewVisitor();
    this.GetStatistics();
    this.GetRatings();
    setTimeout(this.GetRatings, 5000);
    console.log("Finished: " + new Date());
  },
  ready:function(){
    window.title = GetSystemValue(this.ldc,"Title");
  },
  computed: {
    shareLink : function(){
      var baseUrl = "https://beta.distrochooser.de/?l="+TranslateLanguage(ldc.lang);

      if (this.currentTest === -1){
        return baseUrl;
      }
      return baseUrl+ "&test="+this.currentTest;
    },
    noResultText : function(){
      var text =  GetSystemValue(this.ldc,"NoResults");
      return text;
    },
    startTestButtonText: function(){
      var text =  GetSystemValue(this.ldc,"StartTest");
      return text;
    },
    nextButtonText: function(){
      var text =  GetSystemValue(this.ldc,"nextQuestion");
      return text;
    },
    getResultButtonText : function(){
      var text =  GetSystemValue(this.ldc,"getresult");
      return text;
    },
    ratingSent : function (){
        return false;
    },
    resultText : function(){
        return GetSystemValue(this.ldc,"Result");
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
    currentTags: function(){
      //get the currently answered tags
      this.tags = {};
      for (var i = 0; i < ldc.questions.length;i++){
        var q = ldc.questions[i];
        for(var x = 0;  x < q.Answers.length;x++){
          if (q.Answers[x].Selected === true){
            //save tags
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
            for(var y = 0 ; y < q.Answers[x].NoTags.length; y++){
              var weight = 1;
              var tag = "!"+q.Answers[x].NoTags[y];
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
      return ldc.distributions.length - this.excludedDistros.length
    },
    allDistributionsCount : function (){
      return ldc.distributions.length;
    },
    excludedDistros : function(){
      var distros =  [];
      for(var i=0;i<ldc.distributions.length;i++){
        console.log(ldc.distributions[i].Excluded)
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
              console.log(distro.Name + " denied because of tag: "+needle+ " (at least)");
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
      return GetSystemValue(this.ldc,value);
    },
    isTagChoosed:function(tag){
       for (var key in this.currentTags) {
         if (key === tag){
           return true;
         }
      }
      return false;
    },
    StartInit : function(){
        this.getLanguage();
        this.loaded = false;
        this.$http.post(ldc.backend,{method:'GetDistributions',args: "[]", lang:  TranslateLanguage(ldc.lang)}).then(function(data){
        loadingText();
        var result = JSON.parse(data.body);
          ldc.distributions = [];
          for(var i = 0; i < result.length;i++){
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
        this.$http.post(ldc.backend,{method:'GetSystemVars',args: "[]", lang:  TranslateLanguage(ldc.lang)}).then(function(data){
              loadingText();
              ldc.systemVars = JSON.parse(data.body);
              document.title = GetSystemValue(this.ldc,"Title");
              this.i18n = ldc.systemVars;
              UI();
              this.GetQuestionsFromAPI();

        });
    },
    GetStatistics: function(){
    	this.$http.post(ldc.backend,{method:'AllMonthStats',args: "", lang:  TranslateLanguage(ldc.lang)}).then(function(data){
    		  console.log("Grabbing statistics...");
          this.testCount = JSON.parse(data.body);
          console.log("Statistics grabbed.");
        });
    },
    GetRatings: function(){
      this.$http.post(ldc.backend,{method:'GetLastRatings',args: "", lang:  TranslateLanguage(ldc.lang)}).then(function(data){
          this.otherUserResults = [];
          var got =  JSON.parse(data.body).reverse();
          for(var rating in got){
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
       this.$http.post(ldc.backend,{method:'GetQuestions',args: "[]", lang:  TranslateLanguage(ldc.lang)}).then(function(data){
            loadingText();
            ldc.questions[0].ButtonText = this.startTestButtonText;
            ldc.questions[0].Text = GetSystemValue(ldc,"welcomeTextHeader");
            ldc.questions[0].HelpText = GetSystemValue(ldc,"welcomeText");
            var result = JSON.parse(data.body);
            this.lastQuestionNumber = result.length;
            for(var i = 0; i < result.length;i++){
                //translate the 2.x API for 3.x
                var question = {};
                question.Id = "q"+result[i].Id;
                question.Number = i+1;
                question.Text = result[i].Text;
                question.HelpText = result[i].Help;
                question.Important = false; //TODO: Insert into DB
                question.Answered = false;
                question.SingleAnswer = true; //TODO: Insert into DB
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
              this.GetOldTest();


            this.loaded = true;
          });
    },
    GetOldTest: function(){
       //if test is present
        var parts = this.getUrlParts();
        if (typeof parts["answers"] !== 'undefined'){
          this.isOldTest = true;

        }else{
          if (typeof parts["test"] !== 'undefined'){
            var test = parseInt(parts["test"]);
            //Load old test results
              this.$http.post(ldc.backend,{method:'GetTest',args: test, lang:  TranslateLanguage(ldc.lang)}).then(function(data){
                    var obj = JSON.parse(data.body);
                    var answers = JSON.parse(obj.Answers);
                    for(var a =0; a < answers.length;a++){
                      this.selectAnswer(answers[a]);
                    }
              });
          }
        }
    },
    NewVisitor: function(){
      this.$http.post(ldc.backend,{method:'NewVisitor',args: "\""+document.referrer+"\"", lang:  TranslateLanguage(ldc.lang)}).then(function(response){
          console.log("Hello #"+response.body);
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
    makeImportant : function (args){
      args.preventDefault();
      var question = this.getQuestion(this.getTarget(args));
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
      args.preventDefault();
      var id = this.getTarget(args);
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
  		var answer = this.selectAnswer(id);
  		return answer;
  	},
    nomultipleAnswersAllowed : function(){
      var text = GetSystemValue(ldc,"NotAllowed");
      alert(text);
    },
    publishRating : function(args){
      var rating = $("#rating-stars").rateYo().rateYo("rating");
      var _this = this;
      var c = this.comment;
      this.$http.post(ldc.backend,{method:'NewRatingWithComment',args: "["+rating+",\""+c+"\"]", lang:  TranslateLanguage(ldc.lang)}).then(function(data){
          this.commentSent = true;
          this.GetRatings();
      });
    },
    addResult: function (args){
      var answers  = [];
      for(var i = 0; i < this.answered.length;i++){
          var question = this.answered[i];
          for(var x = 0; x < question.Answers.length;x++){
              if (question.Answers[x].Selected){
                answers.push(question.Answers[x].Id);
              }
          }
      }
      this.currentTestLoading = true;
      this.$http.post(ldc.backend,{method:'AddResultWithTags',args: "["+JSON.stringify(ldc.distributions)+","+JSON.stringify(this.currentTags)+","+JSON.stringify(answers)+"]", lang:  TranslateLanguage(ldc.lang)}).then(function(data){
        this.currentTest = parseInt(data.body);
        this.currentTestLoading = false;
    	  this.GetStatistics();
        $("#rating-stars").rateYo();
      });
       //Jump to the result collapse
       window.scroll(0, $("#Result").offset().top);
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
      ldc.lang = TranslateLanguageCode(parseInt(langcode));
    },
    getLanguageKey: function(){
      var parts = this.getUrlParts();
      var langcode = 1;
      if (typeof parts["l"] !== 'undefined'){
        langcode = parts["l"];
      }
      return langcode;
    },
    nextTrigger: function(args){
      var id = this.getClickId(args);
      var needleIndex = -1;
      var needle = id.replace("-next","");
      for(var i=0;i<ldc.questions.length;i++){
            if (i < ldc.questions.length && ldc.questions[i].Id === needle){
              needleIndex = i;
              break;
            }
      }
      if (needleIndex === ldc.questions.length -1){
          $("#getresult").trigger("click");
      }else{
          $("[ldc-header='"+ldc.questions[i+1].Id+"']").trigger("click");
      }
    },
    getClickId : function (args){
      if (args.srcElement){
        //Chrome
        return args.srcElement.attributes[2].value;
      }
      else{
        //Firefox
        return args.target.attributes[1].value;
      }
    },
    getTarget : function(args){
      var target = null;
       if (args.srcElement){
        //Chrome
        target = args.srcElement;
      }
      else{
        //Firefox
        target = args.target;
      }
      return target.attributes[2].value;
    },
    getTagTranslation : function(value){
      var text =  GetSystemValue(this.ldc,value);
      return text !== "" ? text : value;
    }
  }
});

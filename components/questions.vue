<template>
  <div>
    <div class="col-lg-6">
      <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="false">
        <div v-for="(q,qindex) in this.globals.distrochooser.questions" v-bind:key="q.id" class="panel panel-default">
          <div class="panel-heading" role="tab" :id="'header' + q.id">
            <h4 class="panel-title">
              <a class="question-header" :ldc-header="q.id" role="button" data-toggle="collapse" data-parent="#accordion" :href="'#collapse' + q.id" aria-expanded="true" :aria-controls="'collapse' +q.id" v-bind:class="{'answered':q.answered}">
                <span v-if="q.number !== -1"> {{ qindex }}. </span>{{ q.text }}
              </a>
            </h4>
            <a href="#" class="fa fa-exclamation-circle mark-important" v-bind:class="{'important':q.important,'hidden':q.answers.length=== 0}" :data-id="q.id"  :title="text('important-button')"></a>
          </div>
          <div :id="'collapse' + q.id" class="panel-collapse question collapse" role="tabpanel" :aria-labelledby="'header' +q.id">
            <div class="panel-body">
              <p v-html="q.number === -1 ? '' : q.help"></p>
              <img class="largelogo" v-if="q.id === 'welcome'">
              <div id="StartText" v-if="q.id === 'welcome'">
                <span v-html="text('introText')"></span>
                <ul class="list">
                  <li>{{ text('can-skip-questions') }} </li>
                  <li>{{ text('can-get-result-anytime') }} </li>
                  <li>{{ text('can-get-result-anyorder') }}</li>
                  <li v-html="text('can-delete')"></li>
                  <li v-html="text('can-mark-important')"></li>
                  <li v-html="text('get-exclusion')"></li>
                </ul>
              </div>
              <div v-if="q.answers.length !== 0" class="answer-parent">
                <div :class="q.single ? 'radio' : 'checkbox'" v-for="(a,aindex) in q.answers" v-bind:key="a.id">
                  <p v-if="q.single">
                    <input :id="a.id" :checked='a.selected ' :name="q.id + '_a'" :data-id="a.id" type="radio" v-on:click="answer(q, a)">
                    <label class="answer-text" :for="a.id" v-bind:class="{ 'selected': a.selected }">
                      {{ a.text }}
                    </label>
                    <i v-on:click.prevent="showTooltip(translateExcludedTags(a),$event)" v-if="a.notags.length > 0" class="fa fa-question-circle fa-question-exclude" data-placement='left' data-html="true" :data-title="translateExcludedTags(a)"></i>
                  </p>
                  <p v-if="!q.single">
                    <input :id="a.id" v-model="a.selected" :data-id="a.id" :name="q.id + '_a'" type="checkbox" v-on:click="answer(q, a)">
                    <label class="answer-text" :for="a.id" v-bind:class="{ 'selected': a.selected }">
                      {{ a.text }}
                    </label>
                    <i v-on:click.prevent="showTooltip(translateExcludedTags(a),$event)" v-if="a.notags.length > 0" class="fa fa-question-circle" data-placement='left' data-html="true" :data-title="translateExcludedTags(a)"></i>
                  </p>
                </div>
              </div>
              <a href="#" :class="'btn btn-primary ' +q.id + '-next'" :data-id="q.id + '-next'" v-on:click.prevent="nextTrigger(q)">
                {{ lastQuestionNumber=== q.number ? text("getresult") : (q.number === -1 ? text("StartTest") :text("nextQuestion"))}}
              </a>
              <a v-if="lastQuestionNumber !== q.number && q.number !== -1" href="#" class="skip-question hidden-xs" v-on:click.prevent="nextTrigger(q)">
                <i class="fa fa-mail-forward"></i> {{ text("skip-question") }}</a>
              <a href="#" class="clear-answer" v-if="q.answered" v-on:click.prevent="removeAnswers(q)">
                <i class="fa fa-trash remove-answer"></i> {{ text("clear") }}</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-3">
        <ul class="list-group">
					<li class="list-group-item"><a class="hidden-xs" id="homelink" href="index.php">
            <img alt="Linux Distribution Chooser"></a></li>
						<li class="list-group-item">
							<span class="badge"><span id="answeredCount">{{ answered.length }} </span>/ <span id="answerCount">{{ this.globals.questions.length - 1 }}</span></span>
							<span id="answered">{{ text('answered') }}</span>
						</li>
						<li class="list-group-item">
							<div class="checkbox">
								<label>
									<input type="checkbox" v-model="this.globals.distrochooser.options.displayExcluded">  {{ text('displayExcluded') }}
								</label>
							</div>
							<div class="checkbox">
								<label>
									<input type="checkbox" v-model="this.globals.distrochooser.options.displayFilters">  {{ text('displayFilters') }}
								</label>
							</div>
						</li>
						<li class="list-group-item">
							<a class="btn btn-primary" id="getresult" >{{ text('getresult') }}</a>
						</li>
						<li class="list-group-item">
							<i class="fa fa-cog fa-spin fa-fw"></i>  
						</li>
					</ul>
    </div>
  </div>
</template>
 
<script>
import Vue from 'vue' // eslint-disable-line no-unused-vars
import i18n from '../mixins/i18n'
import nuxt from '../mixins/nuxt-wrapper'
export default {
  mixins: [
    i18n,
    nuxt
  ],
  computed: {
    backendUrl: function () {
      return this.$parent.backend + '/'
    },
    lastQuestionNumber: function () {
      return this.globals.questions.length - 1
    },
    answered: function () {
      return this.globals.questions.filter(function (q) {
        return q.answered
      })
    }
  },
  methods: {
    nextTrigger: function (q) {
      var index = this.globals.questions.indexOf(q)
      if (index === this.lastQuestionNumber) { // eslint-disable-line space-infix-ops
        return
      }
      jQuery('#collapse' + q.id).collapse('toggle') // eslint-disable-line no-undef
      var next = this.globals.questions[index + 1]
      jQuery('#collapse' + next.id).collapse('toggle') // eslint-disable-line no-undef
    },
    answer: function (q, a) {
      var answered = 0
      for (var i in q.answers) {
        // input[type='radio'] needs to be set per code that we can handle it the same way as input[type='checkbox']
        if (q.answers[i] === a) {
          q.answers[i].selected = true
        }
        if (q.answers[i].selected) {
          answered++
        }
      }
      q.answered = answered > 0
    },
    removeAnswers: function (q) {
      for (var i in q.answers) {
        q.answers[i].selected = false
      }
      q.answered = false
    }
  }
}
</script>
 
<style scoped>
  .answer-parent input[type='checkbox'],.answer-parent input[type='radio']{
    margin-left: 0.1em;
  }
  .answered{
    font-weight: bold;
  }
</style>

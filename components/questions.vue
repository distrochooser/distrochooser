<template>
  <div class="col-lg-6">
    <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="false">
      <div v-for="(q,qindex) in this.questions" v-bind:key="q.id" class="panel panel-default">
        <div class="panel-heading" role="tab" :id="'header' + q.id">
          <h4 class="panel-title">
            <a class="question-header" :ldc-header="q.id" role="button" data-toggle="collapse" data-parent="#accordion" :href="'#collapse' + q.id" aria-expanded="true" :aria-controls="'collapse' +q.id" v-bind:class="{'answered':q.answered}">
              <span v-if="q.number !== -1"> {{ qindex }}. </span>{{ q.text }}
            </a>
          </h4>
          <a href="#" class="fa fa-exclamation-circle mark-important" v-bind:class="{'important':q.important,'hidden':q.answers.length=== 0}" :data-id="q.id" v-on:click.prevent="makeImportant(question)" :title="text('important-button')"></a>
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
              <div :class="q.single ? 'radio' : 'checkbox'" v-for="(answer,aindex) in q.answers" v-bind:key="answer.id">
                <p v-if="q.single">
                  <input :id="answer.id" :checked='answer.selected ' :name="q.id + '_a'" :data-id="answer.id" type="radio" v-on:click="updateAnsweredFlag($event,answer,question)">
                  <label class="answer-text" :for="answer.id" v-bind:class="{ 'selected': answer.selected }">
                    {{ answer.text }}
                  </label>
                  <i v-on:click.prevent="showTooltip(translateExcludedTags(answer),$event)" v-if="answer.notags.length > 0" class="fa fa-question-circle fa-question-exclude" data-placement='left' data-html="true" :data-title="translateExcludedTags(answer)"></i>
                </p>
                <p v-if="!q.single">
                  <input :id="answer.id" v-model="answer.selected" :data-id="answer.id" :name="q.id + '_a'" type="checkbox" v-on:change="updateAnsweredFlag($event,answer,question)">
                  <label class="answer-text" :for="answer.id" v-bind:class="{ 'selected': answer.selected }">
                    {{ answer.text }}
                  </label>
                  <i v-on:click.prevent="showTooltip(translateExcludedTags(answer),$event)" v-if="answer.notags.length > 0" class="fa fa-question-circle" data-placement='left' data-html="true" :data-title="translateExcludedTags(answer)"></i>
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
</template>
 
<script>
import Vue from 'vue' // eslint-disable-line no-unused-vars
import i18n from '../mixins/i18n'
import api from '../mixins/api'

export default {
  data: function () {
    return {
      'backend': 'https://distrochooser.de/distrochooser-backend-php',
      'lang': 'de',
      'questions': []
    }
  },
  mixins: [
    i18n,
    api
  ],
  computed: {
    backendUrl: function () {
      return this.backend + '/'
    },
    lastQuestionNumber: function () {
      return this.questions.length
    }
  },
  created: function () {
    this.init()
  },
  methods: {
    nextTrigger: function (q) {
      var index = this.questions.indexOf(q)
      if (index === this.lastQuestionNumber-1) { // eslint-disable-line space-infix-ops
        return
      }
      jQuery('#collapse' + q.id).collapse('toggle') // eslint-disable-line no-undef
      var next = this.questions[index + 1]
      jQuery('#collapse' + next.id).collapse('toggle') // eslint-disable-line no-undef
    }
  }
}
</script>
 
<style scoped>
  input[type='checkbox'],input[type='radio']{
    margin-left: 0.1em;
  }
</style>

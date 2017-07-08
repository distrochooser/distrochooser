<template>
  <div class="column col-9">
    <div class="columns">
      <div class="column col-6" id="accordion">
        <div class="accordion">
          <div class="accordion-item" v-for="(q,qindex) in this.globals.distrochooser.questions" v-bind:key="q.id" >
            <input type="radio" :id="'header' + q.id" name="accordion-radio" hidden="">
            <label class="accordion-header hand" :class="{'answered':q.answered}" :for="'header' + q.id">
               <span v-if="q.number !== -1"> {{ qindex }}. </span>{{ q.text }}
            </label>
            <div class="accordion-body">
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
                      <label class="form-radio" :for="a.id" v-bind:class="{ 'selected': a.selected }">
                        <input :id="a.id" :checked='a.selected ' :name="q.id + '_a'" :data-id="a.id" type="radio" v-on:click="answer(q, a)">
                        <i class="form-icon"></i> {{ a.text }}
                      </label>
                      <i v-on:click.prevent="showTooltip(translateExcludedTags(a),$event)" v-if="a.notags.length > 0" class="fa fa-question-circle fa-question-exclude" data-placement='left' data-html="true" :data-title="translateExcludedTags(a)"></i>
                    </p>
                    <p v-if="!q.single">
                      <label class="form-checkbox" :for="a.id" v-bind:class="{ 'selected': a.selected }">
                        <input :id="a.id" :checked='a.selected ' :name="q.id + '_a'" :data-id="a.id" type="checkbox" v-on:click="answer(q, a)">
                        <i class="form-icon"></i> {{ a.text }}
                      </label>
                      <i v-on:click.prevent="showTooltip(translateExcludedTags(a),$event)" v-if="a.notags.length > 0" class="fa fa-question-circle" data-placement='left' data-html="true" :data-title="translateExcludedTags(a)"></i>
                    </p>
                  </div>
                </div>
                <div class="btn-group btn-group-block" v-if="q.number !== -1">
                  <a v-on:click.prevent="nextTrigger(q)" class="btn"> <i class="icon icon-check"></i> {{ lastQuestionNumber=== q.number ? text("getresult") :text("nextQuestion") }}</a>
                  <a v-if="!q.answered && lastQuestionNumber !== q.number && q.number !== -1" class="btn" v-on:click.prevent="nextTrigger(q)"> <i class="icon icon-cross"></i> {{ text("skip-question") }} </a>
                  <a v-if="q.answered" class="btn danger" v-on:click.prevent="removeAnswers(q)"> <i class="icon icon-delete"></i> {{ text("clear") }} </a>
                </div>
                <a class="btn btn-primary" href="#" v-if="q.number === -1" v-on:click.prevent="nextTrigger(q)">
                  {{ text("StartTest") }}
                </a>
              </div>  
            </div>
          </div>
        </div>

        <!-- result part -->
        <div>
          <div class="form-group">
            <div class="columns">
                <div class="column col-3">
                  descr. 
                  <span>unwichtig</span>
                </div>
                <div class="column col-9">
                  <input class="slider" type="range" min="0" max="5" value="1">
                </div>
            </div>
          </div>
        </div>
      </div>
      <div class="column col-2">
      </div>
      <div class="column col-3">
          <div class="panel">
            <div class="panel-header text-center">
              <figure class="avatar avatar-lg">
                <img src="https://distrochooser.de/assets/%5btondo%5d%5bf%5dLinux.png">
              </figure>
              <div class="panel-subtitle">{{ answered.length + "/" + (this.globals.questions.length - 1) + " " + text('answered') }}</div>
              <progress class="progress" :value="answered.length" :max="this.globals.questions.length - 1"></progress>
            </div>
            <div class="panel-body">
              <div class="form-group">
                <label class="form-switch">
                  <input type="checkbox" v-model="globals.distrochooser.options.displayExcluded">
                  <i class="form-icon"></i> {{ text('displayExcluded') }}
                </label>
              </div>
              <div class="form-group">
                <label class="form-switch">
                  <input type="checkbox" v-model="globals.distrochooser.options.displayFilters">
                  <i class="form-icon"></i> {{ text('displayFilters') }}
                </label>
              </div>
              <div class="panel-footer">
                <button class="btn btn-primary">{{ text('getresult') }}</button>
              </div>
            </div>
          </div>
      </div>
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
  mounted: function () {
    jQuery('#headerwelcome').trigger('click') // eslint-disable-line no-undef
  },
  computed: {
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
      jQuery('#header' + q.id).trigger('click') // eslint-disable-line no-undef
      var next = this.globals.questions[index + 1]
      jQuery('#header' + next.id).trigger('click') // eslint-disable-line no-undef
    },
    answer: function (q, a) {
      var answered = 0
      if (q.single) {
        this.removeAnswers(q)
      }
      for (var i in q.answers) {
        // input[type='radio'] needs to be set per code that we can handle it the same way as input[type='checkbox']
        if (q.answers[i] === a) {
          q.answers[i].selected = !q.answers[i].selected
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
  .selected{
    font-weight: bold;
  }
</style>

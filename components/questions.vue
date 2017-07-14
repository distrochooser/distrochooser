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
                  <a v-on:click.prevent="nextTrigger(q)" class="btn"> <i class="icon icon-check"></i> {{ lastQuestionNumber=== q.number ? text("toggleResult") :text("nextQuestion") }}</a>
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
        <div class="columns" v-if="!resultWayChoosed && this.answered.length > 0">
          <h3 id="weighting"> {{ text("choiceweightorresult") }} </h3>
          <div class="column col-5">
            <a class="btn" v-on:click.prevent="toggleResult" href="#">{{ text("choiceresult") }}</a>
          </div>    
          <div class="column col-2">
            {{ text("or") }}
          </div> 
          <div class="column col-5">
            <a class="btn" href="#" v-on:click.prevent="toggleWeighting">{{ text("choiceweight") }}</a>
          </div>
        </div>
        <div v-if="weigthActive">
          <div class="form-group">
            <div class="columns" v-for="(tag,key) in tags" v-bind:key="key">
                <div class="column col-5">
                  {{ text(key) }} is: <pre>{{ tag.negative }}</pre>
                </div>
                <i class="icon icon-minus col-1"></i> 
                <div class="column col-4"> {{ tag.weight }}
                  <input class="slider" type="range" min="-3" max="3" value="0" v-model="tag.weight">
                </div>
                <i class="icon icon-plus col-1"></i> 
            </div>
          </div>
          <div class="btn-group columns">
            <a class="btn" v-on:click.prevent="toggleWeighting" href="#"> {{ text("abort") }}</a>
            <a class="btn" v-on:click.prevent="toggleResult" href="#">{{ text("getresult") }}</a>
          </div>
        </div>
        <div class="results" v-if="resultWayChoosed">
          <div class="columns">
            <a class="btn back-button" v-on:click.prevent="toggleResult"> {{ text("back") }} </a>
          </div>
          <distrolist :distros="distros"></distrolist>
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
                <button class="btn btn-primary" :class="{'disabled':this.answered.length === 0}" v-on:click.prevent="jumpToWeighting">{{ text('getresult') }}</button>
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
import distrolist from './distrolist'
export default {
  data: function () {
    return {
      weigthActive: false,
      resultWayChoosed: false,
      tags: {}
    }
  },
  mixins: [
    i18n,
    nuxt
  ],
  components: {
    distrolist
  },
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
    },
    distros: function () {
      // var raw =  this.globals.distros
      var results = []
      var _t = this
      this.globals.distros.forEach(function (d) {
        var hits = []
        var antihits = []
        for (var k in _t.tags) {
          /**
           * Case I : tag 'foo' -> tag (distro) 'foo'
           * Case II : tag 'foo' -> tag (distro) '!foo'
           * Case III : tag 'foo', negative
           * */

          if (d.tags.indexOf(k) !== -1 && hits.indexOf(k) === -1) {
            if (_t.tags[k].negative) {
              antihits.push(k)
            } else {
              hits.push(k)
            }
          }
          if (d.tags.indexOf('!' + k) !== -1 && antihits.indexOf(k) === -1) {
            antihits.push(k)
          }
        }
        var distroPoints = 0
        // calculate sum with weight
        hits.forEach(function (t) {
          var weight = _t.tags[t].weight
          var amount = _t.tags[t].amount // a tag can be given more than one times, causes "heavier" weight
          var sum = amount * weight
          distroPoints += sum
        })
        // calculate sum with weight
        antihits.forEach(function (t) {
          var weight = _t.tags[t].weight
          var amount = _t.tags[t].amount // a tag can be given more than one times, causes "heavier" weight
          var sum = amount * weight
          distroPoints -= sum
        })
        // calculate percentage
        d.points = distroPoints
        results.push(d)
      })
      return results.sort(function (a, b) {
        return a.points < b.points ? 1 : -1
      })
    }
  },
  methods: {
    computeTags: function () {
      var result = {}
      for (var i = 0; i < this.answered.length; i++) {
        this.answered[i].answers.forEach(function (element) {
          if (element.selected) {
            var tag = element.tags
            tag.forEach(function (t) {
              if (typeof result[t] === 'undefined') {
                result[t] = {
                  amount: 1,
                  weight: 1,
                  negative: false
                }
              } else {
                result[t].amount++
              }
            })
            tag = element.notags
            tag.forEach(function (t) {
              var name = t.replace('!', '')
              if (typeof result[name] === 'undefined') {
                result[name] = {
                  amount: 1,
                  weight: 1,
                  negative: true
                }
              } else {
                result[name].amount++
              }
            })
          }
        }, this)
      }
      this.tags = result
    },
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
      this.resultWayChoosed = false
      this.weigthActive = false
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
      this.computeTags()
    },
    removeAnswers: function (q) {
      for (var i in q.answers) {
        q.answers[i].selected = false
      }
      q.answered = false
    },
    toggleWeighting: function () {
      this.weigthActive = !this.weigthActive
    },
    toggleResult: function () {
      if (this.weigthActive) {
        this.toggleWeighting()
      }
      this.resultWayChoosed = !this.resultWayChoosed
    },
    jumpToWeighting: function () {
      jQuery('html, body').animate({ scrollTop: jQuery('#weighting').offset().top }, 10) // eslint-disable-line no-undef
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
  .back-button{
    display: block;
    margin-bottom: 1em;
  }
</style>

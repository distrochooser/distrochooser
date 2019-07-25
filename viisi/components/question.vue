<template lang="pug">
  div.question(v-if="isLoaded")
    div(v-if="isAtWelcomeScreen")
      div.question-content
        div.welcome-text 
          h1 {{ __i("welcome-text-title") }}
          p {{ __i("welcome-text") }}
          p
            div 
              i.fas.fa-forward
              span {{ __i("welcome-text-skip") }}
            div
              i.fas.fa-play
              span {{ __i("welcome-text-result-get") }}
            div
              i.fas.fa-sort-amount-up
              span {{ __i("welcome-text-order") }}
            div
              i.fas.fa-trash-alt
              span {{ __i("welcome-text-remove") }}
            div
              i.fas.fa-heart
              span {{ __i("welcome-text-feedback") }}
            div
              i.fas.fa-bug
              span(style="color: red") This is an early version. Expect bugs and unfinished parts.
        div.actions
          button.start-test-button.next-step.step(@click="startTest") {{ __i("start-test") }}
    div(v-else)
      div.question-content
        div.additional-infos.animated.fadeIn.fast(v-if="additionalInfoShown")
          div.additional-info-menu(v-on:click="flip")
            span {{ __i("close-additional-info") }}
            i.fas.fa-times-circle
          h3 {{ __i("additional-info") }} | {{ __i($store.state.currentCategory.msgid) }}
          div {{ __i(question.additionalInfo) }}
        div.question-text(v-if="!additionalInfoShown")
          span {{ __i(question.msgid) }}
        div.answer-remark(v-if="question.isMultipleChoice")
          span {{ __i("question-is-multiplechoice") }}
        div.answers(:class="{'flipped': additionalInfoShown}")
          div.answer(v-for="(answer, a_key) in answers", :key="a_key",:class="{'answer-selected': isAnswerSelected(answer)}",@click='answerQuestion(answer)')
            span(v-if="question.isMultipleChoice")
              i.far.answer-box(:class="{'fa-check-square': isAnswerSelected(answer), 'fa-square': !isAnswerSelected(answer)}")
            span(v-else)
              i.far.answer-box(:class="{'fa-check-circle': isAnswerSelected(answer), 'fa-circle': !isAnswerSelected(answer)}")
            label {{ __i(answer.msgid) }}
            div.warning-alert.animated.fadeInUp.faster(v-if="getBlockingAnswers(answer).length > 0 &&  isAnswerSelected(answer)")
              p {{ __i("answer-is-blocking") }}:
              div(v-for="(blockingAnswer, blockingAnswer_key) in getBlockingAnswers(answer)", :key="blockingAnswer_key") 
                i.fas.fa-times-circle
                span "{{ __i(blockingAnswer.msgid) }}"
            div.blocking-alert.animated.fadeInUp.faster(v-if="getBlockedAnswers(answer).length > 0 &&  isAnswerSelected(answer)")
              p {{ __i("answer-is-blocked") }}:
              div(v-for="(blockingAnswer, blockingAnswer_key) in getBlockedAnswers(answer)", :key="blockingAnswer_key") 
                i.fas.fa-times-circle
                span "{{ __i(blockingAnswer.msgid) }}"
      div.actions(v-if="!additionalInfoShown")
        div.additional-remarks-action
          span.additional-remarks-button(v-if="question.additionalInfo",:data-balloon="__i('additional-infos')",data-balloon-pos="left")
            i.far.fa-question-circle.additional-info-icon(v-on:click="flip")
        button.back-step.step(@click="prevQuestion",v-if="!isAtFirstQuestion()") {{  __i("prev-question") }}
        button.next-step.step(@click="nextQuestion") {{  __i(isAtLastQuestion() ? "get-result" : "next-question") }}
</template>
<script>
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  props: {
    language: {
      type: String,
      required: true,
      default: 'en'
    }
  },
  data: function() {
    return {
      additionalInfoShown: false
    }
  },
  computed: {
    isLoaded() {
      return this.$store.state !== null
    },
    question() {
      return this.$store.state.question
    },
    answers() {
      return this.$store.state.answers
    },
    isAtWelcomeScreen() {
      return !this.$store.state.isStarted
    }
  },
  watch: {
    question: function() {
      this.additionalInfoShown = false
    }
  },
  methods: {
    flip() {
      this.additionalInfoShown = !this.additionalInfoShown
    },
    isQuestionAnswered() {
      if (!this.$store.state.currentCategory) {
        return false
      }
      return this.getAnswers().length > 0
    },
    getAnswers() {
      const categoryId = this.$store.state.currentCategory.msgid
      return this.$store.state.givenAnswers.filter(function(answer) {
        return answer.category === categoryId
      })
    },
    getBlockingAnswers(answer) {
      // Case: A given answer is blocked because the current answer excludes them
      return this.$store.state.givenAnswers.filter(function(givenAnswer) {
        return answer.blockedAnswers.indexOf(givenAnswer.msgid) !== -1
      })
    },
    getBlockedAnswers(answer) {
      // Case: A given answer excludes a given answer
      const category = this.$store.state.currentCategory.msgid
      return this.$store.state.givenAnswers.filter(function(givenAnswer) {
        if (givenAnswer.category === category) {
          return false // ignore same category matches as they are already displayed by getBlockingAnswers()
        }
        return givenAnswer.blockedAnswers.indexOf(answer.msgid) !== -1
      })
    },
    answerQuestion(answer) {
      if (this.isAnswerSelected(answer)) {
        this.$store.commit('removeAnswerQuestion', answer)
      } else {
        if (!this.question.isMultipleChoice && this.isQuestionAnswered()) {
          // switch an answer in non multiple choice questions
          var otherAnswers = this.getAnswers()
          const _t = this
          otherAnswers.forEach(function(a) {
            _t.$store.commit('removeAnswerQuestion', a)
          })
        }
        if (this.question.isMultipleChoice || !this.isQuestionAnswered()) {
          this.$store.dispatch('answerQuestion', {
            selectedAnswer: answer,
            currentCategory: this.$store.state.currentCategory
          })
        }
      }
    },
    startTest() {
      var _t = this
      this.$store.dispatch('nextQuestion', {
        params: {
          language: _t.language
        }
      })
    },
    nextQuestion() {
      var _t = this
      if (!this.isAtLastQuestion()) {
        this.$store.dispatch('nextQuestion', {
          params: {
            language: _t.language
          }
        })
      } else {
        this.$store.dispatch('submitAnswers', {
          params: {
            token: this.$store.state.token,
            language: _t.language
          },
          data: {
            answers: this.$store.state.givenAnswers
          }
        })
      }
    },
    prevQuestion() {
      var _t = this
      this.$store.dispatch('prevQuestion', {
        params: {
          language: _t.language
        }
      })
    },
    isAtLastQuestion() {
      var currentIndex = this.$store.state.currentCategory.index
      var maximumIndex = Math.max.apply(
        Math,
        this.$store.state.categories.map(function(c) {
          return c.index
        })
      )
      return currentIndex === maximumIndex
    },
    isAtFirstQuestion() {
      var currentIndex = this.$store.state.currentCategory.index
      var minIndex = Math.min.apply(
        Math,
        this.$store.state.categories.map(function(c) {
          return c.index
        })
      )
      return currentIndex === minIndex
    },
    isAnswerSelected(answer) {
      return (
        this.$store.state.givenAnswers.filter(a => a.msgid === answer.msgid)
          .length === 1
      )
    },
    markImportant(answer) {
      this.$store.commit('toggleImportanceState', answer)
    }
  }
}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
@import '~/node_modules/animate.css/animate.min.css';
@import '~/node_modules/balloon-css/balloon.min.css';
.question {
  margin-top: 1em;
  height: 60%;
  width: 80%;
  margin-right: 10%;
  margin-left: 10%;
}
@media only screen and (max-width: $mobileWidth) {
  .question {
    width: 90%;
    margin-left: 5%;
    margin-right: 5%;
  }
  .next-step {
    left: 80% !important;
  }
}

@media only screen and (max-width: $desktopMinWidth) {
  .question {
    width: 90%;
    margin-left: 5%;
    margin-right: 5%;
  }
}
.welcome-text {
  padding: 2em;
  font-size: 13pt;
  font-family: 'Archivo', sans-serif;
  line-height: 2;
  height: 23em;
}
.question-text {
  padding-top: 2em;
  padding-left: 2em;
  padding-right: 2em;
  padding-bottom: 1em;
  font-family: 'Roboto Slab';
  font-size: 21px;
  line-height: 1.7;
}
.welcome-text b {
  margin-bottom: 1em;
  display: block;
  padding-bottom: 0.5em;
  display: block;
  color: #4484ce;
}
ul {
  padding-top: 0.5em;
}
.answers {
  margin-left: 2em;
}
.answer {
  color: $unselectedAnswerForeground !important;
  min-height: 40px;
  padding: 10px;
  font-family: Open Sans, sans-serif;
  cursor: pointer;
}
.answer-text {
  padding-left: 2em;
  padding-right: 2em;
  font-size: 11pt;
}
.answer-selected {
  color: $selectedAnswerBackground !important;
  font-weight: bold;
}
.actions {
  display: flex;
  justify-content: flex-end;
  padding-bottom: 1em;
  background: $questionBackground;
  padding-right: 1em;
}
.step {
  color: black;
  padding: 0.7rem 1.4rem;
  border: 1px solid $nextButtonBackground;
  margin-left: 1rem;
  cursor: pointer;
  border-radius: 4px;
  font-family: 'Open Sans';
  font-size: 12pt;
}
.skip-step {
  position: relative;
  left: 95%;
  top: 0.5em;
  display: inline;
  color: $skipButtonColor;
}
.next-step {
  background: $lightColor;
  color: white;
  border: 1px solid $nextButtonBackground;
}
.back-step:hover {
  background: $lightColor;
  color: white;
  border: 1px solid $nextButtonBackground;
}
.next-step:hover {
  color: black;
  background: white;
  border: 1px solid $nextButtonBackground;
}
.answer-remark {
  font-family: Open Sans;
  font-style: italic;
  font-size: 11pt;
  position: relative;
  left: 5%;
  bottom: 0.5em;
  margin-left: -0.5em;
  padding-top: 1em;
  padding-bottom: 1em;
}
.mark-important {
  display: none; // it's disabled until I find a proper solution
}
.is-important {
  color: $markImportantSelectedColor;
}
// Flag addition
.flag-icon-en {
  background-image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGlkPSJmbGFnLWljb24tY3NzLWdiIiB2aWV3Qm94PSIwIDAgNjQwIDQ4MCI+CiAgPGRlZnM+CiAgICA8Y2xpcFBhdGggaWQ9ImEiPgogICAgICA8cGF0aCBmaWxsLW9wYWNpdHk9Ii43IiBkPSJNLTg1LjMgMGg2ODIuNnY1MTJILTg1LjN6Ii8+CiAgICA8L2NsaXBQYXRoPgogIDwvZGVmcz4KICA8ZyBjbGlwLXBhdGg9InVybCgjYSkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDgwKSBzY2FsZSguOTQpIj4KICAgIDxnIHN0cm9rZS13aWR0aD0iMXB0Ij4KICAgICAgPHBhdGggZmlsbD0iIzAxMjE2OSIgZD0iTS0yNTYgMEg3Njh2NTEySC0yNTZ6Ii8+CiAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0tMjU2IDB2NTcuMkw2NTMuNSA1MTJINzY4di01Ny4yTC0xNDEuNSAwSC0yNTZ6TTc2OCAwdjU3LjJMLTE0MS41IDUxMkgtMjU2di01Ny4yTDY1My41IDBINzY4eiIvPgogICAgICA8cGF0aCBmaWxsPSIjZmZmIiBkPSJNMTcwLjcgMHY1MTJoMTcwLjZWMEgxNzAuN3pNLTI1NiAxNzAuN3YxNzAuNkg3NjhWMTcwLjdILTI1NnoiLz4KICAgICAgPHBhdGggZmlsbD0iI2M4MTAyZSIgZD0iTS0yNTYgMjA0Ljh2MTAyLjRINzY4VjIwNC44SC0yNTZ6TTIwNC44IDB2NTEyaDEwMi40VjBIMjA0Ljh6TS0yNTYgNTEyTDg1LjMgMzQxLjNoNzYuNEwtMTc5LjcgNTEySC0yNTZ6bTAtNTEyTDg1LjMgMTcwLjdIOUwtMjU2IDM4LjJWMHptNjA2LjQgMTcwLjdMNjkxLjcgMEg3NjhMNDI2LjcgMTcwLjdoLTc2LjN6TTc2OCA1MTJMNDI2LjcgMzQxLjNINTAzbDI2NSAxMzIuNVY1MTJ6Ii8+CiAgICA8L2c+CiAgPC9nPgo8L3N2Zz4K);
}
.languages {
  padding: 2em;
  padding-top: 0em;
}
.flag-icon {
  margin-right: 0.5em;
}
.locale-container {
  margin-top: 0.5em;
}
a {
  color: $linkColor;
  text-decoration: none;
}
.question-content {
  background: $questionBackground;
  padding-bottom: 1em;
}
-test {
  position: relative;
  bottom: 22em;
  text-align: right;
}
.answer input {
  vertical-align: middle;
  margin-right: 1em;
  margin-left: 1em;
}
.fa-check-circle,
.fa-check-square {
  color: $answeredColor;
}
.answer-box {
  font-size: 1.5em;
  vertical-align: sub;
}
.additional-remarks-button {
  margin-left: 0.5em;
}
.additional-infos {
  width: 48%;
  background: $additionalInfoBackground;
  position: absolute;
  z-index: 1000000;
  padding: 1em;
  color: white;
  font-family: 'Roboto Slab';
  font-size: 16pt;
}
.flipped {
  filter: blur(5px);
}
.additional-info-menu {
  text-align: right;
  cursor: pointer;
  margin-bottom: 0.5em;
}
.additional-info-menu span {
  margin-right: 0.5em;
}
.additional-info-icon {
  color: $additionalInfoIcon;
  font-size: 17pt;
}
.additional-remarks-action {
  margin-top: 0.6em;
  margin-right: -0.5em;
}
.start-test-button {
  margin-bottom: -1em;
}
.blocking-alert {
  border: 1px solid red;
  border-radius: 3px;
  padding: 1em;
  font-weight: normal;
  margin-top: 1em;
  background: #ffb5b5;
  color: black;
}
.blocking-alert p,
.warning-alert p {
  margin-bottom: 0.5em;
}
.warning-alert {
  border: 1px solid #ffb180;
  border-radius: 3px;
  padding: 1em;
  font-weight: normal;
  margin-top: 1em;
  background: #ffc300;
  color: black;
}
</style>

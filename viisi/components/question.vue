<template lang="pug">
  div.question(v-if="isLoaded")
    div.skip-container(v-if="!isAtWelcomeScreen")
      a.skip-step.fa.fa-share
    div(v-if="isAtWelcomeScreen")
      div.welcome-text 
        b welcome text
        ul
          li stuff
          li stuff 
          li stuff
        blockquote even more stuff
      div.actions
        button.next-step(@click="startTest") start
    div(v-else)
      div.question-text {{ question.msgid }}
      div.answer-remark(v-if="question.isMultipleChoice")
        span Multiple answers possible
      div.answers
        div.answer(v-for="(answer, a_key) in answers", :key="a_key",:class="{'answer-selected animated pulse fast': isAnswerSelected(answer)}")
          span.answer-text(@click='answerQuestion(answer)') {{ answer.msgid }}
          div.mark-important(v-if="isAnswerSelected(answer)",:class="{'is-important': answer.isImportant}", @click="markImportant(answer)")
            i.fa.fa-exclamation
      div.actions
        button.next-step(@click="nextQuestion") {{ isAtLastQuestion() ? "get result" : "next" }}
</template>
<script>
export default {
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
  methods: {
    answerQuestion(answer) {
      if (this.isAnswerSelected(answer)) {
        this.$store.commit('removeAnswerQuestion', answer)
      } else {
        this.$store.dispatch('answerQuestion', {
          selectedAnswer: answer
        })
      }
    },
    startTest() {
      this.$store.dispatch('nextQuestion')
    },
    nextQuestion() {
      if (!this.isAtLastQuestion()) {
        this.$store.dispatch('nextQuestion')
      } else {
        this.$store.dispatch('submitAnswers', {
          params: {
            token: this.$store.state.token
          },
          data: {
            answers: this.$store.state.givenAnswers
          }
        })
      }
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
.question {
  margin-top: 4em;
  width: 70%;
  margin-right: 15%;
  margin-left: 15%;
  background: $questionBackground;
  height: 25em;
}
@media only screen and (max-width: $mobileWidth) {
  .question {
    width: 90%;
    margin-left: 5%;
    margin-right: 5%;
  }
  .answer-remark {
    left: 53% !important;
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
.question-text,
.welcome-text {
  font-family: 'Raleway', sans-serif;
  padding: 2em;
  font-size: 13pt;
  font-weight: 300;
  height: 40%;
}
.answer {
  background: $unselectedAnswerBackground !important;
  color: $unselectedAnswerForeground !important;
  height: 40px;
  padding: 10px;
  font-family: Karla, sans-serif;
  margin-bottom: 1em;
  cursor: pointer;
}
.answer-selected {
  background: $selectedAnswerBackground !important;
  color: $selectedAnswerForeground !important;
  margin-right: -0.5em;
  margin-left: -0.5em;
}
.next-step {
  background: $nextButtonBackground;
  color: $nextButtonForeground;
  position: relative;
  left: 89%;
  height: 30px;
  width: 60px;
  border: 0px;
  cursor: pointer;
}
.skip-step {
  position: relative;
  left: 95%;
  top: 0.5em;
  display: inline;
  color: $skipButtonColor;
}
.answer-remark {
  font-family: karla;
  font-style: italic;
  font-size: 9pt;
  position: relative;
  left: 5%;
  bottom: 1em;
}
.mark-important {
  display: inline-block;
  margin-left: 1em;
}
.is-important {
  color: $markImportantSelectedColor;
}
</style>

<template lang="pug">
  div.question
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
      div.question-text {{ question.title }}
      div.answer-remark(v-if="question.isMultipleChoice")
        span Multiple answers possible
      div.answers
        div.answer(v-for="(answer, a_key) in question.answers", :key="a_key",:class="{'answer-selected animated pulse fast': answer.isAnswered}", @click='answerQuestion(answer)')
          span.answer-text {{ answer.text }}
          div.mark-important(:class="{'is-important': answer.isImportant}")
            i.fa.fa-exclamation
      div.actions
        button.next-step(@click="nextQuestion") {{ isAtLastQuestion() ? "get result" : "next" }}
</template>
<script>
export default {
  computed: {
    question() {
      return this.$store.state.question
    },
    isAtWelcomeScreen() {
      return this.$store.state.category === null
    }
  },
  methods: {
    answerQuestion(answer) {
      this.$store.dispatch('answerQuestion', {
        selectedAnswer: answer
      })
    },
    startTest() {
      this.$store.dispatch('startTest')
    },
    nextQuestion() {
      if (!this.isAtLastQuestion()) {
        this.$store.dispatch('nextQuestion')
      } else {
        console.log('ende')
      }
    },
    isAtLastQuestion() {
      var categoryIndex = this.$store.state.categories.indexOf(
        this.$store.state.category
      )
      return categoryIndex == this.$store.state.categories.length - 1
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

<template lang="pug">
  div.question
    div.skip-container
      a.skip-step.fa.fa-share
    div.question-text lorem ipsum
    div.answer-remark
      span Multiple answers possible
    div.answers
      div.answer 
        span.answer-text fooooo
        div.mark-important
          i.fa.fa-exclamation
      div.answer.answer-selected 
        span.answer-text bar
        div.mark-important.is-important
          i.fa.fa-exclamation
      div.answer
        span.answer-text  barz 
        div.mark-important
          i.fa.fa-exclamation
    div.actions
      button.next-step next
</template>
<script>
export default {}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
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
.question-text {
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
  left: 73%;
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

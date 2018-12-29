<template lang="pug">
  div.question
    div.question-text lorem ipsum
    div.answers
      div.answer fooooo
      div.answer.answer-selected bar
      div.answer barz
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
  bottom: -2.5em;
  height: 30px;
  width: 60px;
  border: 0px;
  cursor: pointer;
}
</style>

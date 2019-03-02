<template lang="pug">
  div.distrochooser
    div.top-logo-container
      img.top-logo(src='~/assets/logo.png')
    categories
    div(v-if="!isFinished")
      question
    div(v-if="isFinished")
      result

</template>
<script>
import categories from '~/components/categories'
import question from '~/components/question'
import result from '~/components/result'
export default {
  components: {
    categories,
    question,
    result
  },
  computed: {
    isFinished: function() {
      return this.$store.state.result !== null
    }
  },
  async mounted() {
    await this.$store.dispatch('startTest')
  }
}
</script>
<style lang="scss">
@import '~/scss/variables.scss';
body {
  background: $background;
}
@media only screen and (max-width: $mobileWidth) {
  .distrochooser {
    width: 100%;
    margin-left: 0px;
    margin-right: 0px;
  }
  .top-logo-container .top-logo {
    width: 50%;
  }
}
@media only screen and (min-width: $mobileWidth) {
  .distrochooser {
    width: 50%;
    margin-left: 25%;
    margin-right: 25%;
  }
  .top-logo-container .top-logo {
    width: 25%;
  }
}
.top-logo-container {
  text-align: center;
}
.fa-facebook {
  color: #3b5998;
}
.fa-twitter {
  color: #1da1f2;
}
</style>

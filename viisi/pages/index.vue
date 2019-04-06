<template lang="pug">
  div.distrochooser
    div.top-logo-container
      a(href="/")
        img.top-logo(src='~/assets/logo.png')
    categories(:language="language")
    div(v-if="!isFinished")
      question(:language="language")
    div(v-if="isFinished")
      result(:language="language")
    div.footer 
      a(href="/imprint")  {{ __i("imprint") }}
      a(href="/privacy") {{ __i("privacy") }}
      a(href="/about") {{ __i("about") }}
</template>
<script>
import categories from '~/components/categories'
import question from '~/components/question'
import result from '~/components/result'
import i18n from '~/mixins/i18n'
export default {
  components: {
    categories,
    question,
    result
  },
  mixins: [i18n],
  data: function() {
    return {
      language: 'en'
    }
  },
  computed: {
    isFinished: function() {
      return this.$store.state.result !== null
    }
  },
  async mounted() {
    const _t = this
    await this.$store.dispatch('getLocales')
    await this.$store.dispatch('startTest', {
      params: {
        language: _t.language
      }
    })
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
.footer {
  position: absolute;
  bottom: 0px;
  padding-bottom: 1em;
  text-align: left;
  width: 100%;
  left: 0px;
  padding-left: 1em;
}
.footer a {
  color: #4484ce;
  text-decoration: none;
  padding-right: 1em;
}
</style>

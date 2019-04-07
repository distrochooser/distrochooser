<template lang="pug">
  div.page
    div(v-if="content=='about'")
      h1 {{ __i("about-header") }}
      p(v-html="__i('about-intro-text')")
      p {{ __i('about-intro-test-count').replace("%s", $store.state.testCount) }}
      h2 {{ __i("about-licenses") }}
      p {{ __i("about-licenses-text") }}
      h2 {{ __i("about-licenses-source") }}
      p {{ __i("about-licenses-source-text") }}
      h2 {{ __i("about-licenses-database") }}
      p {{ __i("about-licenses-database-text") }}
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
    },
    content: {
      type: String,
      required: true,
      default: 'about'
    }
  }
}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
.page {
  display: block;
  margin-top: 2em;
}
</style>

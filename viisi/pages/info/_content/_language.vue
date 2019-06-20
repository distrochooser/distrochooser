<template lang="pug">
  div.page
    div.top-logo-container
      a(href="/")
        img.top-logo(src='/logo.min.svg')
    div(v-if="content")
      div(v-if="content=='about'")
        h1 {{ __ssr__i("about-header",ssrData) }}
        p(v-html="__ssr__i('about-intro-text',ssrData)")
        br
        p {{ __ssr__i('about-intro-test-count',ssrData).replace("%tests%", ssrData.testCount ) }}
        h2 {{ __ssr__i("about-licenses",ssrData) }}
        p {{ __ssr__i("about-licenses-text",ssrData) }}
        h2 {{ __ssr__i("about-licenses-source",ssrData) }}
        p {{ __ssr__i("about-licenses-source-text",ssrData) }}
        h2 {{ __ssr__i("about-licenses-database",ssrData) }}
        p {{ __ssr__i("about-licenses-database-text",ssrData) }}
      div(v-if="content=='imprint'")
        h1 {{ __ssr__i("imprint-header",ssrData) }}
        p(v-html="__ssr__i('imprint-text',ssrData)")
      div(v-if="content=='privacy'")
        h1 {{ __ssr__i("privacy-header",ssrData) }}
        p(v-html="__ssr__i('privacy-text',ssrData)")
</template>
<script>
import axios from 'axios'
import i18n from '~/mixins/i18n'
import viisiConfig from '~/viisi.json'
export default {
  mixins: [i18n],
  async asyncData(context) {
    const language = context.params.language
    const content = context.params.content
    if (typeof language === 'undefined' || typeof content === 'undefined') {
      return {
        content: null,
        language: null
      }
    } else {
      let { data } = await axios.get(
        viisiConfig.backendUrl + 'ssrdata/' + language + '/'
      )
      return {
        ssrData: data,
        content: content
      }
    }
  }
}
</script>
<style>
.page {
  width: 60%;
  margin-left: 20%;
  margin-right: 20%;
  margin-top: 2em;
}
</style>

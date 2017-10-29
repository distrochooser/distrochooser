<template>
    <div class="container">
      <loading></loading>
      <div class="columns" v-if="nuxt.globals.distrochooser.loaded">
          <navigation></navigation>
          <questions></questions>
      </div>
    </div>
</template>

<script>
    import navigation from '../../components/navigation'
    import loading from '../../components/loading'
    import questions from '../../components/questions'
    import i18n from '../../mixins/i18n'
    import api from '../../mixins/api'
    import nuxt from '../../nuxt.config'
    export default {
      validate ({ params }) {
        var langOk = typeof params.lang === 'undefined' || /^.{2}$/.test(params.lang)
        var testOk = typeof params.test === 'undefined' || /^\d+$/.test(params.test)
        return testOk && langOk
      },
      data: function () {
        return {
          questions: [],
          'options': {
            displayExcluded: false,
            displayFilters: false
          },
          introMessage: {
            'id': 'welcome',
            'text': '',
            'title': '',
            'isSingle': false,
            'answers': [
            ],
            excludedBy: null,
            'number': -1,
            'answered': false
          },
          loaded: false
        }
      },
      components: {
        navigation,
        questions,
        loading
      },
      mixins: [api, i18n],
      created: function () {
        nuxt.globals.distrochooser = this
        this.init(nuxt.globals.useragent, nuxt.globals.referrer)
      },
      computed: {
        nuxt: function () {
          return nuxt
        }
      },
      head: function () {
        return {
          meta: [
            {
              hid: 'description',
              name: 'description',
              content: nuxt.globals.descriptions[nuxt.globals.lang]
            },
            {
              property: 'og:description',
              content: nuxt.globals.descriptions[nuxt.globals.lang]
            },
            {
              property: 'og:locale',
              content: nuxt.globals.lang
            },
            {
              name: 'twitter:description',
              content: nuxt.globals.descriptions[nuxt.globals.lang]
            }
          ]
        }
      }
    }
</script>

<style>
  .container{
    padding-top: 1em;
  }
  body{
    font-size: .65rem !important;
  }
  p{
    margin-bottom: 0.5em;
  }
  .btn{
    font-size: .6rem !important;
  }
</style>

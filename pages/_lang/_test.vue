<template>
    <div class="container">
      <div class="columns" v-if="nuxt.globals.distrochooser.loaded">
          <navigation></navigation>
          <questions></questions>
      </div>
    </div>
</template>

<script>
    import navigation from '../../components/navigation'
    import questions from '../../components/questions'
    import i18n from '../../mixins/i18n'
    import api from '../../mixins/api'
    import nuxt from '../../nuxt.config'
    export default {
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
        questions
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
</style>

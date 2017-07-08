<template>
    <div class="container">
      <div class="row" v-if="nuxt.globals.distrochooser.loaded">
          <navigation></navigation>
          <questions></questions>
      </div>
    </div>
</template>

<script>
    import navigation from '../components/navigation'
    import questions from '../components/questions'
    import i18n from '../mixins/i18n'
    import api from '../mixins/api'
    import nuxt from '../nuxt.config'
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
            'help': '',
            'important': false,
            'single': false,
            'answers': [
            ],
            exclusiontags: null,
            'number': -1
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
      },
      computed: {
        nuxt: function () {
          return nuxt
        }
      }
    }
</script>

<style>
  .container{
    padding-top: 1em;
  }
</style>

import axios from 'axios'
import nuxt from '../nuxt.config'

export default {
  created: function () {
    nuxt.globals.useragent = typeof navigator === 'undefined' ? null : navigator.userAgent
    nuxt.globals.referrer = typeof document === 'undefined' ? null : document.referrer
    nuxt.globals.dnt = typeof navigator === 'undefined' ? false : navigator.doNotTrack === 1
    if (this.$route.params.lang !== undefined) {
      var p = this.$route.params.lang
      if (nuxt.globals.locales.indexOf(p) !== -1) {
        nuxt.globals.lang = this.$route.params.lang
      } else {
        nuxt.globals.lang = 'en'
      }
    } else {
      nuxt.globals.lang = 'de'
    }
    if (this.$route.params.test !== undefined) {
      nuxt.globals.test = this.$route.params.test
    }
  },
  methods: {
    init: function () {
      var _t = this
      axios.get(nuxt.globals.backend + 'get/' + nuxt.globals.lang + '/1/1/')
      .then(function (response) {
        _t.nuxt.globals.i18n = response.data.i18n
        _t.nuxt.globals.questions = response.data.questions
        _t.nuxt.globals.distrochooser.questions = nuxt.globals.questions
        _t.nuxt.globals.distros = response.data.distros
        for (var d in response.data) {
          _t[d] = response.data[d]
        }
        nuxt.globals.questions.forEach(function (element) {
          element.open = false
        }, this)
        _t.nuxt.globals.visitor = response.data.id
        console.log('Hello #' + _t.nuxt.globals.visitor)
        nuxt.globals.questions.splice(0, 0, _t.introMessage)
        nuxt.globals.questions[0].text = _t.text('sys.welcometext')
        nuxt.globals.questions[0].title = _t.text('sys.welcometitle')
        nuxt.globals.distrochooser.loaded = true
        if (_t.nuxt.globals.test !== -1) {
          axios.get(nuxt.globals.backend + 'getresult/' + nuxt.globals.test + '/')
          .then(function (response) {
            _t.globals.preloadInfos = response.data
            nuxt.globals.questions.forEach(function (element) {
              var selected = false
              element.answers.forEach(function (answer) {
                if (_t.globals.preloadInfos.answers.indexOf(answer.id) !== -1) {
                  answer.selected = true
                  selected = true
                }
              }, this)
              element.answered = selected
            }, this)
          })
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    addResult: function (instance) {
      var tags = this.globals.mainInstance.tags // eslint-disable-line no-unused-vars
      var answers = [] // eslint-disable-line no-unused-vars

      this.globals.mainInstance.answered[0].answers.forEach(function (answer) {
        if (answer.selected) {
          answers.push(answer.id)
        }
      })
      var tagsToSubmit = []
      for (var tag in tags) {
        var element = {
          'name': tag,
          'weight': parseInt(tags[tag].weight),
          'negative': tags[tag].negative,
          'amount': tags[tag].amount
        }
        tagsToSubmit.push(element)
      }
      var _t = this
      axios.post(nuxt.globals.backend + 'addresult/' + nuxt.globals.lang + '/1/' + nuxt.globals.visitor + '/', {
        'answers': answers,
        'tags': tagsToSubmit
      })
      .then(function (response) {
        _t.globals.test = response.data
        instance.displayTest = _t.globals.test
      })
    }
  }
}

import axios from 'axios'
import nuxt from '../nuxt.config'

export default {
  data () {
    return {}
  },
  created: function () {
    this.init()
  },
  methods: {
    init: function () {
      var _t = this
      axios.post(nuxt.globals.backend + 'get/' + nuxt.globals.lang + '/', {
        'useragent': 'foo',
        'dnt': true
      })
      .then(function (response) {
        _t.nuxt.globals.i18n = response.data.i18n
        _t.nuxt.globals.questions = response.data.questions
        _t.nuxt.globals.distrochooser.questions = nuxt.globals.questions
        for (var d in response.data) {
          _t[d] = response.data[d]
        }
        nuxt.globals.questions.forEach(function (element) {
          element.open = false
        }, this)

        nuxt.globals.questions.splice(0, 0, _t.introMessage)
        nuxt.globals.questions[0].text = _t.text('welcomeTextHeader')
        nuxt.globals.questions[0].help = _t.text('welcomeText')
        nuxt.globals.distrochooser.loaded = true
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}

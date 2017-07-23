import axios from 'axios'
import nuxt from '../nuxt.config'

export default {
  data () {
    return {}
  },
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
    this.init()
  },
  methods: {
    init: function () {
      var _t = this
      axios.post(nuxt.globals.backend + 'get/' + nuxt.globals.lang + '/', {
        'useragent': nuxt.globals.useragent,
        'dnt': nuxt.globals.dnt,
        'referrer': nuxt.globals.referrer
      })
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
        _t.nuxt.globals.visitor = response.data.visitor
        console.log('Hello #' + _t.nuxt.globals.visitor)
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

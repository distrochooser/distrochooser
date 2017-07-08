import nuxt from '../mixins/nuxt-wrapper'
export default {
  mixins: [
    nuxt
  ],
  methods: {
    text: function (value) {
      return this.globals.i18n !== null && typeof this.globals.i18n[value] !== 'undefined' ? this.globals.i18n[value].val : value
    },
    translateExcludedTags: function (answer) {
      var result = this.text('excludes') + ': <br>'
      var _t = this
      answer.notags.forEach(function (t) {
        var text = _t.text(t)
        if (text !== '') {
          result += _t.text(t) + '<br>'
        }
      })
      return result.trim()
    }
  }
}

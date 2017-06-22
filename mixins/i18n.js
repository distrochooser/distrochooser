export default {
  data () {
    return {
      i18n: {}
    }
  },
  methods: {
    text: function (value) {
      return this.i18n !== null && typeof this.i18n[value] !== 'undefined' ? this.i18n[value].val : ''
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

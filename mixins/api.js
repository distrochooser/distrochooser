import axios from 'axios'
export default {
  data () {
    return {
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
  methods: {
    init: function () {
      var _t = this
      axios.post(this.backendUrl + 'get/' + this.lang + '/', {
        'useragent': 'foo',
        'dnt': true
      })
      .then(function (response) {
        _t.questions = response.data.questions
        _t.i18n = response.data.i18n
        for (var d in response.data) {
          _t[d] = response.data[d]
        }
        _t.questions.forEach(function (element) {
          element.open = false
        }, this)

        _t.questions.splice(0, 0, _t.introMessage)
        _t.questions[0].text = _t.text('welcomeTextHeader')
        _t.questions[0].help = _t.text('welcomeText')
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}

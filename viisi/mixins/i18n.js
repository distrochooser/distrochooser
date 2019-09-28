export default {
  methods: {
    __i: function(val) {
      return this.$store.state.translations !== null &&
        typeof this.$store.state.translations[val.toLowerCase()] !== 'undefined'
        ? this.$store.state.translations[val.toLowerCase()]
        : val
    },
    __ssr__i: function(val, translations) {
      return translations !== null &&
        typeof translations[val.toLowerCase()] !== 'undefined'
        ? translations[val.toLowerCase()]
        : val
    },
    welcomeText: function(locale) {
      var texts = {
        de:
          'Die Linux Auswahlhilfe hilft Anfängern und Umsteigern in der Menge von Linux-Distributionen die passende Linux-Distribution zu finden.',
        en:
          'The Distrochooser helps you to find the suitable Linux distribution based on your needs!',
        fr:
          'Le Distrochooser vous aide à trouver le linux distribution approprié en fonction de vos besoins',
        'zh-cn': '您好！本问卷测试将帮助您选择最适合您使用的 Linux 发行版'
      }
      if (typeof texts[locale] !== 'undefined') {
        return texts[locale]
      }
      return texts['en']
    }
  }
}

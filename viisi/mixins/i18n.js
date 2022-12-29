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
    numberWithSuffix: function(val) {
      if (val == 1){
        return val + this.__i("number-first")
      }
      if (val == 2){
        return val + this.__i("number-second")
      }
      if (val == 3){
        return val + this.__i("number-third")
      }
      return val + this.__i("number-afterthird")
    }
  }
}

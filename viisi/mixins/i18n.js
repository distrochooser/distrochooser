export default {
  methods: {
    __i: function(val) {
      return this.$store.state.translations !== null &&
        typeof this.$store.state.translations[val] !== 'undefined'
        ? this.$store.state.translations[val]
        : val
    }
  }
}

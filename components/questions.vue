<template>
  <div>
    test
  </div>
</template>
 
<script>
import Vue from 'vue' // eslint-disable-line no-unused-vars
import axios from 'axios'
export default {
  data: function () {
    return {
      'backend': 'https://distrochooser.de/distrochooser-backend-php',
      'lang': 'de'
    }
  },
  created: function () {
    this.init()
  },
  computed: {
    backendUrl: function () {
      return this.backend + '/'
    }
  },
  methods: {
    init: function () {
      axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
      axios.post(this.backendUrl + 'get/' + this.lang + '/', {
        'useragent': 'foo',
        'dnt': true
      })
      .then(function (response) {
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}
</script>
 
<style scoped>

</style>

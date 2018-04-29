<template>
    <div class="empty" v-if="isEnabled">
      <div class="empty-icon">
        <i class="icon icon-location"></i>
      </div>
      <h4 class="empty-title">Do you like distrochooser.de and want to help us?</h4>
      <div class="empty-action">       
        <nuxt-link to="/translate">
          Help us with providing a translation into your language!
        </nuxt-link>
        Thank you <i class="icon icon-emoji"></i>!
      </div>
    </div>
</template>
<script>
  import  config from '~/nuxt.config'
  export default{
    computed: {
      isEnabled: function () {
        var found = false
        if (process.server){
          return false
        } else {
          config.globals.locales.forEach(function (l){
            navigator.languages.forEach(function (n){
              if (new RegExp(l).test(n)){
                //matched
                found = true
              }
            })
          })
          return !found
        }
      }
    }
  }
</script>
<style scoped>
.empty {
  margin-bottom: 1em;
  padding: 1em;
}
</style>

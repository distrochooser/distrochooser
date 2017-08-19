<template lang="html">
  <div class="columns loader" v-if="!this.nuxt.globals.distrochooser.loaded">
    <div class="column col-3 hide-xs">
    </div>
    <div class="column col-1 loader-image hide-xs">
      <img src="/logo.png">
    </div>
    <div class="column col-6 loader-text hide-xs">
     <h1>{{ this.nuxt.globals.welcomeHeader[this.nuxt.globals.lang] }} </h1>
     <p v-html="this.nuxt.globals.longDescriptions[this.nuxt.globals.lang]"></p>
    </div>
    <div class="column show-xs mobile-text">
      <div class="centered mobile-logo">
        <img src="/logo.png">
      </div>
      <h1>{{ this.nuxt.globals.welcomeHeader[this.nuxt.globals.lang] }} </h1>
      <p v-html="this.nuxt.globals.longDescriptions[this.nuxt.globals.lang]"></p>
    </div>
    <div class="footer">
     <a :href="'/info/'+this.nuxt.globals.lang+'/contact/'"> {{ this.nuxt.globals.lang === 'de'? 'Impressum' : 'Contact'}}</a>
     <a :href="'/info/'+this.nuxt.globals.lang+'/privacy/'"> {{ this.nuxt.globals.lang === 'de'? 'Datenschutz' : 'Privacy'}}</a>
    </div>
  </div>
</template>

<script>
import nuxt from '../nuxt.config'
export default {
  computed: {
    nuxt: function () {
      return nuxt
    }
  }
}
</script>

<style scoped>
  .loader-text{
    border-left: 1px solid #50596c;
    padding-top: 1.6em;
    margin-top: 15%;
    text-align: justify;
  }
  .loader-image{
    margin-top: 18%;
  }
  .loader-indicator{
    margin-top:1em;
    display: block;
    font-weight: bold;
  }
  .mobile-logo{
    display: block;
    text-align: center;
    margin-bottom: 2em;
  }
  .mobile-text{
    text-align: justify;
  }
  .footer{
    position: fixed;
    bottom: 0px;
    margin-bottom: 1em;
    margin-left: 1em;
    text-align: center;
    width: 100%;
  }
  .footer *:after {
    content: " |"
  }
  .footer *:last-child:after {
    content: ""
  }
  h1{
    font-size: 2em;
    text-align: left;
  }
</style>

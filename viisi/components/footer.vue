<template lang="pug">
div.footer(aria-role="contentinfo")
  a(target="_blank", :href="'/info/imprint/'+ language" )  {{ __i("imprint") }}
  a(target="_blank", :href="'/info/privacy/'+ language" ) {{ __i("privacy") }}
  a(target="_blank", :href="'/info/about/'+ language" ) {{ __i("about") }}
  a(target="_blank", href="https://github.com/distrochooser/distrochooser" )  {{ __i("github-link") }}
  a(target="_blank", href="https://chmr.eu") {{ __i("vendor-text") }}
</template>
<script> 
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  data: function() {
    return {}
  },
  props: {
    language: {
      type: String,
      default: ''
    },
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
.footer {
  position: static;
  padding-top: 1em;
  text-align: center;
}
.footer a {
  color: $linkColor;
  text-decoration: none;
  padding-right: 1em;
  font-size: small;

  .w-icon-github {
    vertical-align: text-top;
    margin-left: 0.5em;
  }
}

.footer select {
  margin-top: 0.5em;
  vertical-align: baseline;
  margin-right: 1.5em;
}
</style>
<template lang="pug">
  div.result
    div.result-link
      div.social-links
        span Share your result
        a(:href="'https://www.facebook.com/sharer/sharer.php?u='+$store.state.result.url")
          i.fab.fa-facebook
        a(:href="'https://twitter.com/share?url='+$store.state.result.url+'&hashtags=distrochooser,linux&via=distrochooser'")
          i.fab.fa-twitter
      div.link
        input(type="text", :value="$store.state.result.url", @focus="$event.target.select()")
    distribution(v-for="(selection, selection_key) in selections", :key="selection_key", :name="selection.distro.name", :description="selection.distro.description", :reasons="selection.reasons", :fgColor="selection.distro.fgColor", :bgColor="selection.distro.bgColor", :id="selection.distro.identifier", :selection="selection.selection", :logo="'/'+selection.distro.identifier+'.png'")
  
    div(v-if="isEmpty")
      h1 {{ __i("no-results")}}
      p {{ __i("no-results-text")}}
</template>
<script>
import distribution from '~/components/distribution'
import i18n from '~/mixins/i18n'
export default {
  components: {
    distribution
  },
  mixins: [i18n],
  computed: {
    selections: function() {
      return this.$store.state.result.selections.concat().sort(function(a, b) {
        return a.score < b.score
      })
    },
    isEmpty: function() {
      var nonEmpty = 0
      this.selections.forEach(element => {
        if (element.reasons.length !== 0) {
          nonEmpty++
        }
      })
      return nonEmpty === 0
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
.result {
  width: 70%;
  margin-right: 15%;
  margin-left: 15%;
  height: 25em;
  font-family: 'Raleway', sans-serif;
}
.link {
  margin-top: 1em;
  font-family: Karla, sans-serif;
}
.link input {
  width: 60%;
  text-align: center;
  padding: 0.7em;
}
.result-link {
  text-align: center;
  margin-bottom: 1em;
}
.social-links i {
  margin-left: 1em;
}
</style>

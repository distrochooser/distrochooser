<template lang="pug">
  div.result
    div.result-link
      div.social-links
        span Share your result
        i.fab.fa-facebook
        i.fab.fa-twitter
      div.link
        input(type="text", :value="$store.state.result.url", @focus="$event.target.select()")
    distribution(v-for="(selection, selection_key) in selections", :key="selection_key", :name="selection.distro.name", :description="selection.distro.description", :reasons="selection.reasons", :fgColor="selection.distro.fgColor", :bgColor="selection.distro.bgColor", :id="selection.distro.identifier", :selection="selection.selection", :logo="'/'+selection.distro.identifier+'.png'")
</template>
<script>
import distribution from '~/components/distribution'
export default {
  components: {
    distribution
  },
  computed: {
    selections: function() {
      return this.$store.state.result.selections.concat().sort(function(a, b) {
        return a.score < b.score
      })
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
.result {
  margin-top: 4em;
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
  width: 50%;
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

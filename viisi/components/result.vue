<template lang="pug">
  div.result
    div.result-link
      div.social-links
        span Share your result
        i.fab.fa-facebook
        i.fab.fa-twitter
      div.link
        a(:href="$store.state.result.url") {{ $store.state.result.url }}
    distribution
</template>
<script>
import distribution from '~/components/distribution'
export default {
  components: {
    distribution
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
}
.result-link {
  text-align: center;
  margin-bottom: 1em;
}
.social-links i {
  margin-left: 1em;
}
</style>

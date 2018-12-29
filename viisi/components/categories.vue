<template lang="pug">
  ul.progressbar
    li(v-for="(category, c_k) in $store.state.categories" v-bind:key="c_k") {{ category }}
  </ul>
</template>

<script>
export default {}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
@media only screen and (min-width: $mobileWidth) {
  .progressbar {
    counter-reset: step;
    padding-left: 14em; //very ugly: FIXME
  }
  .progressbar li {
    width: 7%;
  }
}
@media only screen and (max-width: $mobileWidth) {
  .progressbar {
    counter-reset: step;
    padding-left: 0em !important; //very ugly: FIXME
  }
  .progressbar li {
    width: 10% !important;
  }
}
.progressbar {
  counter-reset: step;
  padding-left: 14em; //very ugly: FIXME
}
.progressbar li {
  list-style-type: none;
  float: left;
  font-size: 11px;
  position: relative;
  text-align: center;
  text-transform: lowercase;
  color: $lightAccent;
  word-wrap: break-word;
  padding-right: 1em;
}
.progressbar li:before {
  width: 15px;
  height: 15px;
  counter-increment: step;
  line-height: 14;
  border: 2px solid $lightAccent;
  display: block;
  text-align: center;
  margin: 0 auto 5px auto;
  border-radius: 50%;
  background-color: white;
  background: white;
  content: '';
}
.progressbar li:hover:before {
  border: 2px solid $activeStepForeground;
  cursor: pointer;
  color: $activeStepForeground;
}
.progressbar li:hover {
  cursor: pointer;
  color: $activeStepForeground;
}
.progressbar li:after {
  width: 100%;
  height: 2px;
  content: '';
  position: absolute;
  background-color: $lightAccent;
  top: 7px;
  left: -50%;
  z-index: -1;
}
.progressbar li:first-child:after {
  content: none;
}
</style>

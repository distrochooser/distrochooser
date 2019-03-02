<template lang="pug">
  ul.progressbar(v-if="isLoaded",v-show="!isAtWelcomeScreen")
    li(@click="restart",:class="{'active': isAtWelcomeScreen }") Welcome
    li(v-for="(category, c_k) in categories" v-bind:key="c_k", :class="{'active': isActive(category)}", @click="selectCategory(category)") {{ category.msgid }}
    li(@click="submit",:class="{'active': $store.state.result !== null }") Your recommendation
</template>

<script>
export default {
  computed: {
    isLoaded() {
      return this.$store.state.categories !== null
    },
    categories() {
      return this.$store.state.categories
    },
    isAtWelcomeScreen() {
      return !this.$store.state.isStarted
    }
  },
  methods: {
    isActive(category) {
      return (
        this.$store.state.result === null &&
        this.$store.state.currentCategory !== null &&
        this.$store.state.currentCategory.msgid === category.msgid
      )
    },
    selectCategory(category) {
      this.$store.dispatch('selectCategory', {
        selectedCategory: category
      })
    },
    restart() {
      this.$store.commit('resetStarted')
    },
    submit() {
      this.$store.dispatch('submitAnswers', {
        params: {
          token: this.$store.state.token
        },
        data: {
          answers: this.$store.state.givenAnswers
        }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
@media only screen and (min-width: $mobileWidth) {
  .progressbar {
    counter-reset: step;
    padding-left: 20em; //very ugly: FIXME
  }
  .progressbar li {
    width: 12%;
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
@media only screen and (max-width: $desktopWidth) {
  .progressbar {
    counter-reset: step;
    padding-left: 0em; //very ugly: FIXME
  }
  .progressbar li {
    width: 10% !important;
  }
}
@media only screen and (min-width: $desktopMinWidth) and (max-width: $desktopWidth) {
  .progressbar {
    counter-reset: step;
    padding-left: 0em; //very ugly: FIXME
  }
  .progressbar li {
    width: 10% !important;
  }
}
.progressbar {
  height: 2em;
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
  width: 20px;
  height: 20px;
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
.active:before {
  border-color: $activeStepForeground !important;
}
.active {
  color: $activeStepForeground !important;
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
  top: 9px;
  left: -50%;
  z-index: -1;
}
.progressbar li:first-child:after {
  content: none;
}
</style>

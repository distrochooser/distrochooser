<template lang="pug">
  div
    ul.progressbar(:class="{'disabled': !isLoaded}")
      li(@click="restart",:class="{'active': isAtWelcomeScreen }") {{ __i("category-welcome") }}
      li(v-for="(category, c_k) in categories" v-bind:key="c_k", :class="{'active': isActive(category), 'answered': isAnswered(category)}", @click="selectCategory(category)") {{ __i(category.msgid) }}
      li(@click="submit",:class="{'active': $store.state.result !== null }",v-if="$store.state.givenAnswers.length > 0") {{ __i("recommendation-category") }}
</template>

<script>
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  props: {
    language: {
      type: String,
      required: true,
      default: 'en'
    }
  },
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
    isAnswered(category) {
      return (
        this.$store.state.givenAnswers.filter(function(a) {
          return a.category === category.msgid
        }).length === 1
      )
    },
    isActive(category) {
      return (
        this.$store.state.result === null &&
        this.$store.state.currentCategory !== null &&
        this.$store.state.currentCategory.msgid === category.msgid
      )
    },
    selectCategory(category) {
      if (this.isAtWelcomeScreen) {
        this.start()
      }
      const _t = this
      this.$store.dispatch('selectCategory', {
        language: _t.language,
        selectedCategory: category
      })
    },
    restart() {
      this.$store.commit('resetStarted')
    },
    start() {
      var _t = this
      this.$store.dispatch('nextQuestion', {
        params: {
          language: _t.language
        }
      })
    },
    submit() {
      if (this.isAtWelcomeScreen) {
        return
      }
      this.$store.dispatch('submitAnswers', {
        params: {
          token: this.$store.state.token,
          language: this.language
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
  }
  .progressbar li {
    width: 8%;
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
  font-size: 13px;
  position: relative;
  text-align: center;
  text-transform: lowercase;
  color: $lightAccent;
  padding-right: 1em;
  word-wrap: initial;
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
.active:before {
  color: $activeStepForeground !important;
}
.answered:before {
  background: $activeStepForeground !important;
  background-color: $activeStepForeground !important;
  border-color: $activeStepForeground !important;
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

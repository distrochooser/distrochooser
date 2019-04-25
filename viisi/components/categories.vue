<template lang="pug">
  div.breadcrumb-container
    div.breadcrumb(:class="{'disabled': !isLoaded}")
      a(href="#",@click="restart",:class="{'active': isAtWelcomeScreen }")
        span.breadcrumb__inner
          span.breadcrumb__title {{ __i("category-welcome") }}
      a(href="#",v-for="(category, c_k) in categories" v-bind:key="c_k", :class="{'active': isActive(category)}", @click="selectCategory(category)")
        span.breadcrumb__inner
          span.breadcrumb__title  
            span.category-status {{ __i(category.msgid) }}
            i(v-if="isAnswered(category)").fa.fa-check.animated.heartBeat
      a(href="#",@click="submit",:class="{'active': $store.state.result !== null }")
        span.breadcrumb__inner
          span.breadcrumb__title {{ __i("recommendation-category") }}
        
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
        }).length > 0
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
      this.$store.commit('toggleSubmitted')
      if (this.isAtWelcomeScreen) {
        this.start()
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
      this.$store.commit('toggleSubmitted')
    }
  }
}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
@import '~/node_modules/animate.css/animate.min.css';
$base: 30px;
// https://codepen.io/iamglynnsmith/pen/BRGjgW
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.breadcrumb-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  position: fixed;
  top: 22px;
  left: 0px;
}

.breadcrumb {
  display: flex;
  overflow: hidden;
  margin: auto;
  text-align: center;
  top: 50%;
  width: 100%;
  // max-width: 1200px;
  height: $base * 1.5;
  transform: translateY(-50%);
  z-index: 1;
  background-color: #ddd;
  font-size: 14px;
}

.breadcrumb a {
  position: relative;
  display: flex;
  flex-grow: 1;
  text-decoration: none;
  margin: auto;
  height: 100%;
  padding-left: $base;
  padding-right: 0;
  color: #666;
}

.breadcrumb a:first-child {
  padding-left: $base / 2.5;
}

.breadcrumb a:last-child {
  padding-right: $base / 2.5;
}

.breadcrumb a:after {
  content: '';
  position: absolute;
  display: inline-block;
  width: $base * 1.5;
  height: $base * 1.5;
  top: 0;
  right: $base / 1.35 * -1;
  background-color: #ddd;
  border-top-right-radius: 5px;
  transform: scale(0.707) rotate(45deg);
  box-shadow: 1px -1px rgba(0, 0, 0, 0.25);
  z-index: 1;
}

.breadcrumb a:last-child:after {
  content: none;
}

.breadcrumb__inner {
  display: flex;
  flex-direction: column;
  margin: auto;
  z-index: 2;
}

.breadcrumb__title {
  font-weight: bold;
}

.breadcrumb a.active,
.breadcrumb a:hover {
  background: $activeStepForeground;
  color: white;
}

.breadcrumb a.active:after,
.breadcrumb a:hover:after {
  background: $activeStepForeground;
  color: white;
}

// 1000px
///////////////////////
@media all and (max-width: 1000px) {
  .breadcrumb {
    font-size: 12px;
  }
}

// 710px
///////////////////////
@media all and (max-width: 710px) {
  .breadcrumb {
    height: $base;
  }

  .breadcrumb a {
    padding-left: $base / 1.5;
  }

  .breadcrumb a:after {
    content: '';
    width: $base * 1;
    height: $base * 1;
    right: $base / 2 * -1;
    transform: scale(0.707) rotate(45deg);
  }
}
.category-status {
  padding-right: 0.5em;
}
</style>

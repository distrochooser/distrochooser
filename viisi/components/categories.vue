<template lang="pug">
    div.breadcrumb-horizontal
      ul
        li
          a(href="#",@click="restart",:class="{'active': isAtWelcomeScreen,'inactive': !isAtWelcomeScreen  }") 
            i.active-indicator.fas.fa-door-open
            span {{ __i("category-welcome") }}
        li(v-for="(category, c_k) in categories" v-bind:key="c_k")
          a(href="#", @click="selectCategory(category)")
            i.active-indicator(:class="category.iconClass + (isAnswered(category) ? ' mobile-answered' : '') + (isActive(category) ? ' mobile-active' : '')")
            span(:class="{'active': isActive(category), 'inactive': !isActive(category)}") {{ __i(category.msgid) }}
            i(v-if="isAnswered(category)").fa.fa-check.animated.heartBeat.isAnswered
        li
          a.get-result(href="#",@click.prevent="submit",:class="{'active': $store.state.result !== null }") 
            i.active-indicator.fas.fa-bullhorn
            span {{ __i("recommendation-category") }}
        
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
    }
  }
}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
@import '~/node_modules/animate.css/animate.min.css';
.breadcrumb-horizontal {
  position: fixed;
  left: 1em;
  top: 24%;
  font-family: Archivo;
  letter-spacing: 0.5px;
}
.breadcrumb-horizontal ul {
  list-style-type: none;
}
.breadcrumb-horizontal ul li {
  margin-bottom: 1em;
}

.breadcrumb-horizontal ul li i {
  color: $categoryIconColor;
}
.breadcrumb-horizontal ul li a {
  text-decoration: none;
}
.inactive {
  color: grey;
}
.active {
  color: $linkColor;
  border-bottom: 1px solid grey;
}
.mobile-answered {
  color: $answeredColor !important;
}
.answered {
  color: $answeredColor !important;
}
.isAnswered {
  // the check mark
  color: $answeredColor !important;
  margin-left: 0.5em;
}
.active-indicator {
  width: 1.2em;
}
.get-result {
  font-weight: bold;
}
</style>

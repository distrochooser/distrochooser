<template lang="pug">
    div.breadcrumb-horizontal
      ul
        li
          a(href="#",@click="restart",:class="{'active': isAtWelcomeScreen,'inactive': !isAtWelcomeScreen  }") 
            i.active-indicator.w-icon-login
            span {{ __i("category-welcome") }}
        li(v-for="(category, c_k) in categories" v-bind:key="c_k", )
          a(href="#", @click="selectCategory(category)")
            i.active-indicator(:class="category.iconClass + (isAnswered(category) ? ' mobile-answered' : '') + (isActive(category) ? ' mobile-active' : '')")
            span(:class="{'active': isActive(category), 'inactive': !isActive(category), 'mobile-answered': isAnswered(category)}") {{ __i(category.msgid) }}
        li(v-if="$store.state.visuallyImpairedMode")
          a(href="#", class="recommendation-link", :aria-disabled="$store.state.givenAnswers.length === 0", @click.prevent="submit", :title="__i('recommendation-category')") {{ __i("recommendation-category") }}


      div.floating-button(v-if="!$store.state.visuallyImpairedMode", :title="__i('recommendation-category')", :class="{'disabled': $store.state.givenAnswers.length === 0}",:data-balloon="__i($store.state.givenAnswers.length === 0 ? 'no-answers' : 'get-my-result')",data-balloon-pos="right",@click.prevent="submit")
        i.w-icon-right-square-o
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
      if (this.$store.state.oldTestData !== null) {
        this.start()
      }
      if (
        this.$store.state.givenAnswers.length === 0 ||
        this.isAtWelcomeScreen
      ) {
        return
      }
      const _t = this
      this.$store.dispatch('submitAnswers', {
        params: {
          token: this.$store.state.token,
          language: this.language,
          method: this.$store.state.method
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
@import '~/node_modules/balloon-css/balloon.min.css';
.breadcrumb-horizontal {
  position: fixed;
  left: 1em;
  font-family: Archivo;
  letter-spacing: 0.5px;
  padding-top: 1em;
}
.breadcrumb-horizontal ul {
  list-style-type: none;
}
.breadcrumb-horizontal ul li {
  margin-bottom: 1em;
}

.breadcrumb-horizontal ul li i {
  color: $categoryIconColor;
  vertical-align: text-bottom;
}
.breadcrumb-horizontal ul li a {
  text-decoration: none;
}
.breadcrumb-horizontal ul li a:focus {
  outline: none;
}
.inactive {
  color: grey;
}
.active {
  color: $linkColor;
  border-bottom: 1px solid grey;
  font-weight: bold;
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
.floating-button-parent {
  position: fixed;
  right: 1em;
  bottom: 15em;
}
.floating-button {
  margin-left: 1.6em;
  background: $linkColor;
  padding: 1em;
  color: white;
}
.floating-button a {
  text-decoration: none;
  color: white;
}
.floating-button a i {
  vertical-align: bottom;
}
.disabled {
  cursor: no-drop;
  background: white;
  color: black;
  border: 1px solid black;
}
.disabled * {
  color: black;
}
.pending-indicator {
  margin-left: 0.5em;
}
</style>

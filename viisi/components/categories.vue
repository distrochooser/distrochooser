<template lang="pug">
.breadcrumb-horizontal
  ul
    li
      a(
        href='#',
        @click='restart',
        :class='{ active: isAtWelcomeScreen && !isAtHardwareScreen, inactive: !isAtWelcomeScreen }'
      ) 
        |
        i.active-indicator.w-icon-login
        span {{ __i('category-welcome') }}
    li(:title='__i("category-hardware-requirements")')
      a(
        href='#',
        @click='openHardwareScreen',
        :class='{ active: isAtHardwareScreen, inactive: !isAtHardwareScreen, answered: $store.state.hardwareRequirements != null }'
      ) 
        |
        i.active-indicator.w-icon-laptop
        span {{ __i('category-hardware-requirements') }}
    li(
      v-for='(category, c_k) in categories',
      v-bind:key='c_k',
      :title='__i(category.msgid)'
    )
      a(href='#', @click='selectCategory(category)')
        i.active-indicator(
          :class='category.iconClass + (isAnswered(category) ? " mobile-answered" : "") + (isActive(category) ? " mobile-active" : "") + (isMarked(category) ? " mobile-marked" : "")'
        )
        span(
          :class='{ active: isActive(category), inactive: !isActive(category), "mobile-answered": isAnswered(category) }'
        ) {{ __i(category.msgid) }}
        i.w-icon-save.marked(v-if='isMarked(category)', :title='__i("marked")')
    li(
      v-if='$store.state.visuallyImpairedMode',
      :title='__i("recommendation-category")'
    )
      a.recommendation-link(
        href='#',
        :aria-disabled='$store.state.givenAnswers.length === 0',
        @click.prevent='submit',
        :title='__i("recommendation-category")'
      ) {{ __i('recommendation-category') }}

  .floating-button(
    v-if='!$store.state.visuallyImpairedMode',
    :title='__i("recommendation-category")',
    :class='{ disabled: $store.state.givenAnswers.length === 0 }',
    :data-balloon='__i($store.state.givenAnswers.length === 0 ? "no-answers" : "get-my-result")',
    data-balloon-pos='right',
    @click.prevent='submit'
  )
    i.w-icon-right-square-o
    span {{ __i('recommendation-category') }}
</template>

<script>
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  props: {
    language: {
      type: String,
      required: true,
      default: 'en',
    },
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
    },
    isAtHardwareScreen() {
      return (
        this.$store.state.isAtHardwareScreen &&
        this.$store.state.result === null
      )
    },
  },
  methods: {
    openHardwareScreen() {
      this.$store.commit('setStarted')

      this.$store.commit('resetResult')
      this.$store.commit('openHardwareScreen')
    },
    closeHardwareScreen() {
      this.$store.commit('closeHardwareScreen')
    },
    isAnswered(category) {
      return (
        this.$store.state.givenAnswers.filter(function (a) {
          return a.category === category.msgid
        }).length > 0
      )
    },
    isActive(category) {
      return (
        this.$store.state.result === null &&
        this.$store.state.currentCategory !== null &&
        this.$store.state.currentCategory.msgid === category.msgid &&
        !this.$store.state.isAtHardwareScreen
      )
    },
    isMarked(category) {
      if (!category) {
        return false
      }
      return this.$store.state.markedQuestions.indexOf(category.msgid) !== -1
    },
    selectCategory(category) {
      const _t = this
      this.$store.dispatch('selectCategory', {
        language: _t.language,
        selectedCategory: category,
      })
    },
    restart() {
      this.closeHardwareScreen()
      this.$store.commit('resetStarted')
    },
    start() {
      var _t = this
      this.$store.dispatch('nextQuestion', {
        params: {
          language: _t.language,
        },
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
          method: this.$store.state.method,
        },
        data: {
          answers: this.$store.state.givenAnswers,
        },
      })
    },
  },
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
  top: 0px;
  padding-top: 5%;
  border-right: 1px solid #89898966;
  height: 100%;
  padding-right: 2.5em;
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
  color: white !important;
}
.floating-button a {
  text-decoration: none;
  color: white !important;
}
.floating-button a i {
  vertical-align: bottom;
}
.disabled {
  cursor: no-drop;
  background: white !important;
  color: black;
  border: 1px solid black;
}
.disabled * {
  color: black;
}
.pending-indicator {
  margin-left: 0.5em;
}
.marked {
  color: $markedHighlightColor !important;
  margin-left: 0.5em;
}
.mobile-marked {
  color: $markedHighlightColor !important;
}
</style>

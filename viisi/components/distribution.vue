<template lang="pug">
  div.distribution(v-if="!hasNoMatch")
    div.title(:style="'background-color: ' + bgColor +'; color: ' + fgColor",:class="{'downvoted-distro': voted && !positiveVote}") 
      span {{ name }}
    div.description {{ __i("description-" + id) }}
    div.description.reasons(v-if="flipped")
      div.reason-list.list
        div(v-if="nonBlocking(reasons).length > 0")
          div(v-for="(reason, reason_key) in nonBlocking(reasons)", :key="reason_key") 
            i.w-icon-plus
            span {{ reason.description }}
            span.importance-toggle(v-if="reason.isImportant")
              i.w-icon-star-on(:title='__i("marked-as-important")')
        div(v-if="negative(reasons).length > 0")
          div(v-for="(reason, reason_key) in negative(reasons)", :key="reason_key") 
            i.w-icon-minus
            span {{ reason.description }}
            span.importance-toggle(v-if="reason.isImportant")
              i.w-icon-star-on(:title='__i("marked-as-important")')
      div.blocking-list.list
        div(v-if="blocking(reasons).length > 0")
          b.block-title {{ __i("reason-list-header-negative").replace("%s",name) }}
          div(v-for="(reason, reason_key) in blocking(reasons)", :key="reason_key") 
            i.w-icon-circle-close-o
            span {{ reason.description }} 
            span.importance-toggle(v-if="reason.isImportant")
              i.w-icon-star-on(:title='__i("marked-as-important")')
      div.blocking-list.list
        div(v-if="blockedByOtherQuestion.length > 0")
          b.block-title {{ __i("reason-list-header-blocked-by-others").replace("%s",name) }}
          div(v-for="(reason, reason_key) in blockedByOtherQuestion", :key="reason_key") 
            i.w-icon-warning
            span {{ reason.description }}
      div.reason-list.list
        div(v-if="neutral.length > 0")
          b.block-title {{ __i("reason-list-header-neutral") }}
          div(v-for="(reason, reason_key) in neutral", :key="reason_key") 
            i.w-icon-question-circle-o
            span {{ reason.description }}
    div.meta
      div.actions
        div.vote-actions
          a.action(href="#", v-on:click.prevent="vote(voted && positiveVote? null : true)",:data-balloon="!$store.state.visuallyImpairedMode ? __i('vote-reminder'): null",data-balloon-pos="left")
            
            i.w-icon-heart-on(v-bind:class="{'animated heartBeat voted': voted && positiveVote}", v-if="!$store.state.visuallyImpairedMode")
            span(v-else) {{ voted && positiveVote ? __i("liked") :  __i("like") }} 

          a.action(href="#", v-on:click.prevent="vote(voted && !positiveVote ? null : false)", :data-balloon="!$store.state.visuallyImpairedMode ? __i('vote-reminder-negative') : null",data-balloon-pos="left")
            i.w-icon-dislike-o(v-bind:class="{'animated swing voted': voted && !positiveVote}", v-if="!$store.state.visuallyImpairedMode")
            span(v-else) {{ voted && !positiveVote? __i("not-liked") :  __i("dislike") }} 
          a.action.hide-reasons(href="#", v-on:click.prevent="flipped=!flipped", :data-balloon="__i('reasons-hide')",data-balloon-pos="right")
            i.w-icon-shrink
      div.url
        a(v-if="url", target="_blank", :href="url") {{ __i("distribution-homepage") }}
</template>
<script>
import i18n from '~/mixins/i18n'
import score from '~/mixins/score'
export default {
  mixins: [i18n, score],
  props: {
    name: {
      type: String,
      default: ''
    },
    id: {
      type: String,
      default: 'linux'
    },
    selection: {
      type: Number,
      default: 0
    },
    logo: {
      type: String,
      default: 'https://distrochooser.de/assets/linux/ubuntu.png'
    },
    url: {
      type: String,
      default: null
    },
    bgColor: {
      type: String,
      default: 'red'
    },
    fgColor: {
      type: String,
      default: 'white'
    },
    reasons: {
      type: Array,
      default: function() {
        return []
      }
    }
  },
  data: function() {
    return {
      flipped: true,
      positiveVote: false,
      voted: false
    }
  },
  computed: {
    neutral: function() {
      return this.reasons.filter(r => {
        return r.isNeutralHit
      })
    },
    blockedByOtherQuestion: function() {
      return this.reasons.filter(r => {
        return r.isRelatedBlocked
      })
    },
    hasNoMatch: function() {
      return this.reasons.length === 0
    }
  },
  methods: {
    vote: function(positive) {
      this.$store.dispatch('voteSelection', {
        data: {
          positive: positive,
          selection: this.selection
        }
      })
      if (positive !== null) {
        this.voted = true
        this.positiveVote = positive
      } else {
        this.voted = false
      }
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
@import '~/node_modules/animate.css/animate.min.css';
@import '~/node_modules/balloon-css/balloon.min.css';
.distribution {
  background: $questionBackground;
  padding-top: 1em;
  margin-bottom: 2em;
}
.title {
  margin-right: -0.5em;
  margin-left: -0.5em;
  height: 40px;
  padding: 10px;
  font-family: Open Sans, sans-serif;
  margin-bottom: 1em;
}
.description {
  margin-left: 1em;
}
.meta .actions {
  width: 50%;
  display: inline-block;
  padding: 1em;
}
.action {
  margin-right: 0.5em;
}
.meta .logo {
  width: 50%;
  display: inline-block;
  text-align: right;
}
.meta .logo img {
  max-height: 2.2em;
  vertical-align: middle;
  margin-right: 1em;
  margin-bottom: 1em;
}
.action i {
  color: $linkColor;
  font-size: 15pt;
}
.action .w-icon-heart-on,
.action .w-icon-dislike-o {
  color: grey;
}
.action .w-icon-heart-on.voted {
  color: #ff1128 !important;
}
.action .w-icon-dislike-o.voted {
  color: black !important;
}
.w-icon-plus {
  color: #1f8c1f;
}
.w-icon-minus {
  color: #f00;
}
.blocking-list div div .w-icon-circle-close-o {
  color: #d40000;
}
.list {
  margin-top: 1em;
}
i {
  margin-right: 0.5em;
}
.block-title {
  padding-bottom: 0.5em;
  display: block;
  color: #000;
}
.show-reasons {
  text-decoration: underline;
  margin-left: 0.2em;
}
.reason-list div {
  margin-bottom: 0.3em;
}
.voted {
  text-shadow: #1e1e1b57 2px 2px 2pt;
}
.url {
  display: inline-block;
  text-align: right;
  width: 50%;
  padding-right: 1em;
}
.url a {
  text-decoration: none;
  color: $linkColor;
}
.scores-summary {
  margin-left: 0.5em;
  margin-right: 0.5em;
}
.scores-summary a {
  text-decoration: none;
}
.summary {
  color: white;
  vertical-align: middle;
  margin-left: 0.4em;
  font-size: 9pt;
}
.downvoted-distro {
  filter: opacity(30%);
}
.downvoted-distro * {
  color: grey;
}
.importance-toggle .w-icon-star-on {
  color: #ff7a00;
  margin-left: 0.5em;
}
.vote-actions {
  display: inline;
}
.vote-actions a {
  text-decoration: none;
}
</style>

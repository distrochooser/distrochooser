<template lang="pug">
  div.distribution(v-if="!hasNoMatch")
    div.title(:style="'background-color: ' + bgColor +'; color: ' + fgColor",:class="{'downvoted-distro': voted && !positiveVote}") 
      span {{ name }}
      span.scores-summary(data-balloon-pos="up", :data-balloon="__i('reason-header-hint')")
        a(href="#", @click.prevent="flipped=!flipped", :style="'color: ' + fgColor")
          span(v-if="nonBlocking(reasons).length !== 0")
            i.fas.fa-thumbs-up.summary(:style="'color: ' + fgColor")
            span {{ nonBlocking(reasons).length }} 
          span(v-if="negative(reasons).length !== 0")
            i.fas.fa-thumbs-down.summary(:style="'color: ' + fgColor")
            span {{ negative(reasons).length + blocking(reasons).length }}
    div.description(v-if="!flipped") {{ __i("description-" + id) }}
    div.description.reasons(v-if="flipped")
      div.reason-list.list
        div(v-if="nonBlocking(reasons).length > 0")
          div(v-for="(reason, reason_key) in nonBlocking(reasons)", :key="reason_key") 
            i.fas.fa-plus
            span {{ reason.description }}
            span.importance-toggle(v-if="reason.isImportant")
              i.fas.fa-star(:title='__i("marked-as-important")')
        div(v-if="negative(reasons).length > 0")
          div(v-for="(reason, reason_key) in negative(reasons)", :key="reason_key") 
            i.fas.fa-minus
            span {{ reason.description }}
            span.importance-toggle(v-if="reason.isImportant")
              i.fas.fa-star(:title='__i("marked-as-important")')
      div.blocking-list.list
        div(v-if="blocking(reasons).length > 0")
          b.block-title {{ __i("reason-list-header-negative").replace("%s",name) }}
          div(v-for="(reason, reason_key) in blocking(reasons)", :key="reason_key") 
            i.fas.fa-ban
            span {{ reason.description }} 
            span.importance-toggle(v-if="reason.isImportant")
              i.fas.fa-star(:title='__i("marked-as-important")')
      div.blocking-list.list
        div(v-if="blockedByOtherQuestion.length > 0")
          b.block-title {{ __i("reason-list-header-blocked-by-others").replace("%s",name) }}
          div(v-for="(reason, reason_key) in blockedByOtherQuestion", :key="reason_key") 
            i.fas.fa-exclamation-triangle
            span {{ reason.description }}
      div.reason-list.list
        div(v-if="neutral.length > 0")
          b.block-title {{ __i("reason-list-header-neutral") }}
          div(v-for="(reason, reason_key) in neutral", :key="reason_key") 
            i.fas.fa-question
            span {{ reason.description }}
    div.meta
      div.actions(:data-balloon="__i('vote-reminder')",data-balloon-pos="left")
        a.action(href="#", v-on:click.prevent="vote(voted && positiveVote? null : true)")
          i.fa-heart(v-bind:class="{'fas animated heartBeat voted': voted && positiveVote, 'far': !voted || !positiveVote}")
        a.action(href="#", v-on:click.prevent="vote(voted && !positiveVote ? null : false)")
          i.fa-heart-broken(v-bind:class="{'fas animated swing voted': voted && !positiveVote, 'fas': !voted || positiveVote}")
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
      flipped: false,
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
.action .fa-heart.voted {
  color: #ff1128 !important;
}
.action .fa-heart-broken.voted {
  color: red !important;
}
.fa-like {
  color: #0e2bff;
}
.fa-plus {
  color: #1f8c1f;
}
.fa-minus {
  color: #f00;
}
.fa-ban {
  color: #d40000;
}
.fa-heart-broken {
  color: #f03c82;
}
.fa-exclamation-triangle {
  color: red;
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
.summary.fa-thumbs-up {
  margin-top: -0.5em;
}
.summary.fa-thumbs-down {
  margin-left: 0.7em;
}
.downvoted-distro {
  filter: opacity(50%);
}
.importance-toggle .fas {
  color: #ff7a00;
  margin-left: 0.5em;
}
</style>

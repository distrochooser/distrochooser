<template lang="pug">
  div.distribution(v-if="!hasNoMatch")
    div.title(:style="'background-color: ' + bgColor +'; color: ' + fgColor") 
      span {{ name }}
      a.show-reasons(href="#", @click.prevent="flipped=!flipped", :style="'color: ' + fgColor")
        span(v-if="!flipped") {{ __i("reason-header".replace("%s",name)) }}
        span(v-if="flipped") {{ __i("hide-reasons")}}
    div.description(v-if="!flipped") {{ __i("description-" + id) }}
    div.description.reasons(v-if="flipped")
      div.reason-list.list
        div(v-if="nonBlocking.length > 0")
          div(v-for="(reason, reason_key) in nonBlocking", :key="reason_key") 
            i.fas.fa-plus(v-if="reason.isPositiveHit")
            i.fas.fa-minus(v-if="!reason.isPositiveHit")
            span {{ reason.description }}
      div.blocking-list.list
        div(v-if="blocking.length > 0")
          b.block-title {{ __i("reason-list-header-negative").replace("%s",name) }}
          div(v-for="(reason, reason_key) in blocking", :key="reason_key") 
            i.fas.fa-ban
            span {{ reason.description }}
      div.blocking-list.list
        div(v-if="blockedByOtherQuestion.length > 0")
          b.block-title {{ __i("reason-list-header-blocked-by-others").replace("%s",name) }}
          div(v-for="(reason, reason_key) in blockedByOtherQuestion", :key="reason_key") 
            i.fas.fa-question
            span {{ reason.description }}
      div.reason-list.list
        div(v-if="neutral.length > 0")
          b.block-title {{ __i("reason-list-header-neutral") }}
          div(v-for="(reason, reason_key) in neutral", :key="reason_key") 
            i.fas.fa-question
            span {{ reason.description }}
    div.meta
      div.actions
        a.action(href="#", v-on:click.prevent="vote(true)")
          i.fa.fa-heart(v-bind:class="{'animated heartBeat voted': voted && positiveVote}")
        a.action(href="#", v-on:click.prevent="vote(false)")
          i.fa.fa-thumbs-down(v-bind:class="{'animated jello voted': voted && !positiveVote}")
      div.logo
        img(:src="logo")
</template>
<script>
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  props: {
    name: {
      type: String,
      default: 'bratwurst'
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
    blocking: function() {
      return this.reasons.filter(r => {
        return r.isBlockingHit && !r.isRelatedBlocked
      })
    },
    nonBlocking: function() {
      return this.reasons.filter(r => {
        return !r.isBlockingHit && !r.isRelatedBlocked && !r.isNeutralHit
      })
    },
    blockedByOtherQuestion: function() {
      return this.reasons.filter(r => {
        return r.isRelatedBlocked
      })
    },
    score: function() {
      return (
        this.nonBlocking.length -
        this.blockedByOtherQuestion.length -
        this.blocking.length
      )
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
      this.voted = true
      this.positiveVote = positive
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
@import '~/node_modules/animate.css/animate.min.css';
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
  font-family: Karla, sans-serif;
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
.fa-heart {
  color: #e40404;
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
.fa-thumbs-down {
  color: #ff8f00;
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
  text-shadow: #1e1e1b 2px 2px 2pt;
}
</style>

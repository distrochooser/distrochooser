<template lang="pug">
  div.distribution
    div.title(:style="'background-color: ' + bgColor +'; color: ' + fgColor") 
      span {{ name }}
      a.show-reasons(href="#", @click.prevent="flipped=!flipped", :style="'color: ' + fgColor")
        span(v-if="!flipped") {{ __i("reason-header".replace("%s",name)) }}
        span(v-if="flipped") {{ __i("hide-reasons")}}
    div.description(v-html="description", v-if="!flipped")
    div.description.reasons(v-if="flipped")
      div.reason-list.list
        div(v-if="nonBlocking.length > 0")
          b.block-title {{ __i("reason-list-header").replace("%s",name) }}
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
    div.meta
      div.actions
        a.action(href="#")
          i.fa.fa-heart
        a.action(href="#")
          i.fa.fa-thumbs-down
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
    description: {
      type: String,
      default: '<p>bla</p><p>bla</p>'
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
      flipped: false
    }
  },
  computed: {
    blocking: function() {
      return this.reasons.filter(r => {
        return r.isBlockingHit && !r.isRelatedBlocked
      })
    },
    nonBlocking: function() {
      return this.reasons.filter(r => {
        return !r.isBlockingHit && !r.isRelatedBlocked
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
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
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
  height: 4em;
  vertical-align: middle;
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
  color: #4484ce;
}
.show-reasons {
  text-decoration: underline;
  margin-left: 0.2em;
}
.reason-list div {
  margin-bottom: 0.3em;
}
</style>

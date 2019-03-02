<template lang="pug">
  div.distribution
    div.title {{ name }}
    div.description(v-html="description", v-if="!flipped")
    div.description.reasons(v-if="flipped")
      div.reason-list.list
        div(v-for="(reason, reason_key) in reasons", :key="reason_key") 
          i.fa.fa-thumbs-up(v-if="reason.isPositiveHit")
          i.fa.fa-thumbs-down(v-if="!reason.isPositiveHit")
          span {{ reason.description }}
      div.blocking-list.list
        div(v-if="blocking.length > 0")
          b.block-title We don't recommend {{ name }} to you because of this reasons:
          div(v-for="(reason, reason_key) in blocking", :key="reason_key") 
            i.fa.fa-thumbs-down
            span {{ reason.description }}
    div.meta
      div.actions
        a.action(href="#")
          i.fa.fa-heart
        a.action(href="#")
          i.fa.fa-thumbs-down
        a.action(href="#", @click="flipped=!flipped")
          span(v-if="!flipped") Why {{ name }}?
          span(v-if="flipped") Hide
      div.logo
        img(:src="logo")
</template>
<script>
export default {
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
        return r.isBlockingHit
      })
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
.distribution {
  background: $questionBackground;
  padding-top: 1em;
  margin-bottom: 3em;
}
.title {
  background: #dd4814 !important;
  color: white !important;
  margin-right: -0.5em;
  margin-left: -0.5em;
  height: 40px;
  padding: 10px;
  font-family: Karla, sans-serif;
  margin-bottom: 1em;
}
.description {
  margin: 1em;
  padding-bottom: 1em;
}
.meta .actions {
  width: 50%;
  display: inline-block;
  padding: 1em;
}
.action {
  margin-right: 1em;
}
.meta .logo {
  width: 50%;
  display: inline-block;
  text-align: right;
}
.meta .logo img {
  height: 5em;
  vertical-align: middle;
}
.fa-heart {
  color: #fe2424;
}
.fa-heart {
  color: #0e2bff;
}
.list {
  margin-bottom: 1em;
  margin-top: 1em;
}
i {
  margin-right: 0.5em;
}
.block-title {
  padding-top: 1em;
  bottom-top: 1em;
}
</style>

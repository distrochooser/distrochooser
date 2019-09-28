<template lang="pug">
  div.result(:class="{'compact-result': compactView}")
    div.result-link
      div.social-links
        span {{ __i("share-result")}}
        a(:href="'https://www.facebook.com/sharer/sharer.php?u='+$store.state.result.url")
          i.fab.fa-facebook-square
        a(:href="'https://twitter.com/share?url='+$store.state.result.url+'&hashtags=distrochooser,linux&via=distrochooser'")
          i.fab.fa-twitter
      div.link
        input(type="text", :value="$store.state.result.url", @focus="$event.target.select()")
      div.remarks
        div(v-if="$store.state.remarksAdded") {{ __i("result-remarks-added")}}
        textarea(v-model="remarks",maxlength="250",:placeholder="__i('remark-placeholder')",v-if="!$store.state.remarksAdded")
        button.add-remarks-button(:data-balloon="__i('no-remark')",data-balloon-pos="left", v-if="!$store.state.remarksAdded", v-on:click="updateRemark",:class="{'disabled': remarks.length === 0}")  {{ __i("result-remarks-button") }}

    distribution(v-for="(selection, selection_key) in selections", :key="selection_key",:name="selection.distro.name", :description="selection.distro.description", :reasons="selection.reasons", :fgColor="selection.distro.fgColor", :bgColor="selection.distro.bgColor", :id="selection.distro.identifier", :selection="selection.selection", :url="selection.distro.url", :class="{'compact-distribution': compactView}")

    div(v-if="isEmpty")
      h1 {{ __i("no-results")}}
      p {{ __i("no-results-text")}}
</template>
<script>
import distribution from '~/components/distribution'
import i18n from '~/mixins/i18n'
import score from '~/mixins/score'
export default {
  components: {
    distribution
  },
  mixins: [i18n, score],
  data: function() {
    return {
      compactView: false,
      remarks: ''
    }
  },
  computed: {
    selections: function() {
      const _t = this
      return this.$store.state.result.selections.concat().sort(function(a, b) {
        return _t.getScore(a.reasons) < _t.getScore(b.reasons)
      })
    },
    isEmpty: function() {
      var nonEmpty = 0
      this.selections.forEach(element => {
        if (element.reasons.length !== 0) {
          nonEmpty++
        }
      })
      return nonEmpty === 0
    }
  },
  methods: {
    updateRemark: function() {
      const resultToken = this.$store.state.result.token
      const remarks = this.remarks
      console.log(this.$store.state.result)
      this.$store.dispatch('addRemarks', {
        data: {
          result: resultToken,
          remarks: remarks
        }
      })
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
@import '~/node_modules/balloon-css/balloon.min.css';
.result {
  width: 70%;
  margin-right: 15%;
  margin-left: 15%;
  height: 25em;
  font-family: 'Open Sans', sans-serif;
}
.compact-result {
  width: unset;
  margin-right: unset;
}
.link {
  margin-top: 1em;
  font-family: Open Sans, sans-serif;
}
.link input {
  width: 50%;
  text-align: center;
  padding: 0.7em;
}
.result-link {
  text-align: center;
  margin-bottom: 1em;
}
.social-links i {
  margin-left: 1em;
}
.compact-distribution {
  display: inline-grid;
  width: 47%;
  height: auto;
  margin-right: 3%;
}
.view-settings {
  text-align: center;
  margin-bottom: 1em;
}
.view-settings a {
  color: $linkColor;
  text-decoration: none;
  padding-right: 1em;
}
.remarks {
  margin-top: 1em;
  padding-bottom: 1em;
}
.remarks textarea {
  width: 50%;
  margin-top: 1em;
  margin-left: 25%;
  margin-right: 25%;
  margin-bottom: 1em;
  font-family: 'Open Sans', sans-serif;
  resize: none;
  padding: 1em;
}
.add-remarks-button {
  border: 0px;
  border-radius: 4px;
  color: white;
  padding: 0.5em;
  background: $linkColor;
  cursor: pointer;
}
.disabled {
  cursor: no-drop;
  background: white;
  color: black;
  border: 1px solid black;
}
</style>

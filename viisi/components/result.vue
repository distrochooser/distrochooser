<template lang="pug">
  div.result(:class="{'compact-result': compactView}")
    div.result-link
      div.social-links(v-if="!$store.state.visuallyImpairedMode")
        span {{ __i("share-result")}}
        span
          a(v-for="(value, key) in $store.state.socialNetworks", :key="key", :href="value.replace('$link$',resultUrl)" , target="_blank")
            i(:class="key")
      div.link(v-if="!$store.state.visuallyImpairedMode", :data-balloon-visible="copyTooltipShown", :data-balloon="copyTooltipShown ? __i('link-copied') : false", data-balloon-pos="down", @click="toggleCopyTooltip(false)", @mouseleave="toggleCopyTooltip(true)")
        i.w-icon-paper-clip
        input(type="text", :name="__i('share-result')", :value="resultUrl", @focus="$event.target.select()")
      footernav(:language="$store.state.language")
      label(v-if="$store.state.visuallyImpairedMode", for="fallback-link",class="fallback-linkshare-label") {{ __i("share-result") }}
      input(v-if="$store.state.visuallyImpairedMode", class="fallback-linkshare", id="fallback-link", aria-role="link", type="text", :name="__i('share-result')", :value="resultUrl", @focus="$event.target.select()")
      div.remarks(aria-role="comment")
        div.remarks-header(v-if="!$store.state.visuallyImpairedMode") {{ __i('remark-placeholder') }}
          span(v-if="$store.state.remarksAdded && remarks.length > 0") {{ " - " + __i('result-remarks-added') }}
        label(v-else,for="remarks-textbox") {{ __i('remark-placeholder') }}
        span(v-if="$store.state.remarksAdded && remarks.length > 0") {{ " - " + __i('result-remarks-added') }}
        textarea(id="remarks-textbox", v-model="remarks",maxlength="3000",:placeholder="__i('remark-placeholder-saving')", @blur="updateRemark", @mouseleave="updateRemark", @input="resetRemarksAdded")
    div.display-options
      span {{ __i('display-options') }}:
      a(href="#",title="List view", v-on:click="() => {listView=true;slideshowView=false;compactView=false}",:class="{'active': listView}")
        i.w-icon-table
      a(href="#",title="Grid view", v-on:click="() => {listView=false;slideshowView=false;compactView=true}",:class="{'active': compactView}")
        i.w-icon-appstore
      a(href="#",title="Slideshow view", v-on:click="() => {listView=false;slideshowView=true;compactView=false;slideShowIndex=0}",:class="{'active': slideshowView}")
        i.w-icon-picture
    div.filtered-results-warning(v-if="!$store.state.showAllResults && filteredSelections.length !==  unfilteredSelections.length", @click="showAllResults") 
      a(href="#") {{ __i("distributions-hidden").replace("#", unfilteredSelections.length - filteredSelections.length) }}
    div(v-if="!slideshowView")
      distribution(aria-role="list-item", v-for="(selection, selection_key) in selections", :ratings="selection.distro.ratings", :age="selection.distro.age", :positive_ratings="selection.distro.positive_ratings", :key="selection_key",:percentage="selection.percentage", :rank="selection.rank", :clicks="selection.distro.clicks" :name="selection.distro.name", :description="selection.distro.description", :reasons="selection.reasons", :fgColor="$store.state.visuallyImpairedMode ? 'white' :  selection.distro.fgColor", :bgColor="$store.state.visuallyImpairedMode ? 'black' : selection.distro.bgColor", :id="selection.distro.identifier", :dbid="selection.distro.id",  :hardware_check="selection.hardware_check", :requirements_check_values="selection.requirements_check_values", :tags="selection.tags", :selection="selection.selection", :url="selection.distro.url", :class="{'compact-distribution': compactView}")
    div(v-if="slideshowView")
      div.slideshow-content(v-if="slideShowElement") 
        
        distribution.slideshow-control.middle(aria-role="list-item", :ratings="slideShowElement.distro.ratings", :age="slideShowElement.distro.age", :positive_ratings="slideShowElement.distro.positive_ratings", :percentage="slideShowElement.percentage", :rank="slideShowElement.rank", :clicks="slideShowElement.distro.clicks" :name="slideShowElement.distro.name", :description="slideShowElement.distro.description", :reasons="slideShowElement.reasons", :fgColor="$store.state.visuallyImpairedMode ? 'white' :  slideShowElement.distro.fgColor", :bgColor="$store.state.visuallyImpairedMode ? 'black' : slideShowElement.distro.bgColor", :id="slideShowElement.distro.identifier", :dbid="slideShowElement.distro.id",  :hardware_check="slideShowElement.hardware_check", :requirements_check_values="slideShowElement.requirements_check_values", :tags="slideShowElement.tags", :selection="slideShowElement.selection", :url="slideShowElement.distro.url", :class="{'compact-distribution': compactView}")
        div.slideshow-navigation-bullets
          div.slideshow-control.left
            div.scroll-button(v-on:click="scroll(-1)") 
              i.w-icon-caret-left
          span(v-for="(result, result_key) in selections.length", :key="result_key")
            a(v-on:click="slideShowIndex=result_key")
              span(:class="{'active': result_key == slideShowIndex}") ⬤
          div.slideshow-control.right
            div.scroll-button(v-on:click="scroll(1)")
              i.w-icon-caret-right
    div(v-if="isEmpty")
      h1 {{ __i("no-results")}}
      p {{ __i("no-results-text")}}
</template>
<script>
import distribution from '~/components/distribution'
import footernav from '~/components/footer'
import i18n from '~/mixins/i18n'
import score from '~/mixins/score'
export default {
  components: {
    distribution,
    footernav
  },
  mixins: [i18n, score],
  data: function() {
    return {
      listView: true,
      compactView: false,
      slideshowView: false,
      remarks: '',
      copyTooltipShown: false,
      unfilteredSelections: [],
      filteredSelections: [],
      slideShowIndex: null
    }
  },
  computed: {
    resultUrl: function() {
      if (this.$store.state.visuallyImpairedMode) {
        return this.$store.state.result.url + '?vim=true'
      }
      return this.$store.state.result.url
    },
    slideShowElement: function (){
      if (this.slideShowIndex != null && this.slideShowIndex < this.selections.length) {
        return this.selections[this.slideShowIndex]
      }
    },
    selections: function() {
      const _t = this
      const sortedSelections = this.$store.state.result.selections
        .concat()
        .sort(function(a, b) {
          return _t.scoreCompare(a, b)
        })
        .filter(function(a) {
          return a.reasons.length > 0
        })
      _t.unfilteredSelections = sortedSelections
      if (this.$store.state.showAllResults){
        _t.filteredSelections = sortedSelections
      } else {
        const selectionsWithPositiveHits = sortedSelections.filter(function(a) {
          return _t.nonBlocking(a.reasons).length > 0
        })
        _t.filteredSelections = selectionsWithPositiveHits
      }
      if (this.$store.state.ratingSort) {
        return _t.filteredSelections.sort(function(a, b) {
          return _t.percentageCompare(a, b)
        })
      } else {
        return _t.filteredSelections
      }
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
    scroll: function (stepping) {
      var new_index = this.slideShowIndex + stepping
      if (new_index < this.selections.length && new_index >= 0) {
        this.slideShowIndex = new_index
      } else {
        if (new_index >= this.selections.length) {
          this.slideShowIndex = 0
        }
        else {
          this.slideShowIndex = this.selections.length -1
        }
      }
    },
    showAllResults: function() {
      this.$store.commit('showAllResults')
      setTimeout(function() { window.scrollTo(0,9999);; }, 200);
    },
    resetRemarksAdded: function() {
      this.$store.commit('resetRemarksAdded')
    },
    updateRemark: function() {
      const resultToken = this.$store.state.result.token
      const sessionToken = this.$store.state.sessionToken
      const remarks = this.remarks
      if (this.$store.state.remarksAdded || remarks.length === 0) {
        return
      }
      this.$store.dispatch('addRemarks', {
        data: {
          sessionToken: sessionToken,
          result: resultToken,
          remarks: remarks
        }
      })
    },
    toggleCopyTooltip: function(forceHide) {
      const shouldBeShown = !this.copyTooltipShown && !forceHide
      if (shouldBeShown) {
        navigator.clipboard.writeText(this.$store.state.result.url)
      }
      this.copyTooltipShown = !this.copyTooltipShown && !forceHide
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
  .compact-distribution {
    display: inline-grid;
    width: 49%;
    height: auto;
    margin-right: 2%;
  }
  .compact-distribution:nth-child(even) {
    margin-right: unset;
  }
}
.link {
  margin-top: 1em;
  font-family: Open Sans, sans-serif;
}
.link input {
  width: 50%;
  text-align: center;
  height: 36px;
  padding-top: 0px;
  padding-bottom: 3px;
  border: 0px;
  cursor: pointer;
}
.result-link {
  text-align: center;
  margin-bottom: 1em;
}
.social-links i {
  margin-left: 1em;
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
  margin-top: 1.5em;
  padding-bottom: 0.5em;
  border-bottom: 1px solid $lightAccent;
  margin-bottom: 1.5em;
}
.remarks textarea {
  width: 100%;
  margin-top: 1em;
  margin-bottom: 1em;
  font-family: 'Open Sans', sans-serif;
  resize: none;
  padding: 1em;
  resize: vertical;
  border: 0px;
  padding-top: 5em;
}
.add-remarks-button {
  border: 0px;
  color: white;
  padding: 0.7em;
  background: $linkColor;
  cursor: pointer;
}
.disabled {
  cursor: no-drop;
  background: white;
  color: black;
  border: 1px solid black;
}
.info-box {
  margin-top: 1em;
  margin-bottom: 1em;
  background: white;
  padding: 0.5em;
  background: $infoBoxBackground;
  color: white;
}
.social-links a {
  text-decoration: none;
}
.w-icon-facebook {
  color: #4267b2;
}
.w-icon-twitter {
  color: #1da1f2;
}
.w-icon-reddit {
  color: #ff4500;
}
.w-icon-paper-clip {
  padding: 10px;
  margin-right: 0px;
  color: white;
  background: $linkColor;
  vertical-align: middle;
  cursor: pointer;
}
.remarks-header {
  border: 1px solid black;
  width: 103%;
  margin-left: -1.5%;
  padding: 0.6em;
  margin-bottom: -4.7em;
  z-index: 100000000000;
  position: relative;
  background: #05396b;
  color: white;
  text-align: left;
  margin-top: 2.5em;
}
.w-icon-check-square,
.w-icon-close-square {
  vertical-align: middle;
  margin-left: 0.4em;
  font-size: 11pt;
}
.fallback-linkshare {
  width: 50%;
  text-align: center;
  font-size: large;
}
.fallback-linkshare-label {
  display: block;
}
div.filtered-results-warning {
  background-color: #05396b;
  margin-right: -0.5em;
  margin-left: -0.5em;
  min-height: 40px;
  padding: 10px;
  font-family: Open Sans, sans-serif;
  margin-bottom: 1em;
  a {
    color: white;
  }
}
.display-options {
  text-align: left;
  margin-top: -1em;
  margin-bottom: 1em;
  span {
    font-weight: bold;
    font-size: 1.2em;
    margin-right: 1em;
  }
  a {
    text-decoration: none;
    i {
      font-size: 1.5em;
      color: $lightAccent;

      &.w-icon-appstore::before {
        content: "\ea07";
      }
    }

    &.active i {
      color: $linkColor;
      
  
      &.w-icon-appstore::before {
        content: "\ea08";
      }
    }
  } 
} 
.slideshow-navigation-bullets {
  text-align: center;
  margin: 0.5em;
  margin-bottom: 1em;
  cursor: pointer;
  span {
    font-size: 8pt;
    margin: 0.5em;
    color: grey;
    &.active {
      color: #3c6eb4;
      font-size: 12pt;
      vertical-align: sub;
    }
  }
}
.slideshow-content {
  .distribution {
    text-align: left;
  }
  .left,
  .right {
    width: 5%;
    display: inline-block;
  }
  .right {
    text-align: right;
    margin-left: 0.5em;
  }
  .left {
    margin-right: 1em;
  }
  .slideshow-control {
    vertical-align: top;
  }
  .scroll-button {
    i {
      font-size: 2em;
      color: #05396b;
    }
  }
}
</style>

<template lang="pug">
  div.tags
    span.header {{ __i("tags-"+answer) }}
    v-select(v-model="selected",:dir="$store.state.inRTLMode ? 'rtl' : 'ltr'", multiple="multiple",label="tags",:options="values")
</template>
<script> 
import { VueSelect as vSelect } from 'vue-select';
import 'vue-select/dist/vue-select.css';
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  data: function() {
    return {
      "selected": []
    }
  },
  props: {
    answer: {
        type: String,
        default: ""
    },
    values: {
      type: Array,
      default: []
    }
  },
  mounted: function (){
    var existingValues = this.$store.state.tags[this.answer]
    if (typeof existingValues === 'undefined') {
      this.selected = [...this.values]
    } else {
      this.selected = this.$store.state.tags[this.answer]
    }
  },
  watch: {
    selected: function(newSelection, oldSelection) {
      this.$store.commit('saveTags',{
        answerId: this.answer,
        selection: newSelection,
        oldSelection: oldSelection
      })
    }
  },
  components: {
    vSelect,
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
div.tags {
  margin-left: 2em;

  .v-select {
    margin-top: 0.5em;
  }
}
</style>
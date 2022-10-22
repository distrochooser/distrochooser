<template lang="pug">
  div.peculiarities
    span.header {{ __i("peculiarities-"+question) }}
    v-select(v-model="selected",:dir="$store.state.inRTLMode ? 'rtl' : 'ltr'", multiple="multiple",label="peculiarities",:options="values")
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
    question: {
        type: String,
        default: ""
    },
    values: {
      type: Array,
      default: []
    }
  },
  mounted: function (){
    var existingValues = this.$store.state.peculiarities[this.question]
    if (typeof existingValues === 'undefined') {
      this.selected = [...this.values]
    } else {
      this.selected = this.$store.state.peculiarities[this.question]
    }
  },
  watch: {
    selected: function(newSelection, oldSelection) {
      this.$store.commit('savePeculiarities',{
        questionId: this.question,
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
div.peculiarities {
  margin-left: 2em;

  .v-select {
    margin-top: 0.5em;
  }
}
</style>
<template lang="pug">
  div.tags-select
    span.tags-header {{ __i("tags-header") }}: {{ __i("tags-"+answer) }}
    span.tags-description {{ __i("tags-description") }}
    v-select(id="tags-select",v-model="selected",:dir="$store.state.inRTLMode ? 'rtl' : 'ltr'", multiple="multiple",:options="translatedOptions", :reduce="(option) => option.id")
    blockquote.additional-info(v-if="__i('tags-'+answer+'-additional-info') != 'tags-'+answer+'-additional-info'")
      span(v-html="__i('tags-'+answer+'-additional-info')")
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
    },
    translations: {
      type: Object,
      default: {}
    }
  },
  computed: {
    translatedOptions: function() {
      var translated = []
      var i = this.__i
      this.values.forEach((value) => {
        translated.push(
          {
            label: typeof this.translations[value][this.$store.state.language] !== undefined ?  this.translations[value][this.$store.state.language] : value,
            id: value
          }
        )
      })
      return translated
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
div.tags-select {
  margin-left: 2em;
  min-width: 50%;
  padding: 1em;

  .tags-header {
    color: #000;
    font-family: "Roboto Slab";
    border-bottom: 1px solid #ccc;
    padding-bottom: 5px;
    margin-bottom: 1em;
    display: block;
  }

  .tags-header::after {
    content: "";
    display: block;
    border-bottom: 0.15em solid #e1760d;
    width: 5%;
    position: relative;
    bottom: -6px; /* your padding + border-width */
  }

  .v-select {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
  }
  .header {
    margin-bottom: 0.5em;
    display: block;
    font-family: "Roboto Slab";
    color: black;
  }

  blockquote.additional-info  {
    border-left: 0.25em solid #e1760d;
    padding: 0.5em;
  }
}

#tags-select div div {

  .vs__selected{
      border-radius: 0px !important;
      background-color: #05396b;
      color: white;
  }
}
.vs__dropdown-toggle{
  border-radius: 0px !important;
}
.vs__deselect {
  svg {
    margin-left: 0.5em;
    path {
      fill: white !important;
    }
  }
}
</style>
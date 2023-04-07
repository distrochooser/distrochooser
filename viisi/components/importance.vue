<template lang="pug">
span.importance
    i.w-icon-down-circle-o(v-on:click="makeLessImportant", v-bind:class="{'w-icon-down-circle active': lessImportant }", :title='__i("make-less-important")')
    i.w-icon-star-on(v-on:click="makeImportant", v-bind:class="{'active': important }", :title='__i("make-important")')
</template>
<script>
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  methods: {
    makeImportant: async function() {
        var old = this.important
        var oldLessImportant = this.lessImportant
        this.resetImportanceState()
        if (!old || oldLessImportant) {
            this.$store.commit('makeImportant', this.answer)
        }
    },
    makeLessImportant: async function() {
        var old = this.lessImportant
        var oldImportant = this.important
        this.resetImportanceState()
        if (!old || oldImportant) {
            this.$store.commit('makeLessImportant', this.answer)
        }
    },
    resetImportanceState: async function() {
        this.$store.commit('resetImportanceState', this.answer)
    }
  },
  props: {
    answer: {
        type: Object,
        default: null
    },
    important: {
      type: Boolean,
      default: false,
    },
    lessImportant: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
@import '~/node_modules/animate.css/animate.min.css';

.importance {
    display: inline-block;
    margin-left: 0.5em;
    vertical-align: middle;
}

.w-icon-star-on {
    color: $lightAccent;
}

.w-icon-down-circle {
    color: notImportantSelectedColor;
}

.w-icon-star-on.active {
  color: $importanceSelectedColor;
}

.w-icon-star-off.active {
    color: $importanceSelectedColor;
    font-weight: bold;

}
.w-icon-stop.active {
    color: $markImportantUnselectedColor;
}
</style>
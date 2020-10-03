<template lang="pug">
  div
    div.feedbackmode(v-for="(matrix, key) in matrixes", :key="key")
      h2.feedback-header {{ __i(matrix.description) }} 
      i.w-icon-close(v-if="matrix.IsBlockingHit", title="Counts as a 'no-go'")
      i.w-icon-down(v-if="matrix.IsNegativeHit", title="Counts as a negative point")
      i.w-icon-pause(v-if="matrix.IsNeutralHit", title="unweighted match")
      i.w-icon-up(v-if="!matrix.IsNegativeHit && !matrix.IsBlockingHit && !matrix.IsNeutralHit", title="positive match")
      hr
      div.feedback-box-distro(v-for="(distro_enabled, distro) in matrix.distros", :key="distro")
        input(type="checkbox", :checked="distro_enabled", @change="onChange($event, matrix.description, distro, distro_enabled)")
        span {{ distro }}
      input(type="submit", value="send", @click="submit")
</template>
<script>
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  props: {
    matrixes: {
      type: Array,
      default: function() {
        return []
      }
    }
  },
  data: function() {
    return {
      changedMatrix: {}
    }
  },
  methods: {
    onChange(event, description, distro, initial_enabled) {
      var new_state = event.target.checked

      if (this.changedMatrix[description] === undefined) {
        this.changedMatrix[description] = {}
      }
      if (initial_enabled === new_state) {
        delete this.changedMatrix[description][distro]
        var length = Object.keys(this.changedMatrix[description]).length
        if (length === 0) {
          delete this.changedMatrix[description]
        }
      } else {
        this.changedMatrix[description][distro] = new_state
      }
    },
    async submit() {
      // session!
      await this.$store.dispatch('submitFeedback', {
        data: {
          category: this.$store.state.currentCategory,
          matrixes: this.changedMatrix,
          session: this.$store.state.token
        }
      })
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
.feedbackmode {
  margin-bottom: 1em;
}
.feedback-box-distro {
  display: inline-block;
  padding-right: 1em;
  padding-bottom: 1em;
  width: 250px;
}
.feedback-box-distro span {
  margin-left: 0.5em;
}
.feedback-header {
  display: inline;
}
.feedbackmode-comment {
  width: 100%;
  margin-top: 1em;
}
.w-icon-close {
  color: darkred;
  font-weight: bold;
}
.w-icon-down {
  color: red;
  font-weight: bold;
}
.w-icon-up {
  color: green;
  font-weight: bold;
}
.w-icon-pause {
  color: blue;
  font-weight: bold;
}
</style>

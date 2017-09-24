<template lang="html">
  <div>
        <p v-if="selectedRating == 0">
            {{ this.nuxt.globals.distrochooser.text('sys.rate') }}
        </p>
        <p class="star-parent" v-if="selectedRating == 0">
            <span class="star" v-for="(icon, key) in icons">
                <a class="face" :class="{'active': selectedRating == key }"  v-on:click.prevent="setRating(key)">
                    {{ icon }}
                </a>
            </span>
        </p>
        <p v-if="selectedRating != 0">
            {{ this.nuxt.globals.distrochooser.text('sys.rated') }}
        </p>
  </div>
</template>

<script>
import nuxt from '../nuxt.config'
export default {
  props: ['parent'],
  data: function () {
    return {
      selectedRating: 0,
      icons: {
        1: '😞',
        2: '😐',
        3: '😄'
      }
    }
  },
  computed: {
    nuxt: function () {
      return nuxt
    }
  },
  methods: {
    setRating: function (rating) {
      this.selectedRating = parseInt(rating)
      var test = this.nuxt.globals.test
      this.nuxt.globals.distrochooser.setRating(this.selectedRating, test)
    }
  }
}
</script>

<style scoped>
    .star{
        margin-right: 1em;
    }
    .face{
        font-size: xx-large;
        text-decoration: none;
        color: rgba(69, 77, 93, 0.5);
        cursor: pointer;
    }
    .active{
        color: #5764c6;
    }
</style>

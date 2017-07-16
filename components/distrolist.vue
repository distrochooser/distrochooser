<template>
<div class="timeline">
  <div class="timeline-item" v-for="(d,key) in distros" v-bind:key="key" v-if="d.points > 0 || globals.distrochooser.options.displayExcluded">
    <div class="timeline-left">
      <a class="timeline-icon icon-lg tooltip" :data-tooltip="distros.indexOf(d) + 1">
        <i class="icon" :class="{'icon-check':d.points > 0, 'icon-cross': d.points <= 0}"></i>
      </a>
    </div>
    <div class="timeline-content">
      <div class="tile-content">
        <div class="logo-parent">
          <img :src="'https://distrochooser.de' + d.image.replace('./','/')">
        </div>
        <p class="tile-subtitle">{{ d.name }} </p>
        <p class="tile-title" v-html="d.description"></p>
          <div class="timeline tags">
            <div class="timeline-item" v-for="(value,key) in d.results">
              <div class="timeline-left">
                <i class="icon" :class="{'icon-check icon-hit':!value.negative,' icon-cross icon-nohit':value.negative}"></i> {{ text(key) }}
                <span class="important" v-if="parseInt(value.weight) > 1 ">{{ text("important") }}</span>
                <span class="important" v-if="parseInt(value.weight) < 0 ">{{ text("notimportant") }}</span>
              </div>
              <div class="timeline-content">
                <!-- tiles structure -->
              </div>
            </div>
          </div>
        </div>
      <div class="tile-action">
        <a class="btn" :href="d.homepage" target="_blank">Website</a>
      </div>
    </div>
  </div>
</div>
</template>
<script>
import nuxt from '../mixins/nuxt-wrapper'
import i18n from '../mixins/i18n'
export default {
  props: [
    'distros'
  ],
  mixins: [
    nuxt,
    i18n
  ]
}
</script>
<style scoped>
.logo-parent{
    z-index: -10000;
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0.5;
}
.logo-parent img{
    max-width: 30%;
    max-height: 30%;
    position: absolute;
    right: 0px;
    bottom: 0px;
}
.icon-hit{
  color: #32b643;
}
.icon-nohit{
  color: #ff1515;
}
.important{
  font-weight: bold;
}
.tags{
  margin-bottom: 3em;
}
</style>


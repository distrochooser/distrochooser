<template>
<div class="timeline">
  <div class="empty" v-if="isDistroListEmpty">
    <div class="empty-icon">
      <i class="icon icon-cross"></i>
    </div>
    <h4 class="empty-title">{{ text("nodistros") }}</h4>
    <p class="empty-subtitle">{{ text("nodistrostext") }}</p>
  </div>
  <div class="share-mobile show-xs" v-if="!isDistroListEmpty && this.parent.displayTest != -1">
    <a class="btn centered" :href="shareLink">{{ text('share') }}: {{ shareLink }}</a>
  </div>
  <div class="share columns hide-xs" v-if="!isDistroListEmpty">
    <div class="column col-4"></div>
    <div class="column col-6">
      <div class="loading" v-if="this.parent.displayTest == -1"></div>
      <div class="tile" v-if="this.parent.displayTest != -1">
        <div class="tile-icon">
          <figure class="avatar avatar-lg">
            <img src="/logo.png">
          </figure>
        </div>
        <div class="tile-content" >
          <p class="tile-title">{{ text('share') }}</p>
          <p class="tile-subtitle">
            <a :href="shareLink">{{ shareLink }}</a>
          </p>
          <p>
            <a class="btn btn-sm twitter" :href="'https://twitter.com/share?url='+shareLink+'&hashtags=distrochooser,linux&via=distrochooser'">Twitter</a>
            <a class="btn btn-sm facebook" :href="'https://www.facebook.com/sharer/sharer.php?u='+shareLink">Facebook</a>
            <a class="btn btn-sm google-plus" :href="'https://plus.google.com/share?url='+shareLink">G+</a>
          </p>
        </div>
      </div>
    </div>
  </div>
  <div class="timeline-item" v-for="(d,key) in distros" v-bind:key="key" v-if="d.points > 0 || globals.distrochooser.options.displayExcluded">
    <div class="timeline-left">
      <a class="timeline-icon icon-lg tooltip" :data-tooltip="distros.indexOf(d) + 1">
        <i class="icon" :class="{'icon-check':d.points > 0, 'icon-cross': d.points <= 0}"></i>
      </a>
    </div>
    <div class="timeline-content">
      <div class="tile-content">
        <div class="logo-parent hide-xs">
          <img :src="'https://distrochooser.de' + d.image.replace('./','/')">
        </div>
        <p class="tile-subtitle">{{ d.name }} </p>
        <p class="tile-title" v-html="d.description"></p>
          <div class="timeline tags">
            <div class="toast" v-if="Object.keys(d.results).length ===0">
              {{ text("sys.notags") }}
            </div>
            <div class="timeline-item" v-bind:key="key" v-for="(value,key) in d.results">
              <div class="timeline-left">
                <i class="icon" :class="{'icon-check icon-hit':!value.negative,' icon-cross icon-nohit':value.negative}"></i> 
              </div>
              <div class="timeline-content">
                {{ text(key) }}
                <span class="important" v-if="parseInt(value.weight) > 1 ">{{ text("important") }}</span>
                <span class="notimportant" v-if="parseInt(value.weight) < 0 ">{{ text("notimportant") }}</span>
              </div>
            </div>
          </div>
        </div>
      <div class="tile-action">
        <a class="btn" :href="d.website" target="_blank">Website</a>
        <a class="source" :href="d.textSource" target="_blank">{{ text("sys.textsource") }}</a>
        <a class="source" :href="d.imageSource" target="_blank">{{ text("sys.imagesource") }}</a>
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
    'distros',
    'parent'
  ],
  mixins: [
    nuxt,
    i18n
  ],
  computed: {
    shareLink: function () {
      return 'https://distrochooser.de/' + this.globals.lang + '/' + this.parent.displayTest
    },
    isDistroListEmpty: function () {
      if (!this.globals.distrochooser.options.displayExcluded) {
        var nonEmpty = 0
        for (var i in this.distros) {
          if (this.distros[i].points > 0) {
            nonEmpty++
          }
        }
        return nonEmpty === 0
      }
      return false
    }
  }
}
</script>
<style scoped>
.logo-parent{
    z-index: -10000;
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0.7;
}
.logo-parent img{
    max-width: 8em;
    max-height: 4em;
    position: absolute;
    right: 2em;
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
.notimportant{
  font-weight: 300;
  font-style: italic;
} 
.tags{
  margin-bottom: 3em;
}
.share-mobile{
  margin-bottom: 1em;
}
.twitter{
  background-color: #00aced;
  color: white;
  border: 1px solid #00aced;
  margin-right: 0.2em;
}
.facebook{
  background-color: 	#3b5998;
  border: 1px solid 	#3b5998;
  color: white;
  margin-right: 0.2em;
}
.google-plus{
  background-color: #ea4335;
  border: 1px solid #ea4335;
  color: white;
  margin-right: 0.2em;
}
.source{
  margin-left: 0.4em;
}
.tag-description{
  margin-left:0.2em;
}
.avatar{
  background: white !important;
}
</style>


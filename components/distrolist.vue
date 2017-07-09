<template>
<div class="timeline">
  <div class="timeline-item" id="timeline-example-2" v-for="(d,key) in distros" v-bind:key="key">
    <div class="timeline-left">
      <a class="badge" href="#timeline-example-1" data-badge="8%"></a>
    </div>
    <div class="timeline-content">
      <div class="tile-content">
        <div class="logo-parent">
          <img :src="'https://distrochooser.de' + d.image.replace('./','/')">
        </div>
        <p class="tile-subtitle">{{ d.name }} </p>
        <p class="tile-title" v-html="d.description"></p>
        </div>
      <div class="tile-action">
        <a class="btn" :href="d.homepage" target="_blank">Website</a>
      </div>
    </div>
  </div>
  ...
</div>
</template>
<script>
export default {
  props: [
    'distros'
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
</style>


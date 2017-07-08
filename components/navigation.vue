<template>
	<div class="column col-3">
		<a href="about" class="btn btn-primary button-left-nav contact" data-toggle="modal" data-target="#about">{{ text("about") }}</a>
		<span class="spacer"></span>
		<a class="btn btn-primary button-left-nav contact" href="./static/privacy.html"> {{ text("privacy") }}</a>
		<span class="spacer"></span>
		<a class="btn btn-primary button-left-nav contact" href="./static/contact.html"> {{ text("contact") }} </a>
		<span class="spacer"></span>
		<a class="btn btn-primary button-left-nav" target="_blank" href="http://0fury.de">
			<img class="vendor" alt="0fury.de" src="https://distrochooser.de/assets/0fury.ico">
			<span>{{ text("Vendor") }}</span> 0fury.de</a>
		<span class="spacer"></span>
		<a class="flag" title="Zur deutschen Version wechseln" href="?l=1">
			<img src="https://distrochooser.de/assets/langs/de.png" alt="Deutsch">
		</a>
		<a class="flag" title="Switch to english version" href="?l=2">
			<img src="https://distrochooser.de/assets/langs/gb.png" alt="English">
		</a>
	</div>
</template>
 
<script>
import i18n from '../mixins/i18n'
import nuxt from '../mixins/nuxt-wrapper'
export default {
  mixins: [i18n, nuxt],
  created: function () {
    console.log(this)
  }
}
</script>
 
<style scoped>
.button-left-nav {
    color: #fff;
    display: block;
    width: 70%;    
		padding: 9px 12px 7px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 0.5em;
}
.vendor{
    float: left;
}
.flag{
    margin-right: 0.5em;
}
</style>

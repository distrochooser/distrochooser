<template>
	<div class="column col-3">
		<div class="column col-11">
			<ul class="menu">
				<!-- menu header text -->
				<li class="divider" :data-content="text('links')">
				</li>
				<li class="menu-item">
					<a href="about">
						<i class="icon icon-link"></i> {{ text("about") }}
					</a>
				</li>
				<li class="menu-item">
					<a href="privacy">
						<i class="icon icon-link"></i> {{ text("privacy") }}
					</a>
				</li>
				<li class="menu-item">
					<a href="contact">
						<i class="icon icon-link"></i> {{ text("contact") }}
					</a>
				</li>
				<li class="menu-item">
					<a target="_blank" href="http://0fury.de">
					<img class="vendor" alt="0fury.de" src="https://distrochooser.de/assets/0fury.ico">
					{{ text("Vendor") }} <span class="0fury">0fury.de</span>
					</a>
				</li>
				<!-- menu divider -->
				<li class="divider" :data-content="text('lang')">
				</li>
				<!-- menu item with badge -->
				<li class="menu-item">
					<div class="menu-badge">
						<a class="flag" title="Zur deutschen Version wechseln" href="?l=1">
							<img src="https://distrochooser.de/assets/langs/de.png" alt="Deutsch">
						</a>
						<a class="flag" title="Switch to english version" href="?l=2">
							<img src="https://distrochooser.de/assets/langs/gb.png" alt="English">
						</a>
					</div>
					<a href="#">
						<i class="icon icon-link"></i> 
					</a>
				</li>
			</ul>
		</div>
		<div class="col-1">
		</div>
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
    margin-right: 0.2em;
    margin-left: -0.1em;
}
.flag{
    margin-right: 0.5em;
}
</style>

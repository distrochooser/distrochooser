<template>
	<div>
		<div class="col-lg-3">
			<div class="row">
				<div class="visible-lg">
					<a href="about" class="btn btn-primary button-left-nav contact" data-toggle="modal" data-target="#about">Über den Distrochooser</a>
					<span class="spacer"></span>
					<a class="btn btn-primary button-left-nav contact" href="./static/privacy.html">Datenschutz</a>
					<span class="spacer"></span>
					<a class="btn btn-primary button-left-nav contact" href="./static/contact.html">Kontakt</a>
					<span class="spacer"></span>
					<a class="btn btn-primary button-left-nav" target="_blank" href="http://0fury.de">
						<img class="vendor" alt="0fury.de" src="https://distrochooser.de/assets/0fury.ico">
						<span>Ein Projekt von</span> 0fury.de</a>
					<span class="spacer"></span>
					<a title="Zur deutschen Version wechseln" href="?l=1">
						<img class="flag" src="https://distrochooser.de/assets/langs/de.png" alt="Deutsch">
					</a>
					<a title="Switch to english version" href="?l=2">
						<img class="flag" src="https://distrochooser.de/assets/langs/gb.png" alt="English">
					</a>
				</div>
				<div class="hidden-lg">
					<nav class="navbar navbar-default">
						<div class="container-fluid">
							<div class="navbar-header">
								<a class="navbar-brand brand" href="index.html">
									Distrochooser
								</a>
								<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#example-navbar-collapse">
									<span class="sr-only">Toggle navigation</span>
									<span class="icon-bar"></span>
									<span class="icon-bar"></span>
									<span class="icon-bar"></span>
								</button>
							</div>
							<div class="collapse navbar-collapse" id="example-navbar-collapse">
								<ul class="nav navbar-nav">
									<li role="presentation">
										<a class="flags" title="Zur deutschen Version wechseln" href="?l=1">
											<img class="flag" src="https://distrochooser.de/assets/langs/de.png" alt="Deutsch">
										</a>
	
										<a class="flags" title="Switch to english version" href="?l=2">
											<img class="flag" src="https://distrochooser.de/assets/langs/gb.png" alt="English">
										</a>
									</li>
									<li role="presentation">
									</li>
									<li role="presentation">
										<a class="sprivacy" id="privacy" href="./static/privacy.php">Datenschutz</a>
									</li>
									<li role="presentation">
										<a class="scontact" id="contact" href="./static/contact.php">Kontakt</a>
									</li>
								</ul>
							</div>
						</div>
					</nav>
				</div>
			</div>
		</div>
	</div>
</template>
 
<script>
export default {
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
</style>

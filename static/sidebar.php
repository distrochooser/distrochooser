<div class="col-lg-3">
	<div class="row">
		<!--<a class ="hidden-xs" id ="homelink" href="index.php"><img src="./assets/ldc2.png"></img></a>-->					
			<div class="hidden-xs hidden-sm">			
			<a class="btn btn-primary buttonBright ldcui share" id="shareMenuEntry"><?php echo (isset($ldc)) ? GetSystemVar($ldc,"share") : "" ; ?></a>					
			<span class="spacer"></span>
			<a class="btn btn-primary buttonBright ldcui privacy" id="privacyMenuEntry" href="./static/privacy.php"><?php echo (isset($ldc)) ? GetSystemVar($ldc,"privacy") : "" ; ?></a>					  
			<span class="spacer"></span>
			<a class="btn btn-primary buttonBright ldcui contact" id="contactMenuEntry" href="./static/contact.php"><?php echo (isset($ldc)) ? GetSystemVar($ldc,"contact") : "" ; ?></a>					  
			<span class="spacer"></span>				
  <a class="btn btn-primary buttonBright ldcui contact" id="about"><?php echo (isset($ldc)) ? GetSystemVar($ldc,"about") : "" ; ?></a>     
			<span class="spacer"></span>	

			<a class="btn btn-primary buttonBright" target="_blank" href="http://0fury.de"><img class="vendor" alt="0fury.de" src="./assets/0fury.ico"><span class="ldcui" id="Vendor"><?php echo (isset($ldc)) ? GetSystemVar($ldc,"Vendor") : "" ; ?></span>  0fury.de</a>				  
			<?php if (strpos($_SERVER["REQUEST_URI"], "detail.php") === false)	: ?>	
			<a title="Zur deutschen Version wechseln" href="?l=1"><img src="./assets/langs/de.png" alt="Deutsch"></img></a>
			<a title="Switch to english version" href="?l=2"><img src="./assets/langs/gb.png" alt="English"></img></a>
			<?php endif;?>
			</div>
			<div class="visible-xs visible-sm">					
				<ul class="nav nav-pills" role="tablist">
				  <li role="presentation"> <a class="ldcui sshare" href="#" id="share"></a></li>
				  <li role="presentation"> <a class="ldcui sprivacy" id="privacy" href="./static/privacy.php"></a></li>
				  <li role="presentation"> <a class="ldcui scontact" id="contact" href="./static/contact.php"></a></li>
				</ul>
			</div>
	</div>
</div>
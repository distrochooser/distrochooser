<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<!--<link rel="stylesheet" href="./Lib/bootstrap/css/bootstrap.min.css">-->
<link rel="stylesheet" href="./Lib/bootstrap/css/lumen.css">
<link  href="./Lib/font-awesome/css/font-awesome.css" rel="stylesheet">
<link rel="stylesheet" href="./css/ldc.css">
<script src="./Lib/jquery.min.js"></script>
<script src="./Lib/bootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript" src="./js/ldc.js"></script>
<script type="text/javascript" src="./js/ldc-ui.js"></script>
<title>Linux Distribution Chooser</title>
</head>
<body>
<div class="container">
	<div class="row">
		<div class="col-lg-3">
			<div class="row">
				<!--<a class ="hidden-xs" id ="homelink" href="index.php"><img src="./assets/ldc2.png"></img></a>-->					
					<div class="hidden-xs hidden-sm">
					<button class="btn btn-primary buttonBright" type="button">
					  <a class="ldcui" class="share" id="share"></a>	
					</button>
					<span class="spacer"></span>
					<button class="btn btn-primary buttonBright" type="button">
					  <a class="ldcui "  class="privacy" id="privacy" href="./static/privacy.php"></a>					  
					</button>
					<span class="spacer"></span>
					<button class="btn btn-primary buttonBright" type="button">
					  <a class="ldcui " class="contact"  id="contact" href="./static/contact.php"></a>					  
					</button>
					<span class="spacer"></span>
					<button class="btn btn-primary buttonBright" type="button">
					  <a class="ldcui " class="contact"  id="about"></a>					  
					</button>
					<span class="spacer"></span>
					<button class="btn btn-primary buttonBright" type="button">					
						<a target="_blank" href="http://0fury.de"> <img class="vendor" src="./assets/0fury.ico"><span class="ldcui" id="Vendor"></span>  0fury.de</a>				  
					</button>

					</div>
					<div class="visible-xs visible-sm">					
						<ul class="nav nav-pills" role="tablist">
						  <li role="presentation"> <a class="ldcui" href="#" class="sshare" id="share"></a>	</li>
						  <li role="presentation"> <a class="ldcui" class="sprivacy" id="privacy" href="./static/privacy.php"></a>	</li>
						  <li role="presentation"> <a class="ldcui" class="scontact" id="contact" href="./static/contact.php"></a></li>
						</ul>
					</div>
			</div>
		</div>
		<div class="col-lg-6 main">   
			<div class="row">
        <noscript>
          <div class="alert alert-danger">
            Die Linux-Auswahlhilfe benötigt JavaScript für essentielle Funktionen. 
            JavaScript ist nicht böse. Ich nutze JavaScript für eine bessere Benutzbarkeit des Dienstes.
            Du kannst dir auf <a href="https://github.com/squarerootfury/distrochooser/tree/ldc2/">Github</a> gerne ansehen, was der Distrochooser im Hintergrund macht und das es sich um ein vertrauenswürdiges Projekt handelt.
            <hr>
            The Linux-Distrochooser requires JavaScript to improve the user expierience. 
            JavaScript ist not evil. You can look on <a href="https://github.com/squarerootfury/distrochooser/tree/ldc2/">Github</a> what the Distrochooser does with JavaScript.
          </div>
        </noscript>
				<div class="panel-group" id="accordion">
					<div class="panel panel-default">
						<div class="panel-heading" data-toggle="collapse" data-parent="#accordion" href="#collapseOne">
							<h4 class="panel-title">
								<a id="welcomeTextHeader"  class="collapsed ldcui"></a>
							</h4>
						</div>
						<div id="collapseOne" class="panel-collapse collapse">
							<div class="panel-body ldcui" id="welcomeText">
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="col-md-1">
		</div>
		<div class="col-lg-2">
			<div class="row">				
				<ul class="list-group"  id='rightBar'>
				  <li class="list-group-item"><a class="hidden-xs" id="homelink" href="index.php" style="display: inline;"><img src="./assets/ldc2alpha.png" style="
					    width: 100%;
					"></a></li>
				  <li class="list-group-item">
				    <span class="badge"><span id="answeredCount" class="ldcui">X</span>/ <span class="ldcui" id="answerCount">Y</span></span>
				    <span class="ldcui" id="answered">Beantwortet</span>
				  </li>
				  <li class="list-group-item">
				    <span class="badge"><span id="hitCount" class="ldcui">X</span>/ <span class="ldcui" id="allCount">Y</span></span>
				    <span class="ldcui" id="Suitable"></span>
				  </li>
				   <li class="list-group-item">
				   	<a class="btn btn-primary ldcui" id="getresult">Auswerten</a>
				   </li>           
				</ul>
			</div>
		</div>
	</div>
</div>
<script type="text/javascript">
	var htmlInject = "<div class='panel panel-default'>" + 
	"<div class='panel-heading' role='tab' id='Heading{{ID}}' data-toggle='collapse' data-parent='#accordion' href='#collapse{{ID}}' aria-expanded='false' aria-controls='collapse{{ID}}'>" + 
	"  <h4 class='panel-title'>" + 
	   " <a class='collapsed' >" + 
	     " {{TITLE}}" + 
	    "</a>" + 
	 " </h4>" + 
	"</div>" + 
	"<div id ='collapse{{ID}}' class='panel-collapse collapse' role='tabpanel' aria-labelledby='Heading{{ID}}'>" + 
	  "<div id = 'Question_{{ID}}' class='panel-body'>" + 
	   "<p>{{QUESTION}}</p>" +
	  "{{CONTENT}}" + 
	  "</div>" + 
	"</div>" + 
"</div>";
</script>
<!-- Dialogs -->
<div class="modal fade" id="modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title ldcui" id="Result"></h4>
      </div>
      <div class="modal-body">
        <p id="ResultContent">        	
        </p>
        <h4 class="ldcui" id="MatrixHeader"></h4>
        <table style="table-layout:fixed;" id="matrix" class="table table-hover table-condensed">
        </table>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div>
  </div>
</div>
<!-- imprint-->
<div class="modal fade" id="modalImprint">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
        <p id="imprint" class="ldcui">
        	
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="modalPrivacy">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
        <p id="privacyText" class="ldcui">
        	
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="modalAbout">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
        <h3 id="Title" class="ldcui"></h3>
        <p id="aboutText" class="ldcui"></p>
        <h3 id="installedDistros" class="ldcui"></h3>
        <ul id="distros">
        </ul>
        <h3 id="stats" class="ldcui"></h3>
        <span id="testCount" class="ldcui"></span><span  id="tc" class="badge"></span>
         <h4 id="rankedDistros" class="ldcui"></h4>
        <ul id="ranks">
        </ul>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div>
  </div>
</div>
<div id ="shareDialog" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title ldcui" id="shareTitle">Modal title</h4>
      </div>
      <div class="modal-body" id="shareDialogContent">  
      <div class="socialicons">     
        <a href="https://twitter.com/home?status=http://distrochooser.0fury.de?r=tw" target="_blank">
          <i class="fa fa-twitter fa-2x twitter"></i>
        </a>
        <a href="https://plus.google.com/share?url=http://distrochooser.0fury.de?r=gp" target="_blank">
          <i class="fa fa-google-plus  fa-2x gplus"></i>
        </a>
        <a href="https://www.facebook.com/sharer/sharer.php?u=http://distrochooser.0fury.de&r=fb" target="_blank">
          <i class="fa fa-facebook fa-2x facebook"></i>
        </a>
        <a href="mailto:?subject=Distro%20Chooser">
          <i class="fa fa-envelope fa-2x email"></i>
        </a>
        <a href="https://github.com/squarerootfury/distrochooser" target="_blank">
          <i class="fa fa-github fa-2x github"></i>
        </a>
       </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
</body>
</html>
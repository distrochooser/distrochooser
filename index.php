<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="./Lib/bootstrap/css/bootstrap.min.css">
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
				<a href="index.php"><img src="./assets/ldc2.png"></img></a>				
			</div>
		</div>
		<div class="col-lg-6">
			<div class="row">
				<div class="panel-group" id="accordion">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h4 class="panel-title">
								<a id="welcomeTextHeader" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" class="collapsed ldcui">Collapsible Group Item #1</a>
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
	"<div class='panel-heading' role='tab' id='Heading{{ID}}'>" + 
	"  <h4 class='panel-title'>" + 
	   " <a class='collapsed' data-toggle='collapse' data-parent='#accordion' href='#collapse{{ID}}' aria-expanded='false' aria-controls='collapse{{ID}}'>" + 
	     " {{TITLE}}" + 
	    "</a>" + 
	 " </h4>" + 
	"</div>" + 
	"<div id ='collapse{{ID}}' class='panel-collapse collapse' role='tabpanel' aria-labelledby='Heading{{ID}}'>" + 
	  "<div id = 'Question_{{ID}}' class='panel-body'>" + 
	   "<h3>{{QUESTION}}</h3>" +
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
<footer class="footer hidden-xs">
	<img class="vendor" src="./assets/0fury.ico"><span class="ldcui" id="Vendor"></span> <a target="_blank" href="http://0fury.de">0fury.de</a>
	<a class="ldcui" id="contact" href="./content/contact.inc.php"></a>
	<a class="ldcui" id="privacy" href="./content/privacy.inc.php">Datenschutz</a>		
	<a class="ldcui" id="share"></a>
	<a class="ldcui"  id="faq" href="./content/faq.inc.php">Häufig gestellte Fragen</a>	
</footer>
</body>
</html>
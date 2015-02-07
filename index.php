<html>
<head>
<link rel="stylesheet" href="./Lib/bootstrap/css/bootstrap.min.css">
<link rel="stylesheet" href="./css/ldc.css">

<script src="./Lib/jquery.min.js"></script>
<script src="https://www.promisejs.org/polyfills/promise-done-6.1.0.min.js"></script>
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
				<img src="./assets/ldc2.png"></img>
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
	   "<h1>{{QUESTION}}</h1>" +
	  "{{CONTENT}}" + 
	  "</div>" + 
	"</div>" + 
"</div>";
</script>
</body>
</html>
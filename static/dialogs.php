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
<div class="modal" id="modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title ldcui" id="Result">#</h4>
      </div>
      <div class="modal-body">
        <p id="ResultContent">          
        </p>
        <h4 class="ldcui" id="MatrixHeader">#</h4>
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
<div class="modal" id="modalImprint">
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
<!-- Privacy -->
<div class="modal" id="modalPrivacy">
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
<!-- about -->
<div class="modal" id="modalAbout">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
        <h3 id="Title" class="ldcui">#</h3>
        <p id="aboutText" class="ldcui"></p>
        <h3 id="installedDistros" class="ldcui">#</h3>
        <ul id="distros">
        </ul>
        <h3 id="stats" class="ldcui">#</h3>
        <h4 id="testCountCanvasTitle" class="ldcui">#</h4>
        <!-- chart -->
        <canvas id="testCountCanvas" width="598" height="400"></canvas>
        <br>
        <script type="text/javascript">
        	$(document).ready(function(){        		
        		$('#modalAbout').on('shown.bs.modal', function () {
				  	$("canvas").each(function(){
	        			$(this).attr("width","500");
	        			$(this).attr("height","240");  
	        			$(this).removeAttr("style");
	        		});
	        		var label = [];
	        		var labelData = [];
	        		$.post( "./rest.php", { method: "GetMonthStats", args: "",lang: 1 })
					.done(function( data ) {					
						var stats = $.parseJSON(data);		
						for (var i = stats.length - 1; i >= 0; i--) {
							label.push(stats[i].MONTH + "/" +new Date().getFullYear());
							labelData.push(parseInt(stats[i].count));
						};
						var chartData = {
						labels : label,
						datasets : [
							{
								
								fillColor : "#158cba",
								strokeColor : "#127ba3",
								pointColor : "#fff",
								pointStrokeColor : "#9DB86D",
								data : labelData,
							}
						]
					};
					 var buyers = document.getElementById('testCountCanvas').getContext('2d');
	    			new Chart(buyers).Line(chartData);
					});	
	        		
				}); 			
        	});        	
        </script>         
       <h4 class="ldcui" id="distroResultStats">#</h4>
        <canvas id="distroCountCanvas" width="598" height="400"></canvas>       
         <script type="text/javascript">
        	$(document).ready(function(){        		
        		$('#modalAbout').on('shown.bs.modal', function () {        		
	        		var labelData = [];
	        		$.post( "./rest.php", { method: "GetStats", args: "",lang: 1 })
					.done(function( data ) {					
						var stats = $.parseJSON(data);								
						for (var i = stats.length - 1; i >= 0; i--) {							
							labelData.push({ color:stats[i].ColorCode,value: parseInt(stats[i].count),label:stats[i].Name});
						};		
						console.log(labelData);				
						var buyers = document.getElementById('distroCountCanvas').getContext('2d');
		    			new Chart(buyers).Pie(labelData,{animationSteps:80});
					});	
	        		
				}); 			
        	});        	
        </script>
        <h4 id="uses" class="ldcui">Usage</h4>
      
        	<ul>
        	<li><a href="http://getbootstrap.com/">Bootstrap</a></li>
        	<li><a href="https://bootswatch.com/lumen/">Bootswatch Theme Lumen</a></li>
        	<li><a href="https://jquery.com/">jQuery</a></li>
        	<li><a href="http://www.chartjs.org/">Chart.js</a></li>
        	<li><a href="https://fortawesome.github.io/Font-Awesome/icons/">Font Awesome</a></li>
        	<li><a href="http://www.deviantart.com/art/Tondo-F-Icon-Set-OS-327759704">Tux Icon von P3T3B3</a></li>
        	<li><a href="http://phishy.de">Phis</a> (Design)</li>
          	<li><a href="http://www.famfamfam.com/lab/icons/flags/">famfamfam flag icons</a></li>
		<li>Lenny (Manjaro Screenshots)</li>
        	</ul>
        
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div>
  </div>
</div>
<!-- Share -->
<div id ="shareDialog" class="modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title ldcui" id="shareTitle">Modal title</h4>
      </div>
      <div class="modal-body" id="shareDialogContent">  
      <div class="socialicons">    
        <a id="twitterlink" href="https://twitter.com/share?text=Distrochooser+&amp;url=http://distrochooser.0fury.de/?r=tw&amp;hashtags=distrochooser,linux" target="_blank">
          <i class="fa fa-twitter fa-2x twitter"></i>
        </a>
        <a href="https://plus.google.com/share?url=http://distrochooser.0fury.de/?r=gp" target="_blank">
          <i class="fa fa-google-plus  fa-2x gplus"></i>
        </a>
        <a href="https://www.facebook.com/sharer/sharer.php?u=http://distrochooser.0fury.de/?r=fb" target="_blank">
          <i class="fa fa-facebook fa-2x facebook"></i>
        </a>
        <a href="mailto:?subject=Distro%20Chooser">
          <i class="fa fa-envelope fa-2x email"></i>
        </a>
        <a href="http://distrochooser.0fury.de/?r=l" target="_blank">
          <i class="fa fa-link fa-2x link"></i>
        </a>
        <a href="https://github.com/squarerootfury/distrochooser" target="_blank">
          <i class="fa fa-github fa-2x github"></i>
        </a>  
        <hr> 
        <div class="input-group">
          <span class="input-group-addon ldcui" id="shareMyResultText">Weitersagen per Link</span>
          <input type="text" class="form-control" id="shareMyResult">
        </div>  
        <script>
        	$("#shareMyResult").click(function(){
        		$(this).select();
        	});
        </script>      
       </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->

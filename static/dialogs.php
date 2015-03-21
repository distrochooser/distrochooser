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
<!-- Privacy -->
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
<!-- about -->
<div class="modal fade" id="modalAbout">
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
        <span id="testCount" class="ldcui"></span><span  id="tc" class="badge"></span>
         <h4 id="rankedDistros" class="ldcui">#</h4>
        <ul id="ranks">
        </ul>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div>
  </div>
</div>
<!-- Share -->
<div id ="shareDialog" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title ldcui" id="shareTitle">Modal title</h4>
      </div>
      <div class="modal-body" id="shareDialogContent">  
      <div class="socialicons">    
        <a id="twitterlink" href="https://twitter.com/share?text=Distrochooser: &url=http://distrochooser.0fury.de/?r=tw&hashtags=distrochooser,linux" target="_blank">
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
       </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span></button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
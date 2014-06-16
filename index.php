<?php
		//header("HTTP/1.0 403 Forbidden");
		//exit();
?>
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
	
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<link rel="shortcut icon" type="image/x-icon" href="img/0fury.ico">
        <title>Linux Distribution Chooser</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="css/css/font-awesome.min.css" rel="stylesheet">
        <link rel="stylesheet" href="css/superhero.min.css">
        <style>
            body {
                padding-top: 50px;
                padding-bottom: 20px;
            }
        </style>
       
        <link rel="stylesheet" href="css/main.css">

        <!--[if lt IE 9]>
            <script src="js/vendor/html5-3.6-respond-1.1.0.min.js"></script>
        <![endif]-->
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->
	<?php
		include "./content/contact.inc.php";
		include "./content/privacy.inc.php";
		include "./content/share.inc.php";
		include "./content/status.inc.php";
	?>
		
    <div class="navbar navbar-header navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
	
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <img class="logo" src="./img/tux.png"/>
          <a id ="SystemTitle" class="navbar-brand logotext" href="./"></a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
	<li class="visible-xs"><a href="#" class="contact"></a></li>
	<li class="visible-xs"><a href="#" class="privacy"></a></li>
        </ul>
        </div><!--/.navbar-collapse -->
      </div>
    </div>

    <!-- Main jumbotron for a primary marketing message or call to action -->
   
    
  <div id="parentContainer">
    <div class="container"  >
      <!-- Example row of columns -->
       <div id ="content"> 
	     
        <div class="jumbotron">
          <div class="container">
		
            <h1 id="StartWelcomeTitle"></h1>
            <p id ="StartText"></p>
            <p style="text-align:center"><a id = "startButton" class="btn btn-primary btn-lg" role="button"></a> </p>
          </div>
        </div>
      </div>


     
    </div> </div><!-- /container -->    
	
	 <footer class="footer hidden-xs" >
        <p class="hidden-xs links vendorSubTitle">Made by <img class="vendor" src= "./img/0fury.ico"/> <a target= "_blank"  href="http://0fury.de">0fury.de</a>
<a class ="contact" href="./content/contact.inc.php"></a>
<a class ="privacy" href="./content/privacy.inc.php"></a><a class ="status" href="#">Status</a>		
 <a class = "shareButton "></a>
	</p>
      </footer>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.11.0.min.js"><\/script>')</script>

        <script src="js/vendor/bootstrap.min.js"></script>

        <script src="js/main.js"></script>
       
    </body>
</html>

<?php
	error_reporting(E_ALL);
	require_once "./Includes/DB.class.php";
	require_once "./Includes/LDC.class.php";
	if (!isset($_GET["l"]))
		$lang = 1;
	else		
		$lang = $_GET["l"];

	$ldc = new \LDC($lang);
	$distros = json_decode($ldc->GetDistributions());	
	$distro = null;	
	foreach ($distros as $key => $value) {
		if ($value->Id == $_GET["id"]){
			$distro = $value;
			break;
		}
	}
	function GetSystemVar($ldc,$name){			
		$languageVars = json_decode($ldc->GetSystemVars());		
		foreach ($languageVars as $key => $value) {			

			if ($value->Val == $name)
				return $value->Text;
		}
		return "";
	}
?>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="UTF-8">
<meta name="description" lang = "de"  content ="Die Linux Auswahlhilfe hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden.">
<meta name="description" lang = "en"  content ="The Linux Distribution Chooser helps you to find the suitable Distribution for you!">
<meta name="keywords" content="Linux, Linux Chooser, Linux Distribution Chooser, Linux Auswahlhilfe, Linux Auswahl, Alternative to Windows, Linux Comparison, Linux Vergleich, Vergleich, Auswahlhilfe, Alternative zu Windows">
<meta name="generator" content="LDC 2015">
<link rel="stylesheet" href="./Lib/bootstrap/css/lumen.css">
<link  href="./Lib/font-awesome/css/font-awesome.css" rel="stylesheet">
<link rel="stylesheet" href="./css/ldc.css">
<link rel="icon" href="./assets/0fury.ico">
<script src="./Lib/jquery.min.js"></script>
<script src="./Lib/bootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript" src="./js/ldc.js"></script>
<script type="text/javascript" src="./js/ldc-ui.js"></script>
<title><?php echo $distro->Name;?> - <?php echo GetSystemVar($ldc,"Title");?></title>
</head>
<body>
<div class="container">
<div class="row">
<?php include "./static/sidebar.php";?>
<div class="col-lg-6 main">
<h1><?php echo $distro->Name;?></h1>
<div class="panel panel-default"> 
  <div class="panel-heading"><?php echo GetSystemVar($ldc,"Description");?></div> 
  <div class="panel-body">
  <img class="linuxlogo" src="<?php echo $distro->Image;?>">
    <?php echo $distro->Description;?>
  </div>
</div>
<div class="panel panel-default">  
  <div class="panel-heading"><?php echo GetSystemVar($ldc,"Screenshots");?></div>
  <div class="panel-body screenshotContainer">           
	    <?php 
	  		if (!empty($distro->Media)){
	  			foreach ($distro->Media as $key => $value) {		  				
	  				echo '<p><img class="screenshot" src="'.$value->MediaPath.'" alt="'.$value->Alt.'" title="'.$value->Alt.'"></img></p>';	
	  				echo "<p>".$value->Alt."</p>";
	  			}
	  		}
	  		else{
	  			echo "<div class='alert alert-info'>".GetSystemVar($ldc,"NoScreenshots")."</div>";
	  		}
	  	?>              	
  </div>
</div>
<div class="panel panel-default">  
  <div class="panel-heading">Links</div>
  <div class="panel-body">
    <a class="detail" href="<?php echo $distro->Homepage;?>">Homepage</a>
    <a class="detail" href="<?php echo $distro->ImageSource;?>"><?php echo GetSystemVar($ldc,"ImageSource");?></a>
    <a class="detail" href="<?php echo $distro->TextSource;?>"><?php echo GetSystemVar($ldc,"TextSource");?></a>
  </div>
</div>
</div>

<div class="col-md-1">
</div>
<div class="col-lg-2">
			<div class="row">				
				<ul class="list-group">
				  <li class="list-group-item"><a class="hidden-xs" href="index.php"><img src="./assets/ldc2alpha.png" alt="Linux Distribution Chooser" style="
					    width: 100%;
					"></a></li>				    
				</ul>
			</div>
		</div>
		</div>
</div>
<?php include "./static/dialogs.php";?>
</body>
</html>
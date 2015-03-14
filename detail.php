<?php
	error_reporting(E_ALL);
	require_once "./Includes/DB.class.php";
	require_once "./Includes/LDC.class.php";
	$lang = $_GET["lang"];
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
<title><?php echo $distro->Name;?> - <?php echo GetSystemVar($ldc,"Title");?></title>
<link rel="stylesheet" href="./Lib/bootstrap/css/lumen.css">
<link  href="./Lib/font-awesome/css/font-awesome.css" rel="stylesheet">
<link rel="stylesheet" href="./css/ldc.css">
<script src="./Lib/jquery.min.js"></script>
<script src="./Lib/bootstrap/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
<div class="row">
<h1><img class="detailLogo" alt="<?php echo $distro->Name;?>-Logo" src="<?php echo $distro->Image;?>"/></h1>
<div class="panel panel-default"> 
  <div class="panel-heading"><?php echo GetSystemVar($ldc,"Description");?></div> 
  <div class="panel-body">
  <?php echo $distro->Name;?>
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
</div>
</body>
</html>
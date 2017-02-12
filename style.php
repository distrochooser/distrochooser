<?php
   $dnt = isset($_SERVER['HTTP_DNT']) && $_SERVER['HTTP_DNT'] == 1;
   $nocdn = isset($_GET["nocdn"]);
   $local =  $dnt || $nocdn;
?>
<?php if ($what === "head" && $local) :?>
	<link rel="stylesheet" href="./3rdparty/bootstrap.min.css">
	<link rel="stylesheet" href="./3rdparty/gfonts.css">
	<link rel="stylesheet" href="./3rdparty/font-awesome.min.css" />
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="./3rdparty/jquery.rateyo.min.css">
<?php endif;?>

<?php if ($what === "foot" &&  $local) :?>
	<script src="./3rdparty/jquery-2.2.4.min.js"></script>
	<script src="./3rdparty/bootstrap.min.js"></script>
	<!-- Latest compiled and minified JavaScript -->
	<script src="./3rdparty/jquery.rateyo.min.js"></script>
	<script
	src="./3rdparty/vue.js"></script>
	<script src="./3rdparty/Chart.min.js"></script>
	<script src="./3rdparty/vue-resource.min.js"></script>
<?php endif;?>

<?php if ($what === "head" && !$local) :?>
    <!-- You don't have a DNT header present, so i will use CDN's -->    
	<link rel="stylesheet" href="https://bootswatch.com/lumen/bootstrap.min.css">
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.1.1/jquery.rateyo.min.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />
<?php endif;?>

<?php if ($what === "foot" && !$local) :?>
    <!-- You don't have a DNT header present, so i will use CDN's -->
	<script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<!-- Latest compiled and minified JavaScript -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.1.1/jquery.rateyo.min.js"></script>
	<script
	src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.25/vue.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.2.2/Chart.min.js"></script>
	<script src="https://cdn.jsdelivr.net/vue.resource/0.9.1/vue-resource.min.js"></script>
<?php endif;?>
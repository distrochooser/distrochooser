<?php
  include "./redirect.php";
?>
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="language" content="<?php echo (isset($_GET["l"]) && $_GET["l"] == 1 || !isset($_GET["l"])) ? "de":"en";?>">
  <meta charset="UTF-8">
  <meta name="description" lang = "de"  content ="Die Linux Auswahlhilfe hilft, im Dschungel der Linux-Distributionen die persönlich passende Distribution zu finden.">
  <meta name="description" lang = "en"  content ="The Linux Distribution Chooser helps you to find the suitable Distribution for you!">
  <meta name="keywords" content="Linux, Linux Chooser, Linux Distribution Chooser, Linux Auswahlhilfe, Linux Auswahl, Alternative to Windows, Linux Comparison, Linux Vergleich, Vergleich, Auswahlhilfe, Alternative zu Windows">
  <meta name="google-site-verification" content="nqtoKAtXX7xTNyddaEGkkYtgpc0pc0b-wigel0Acy5c" />
  <meta name="msvalidate.01" content="8165DC81CC6E5D6805201B58C5596403" />
  <meta name="generator" content="LDC 2015">
  <link rel="stylesheet" href="./Lib/bootstrap/css/lumen.css">
  <link  href="./Lib/font-awesome/css/font-awesome.css" rel="stylesheet">
  <link rel="stylesheet" href="./css/ldc.css">
  <link rel="icon" href="./assets/0fury.ico">
  <script src="./Lib/jquery.min.js"></script>
  <script src="./Lib/bootstrap/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="./js/ldc.js"></script>
  <script type="text/javascript" src="./js/ldc-ui.js"></script>
  <script type="text/javascript" src="./Lib/chart.min.js"></script>
  <script type="text/javascript" src="./Lib/spin.min.js"></script>
  <link rel="stylesheet" href="./Lib/rateyo/jquery.rateyo.css"/>
  <script src="./Lib/rateyo/jquery.rateyo.js"></script>
  <title>Linux Distribution Chooser</title>
</head>
<body>
  <div class="container">
   <div class="row">
    <?php include "./static/sidebar.php";?>
    <div class="col-lg-6 main">   
     <div class="row">        
      <div id='loadingHint'>      
      <p id="spinner"></p>
      <script type="text/javascript">
        var opts = {
          lines: 13 // The number of lines to draw
        , length: 28 // The length of each line
        , width: 14 // The line thickness
        , radius: 42 // The radius of the inner circle
        , scale: 1 // Scales overall size of the spinner
        , corners: 1 // Corner roundness (0..1)
        , color: '#000' // #rgb or #rrggbb or array of colors
        , opacity: 0.2 // Opacity of the lines
        , rotate: 0 // The rotation offset
        , direction: 1 // 1: clockwise, -1: counterclockwise
        , speed: 1 // Rounds per second
        , trail: 60 // Afterglow percentage
        , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
        , zIndex: 2e9 // The z-index (defaults to 2000000000)
        , className: 'spinner' // The CSS class to assign to the spinner
        , top: '40%' // Top position relative to parent
        , left: '50%' // Left position relative to parent
        , shadow: false // Whether to render a shadow
        , hwaccel: false // Whether to use hardware acceleration
        , position: 'fixed' // Element positioning
        }
        var target = document.getElementById('spinner')
        var spinner = new Spinner(opts).spin(target);
      </script>
    </div>
      <div class="panel-group" id="accordion" style="display:none;">
       <div class="panel panel-default">
        <div class="panel-heading">
         <h4 class="panel-title">
          <a id="welcomeTextHeader" class="collapsed ldcui"  data-toggle="collapse" data-parent="#accordion" href="#collapseOne">#</a>
        </h4>
      </div>
      <div id="collapseOne" class="panel-collapse ">
       <div class="panel-body ldcui" id="welcomeText">
        <div class="remarks">
         <h1 >
          Willkommen beim Linux Distribution Chooser! Welcome to the Linux Distribution Chooser!
        </h1>
        <div class="alert alert-info">
          Dieser Test soll Dir helfen, die für Deine Zwecke am besten geeignete Linux-Distribution zu finden. 
          Dabei stellt Dir der Test einfache Fragen, um z. B. ungeeignete Distributionen auszuschließen. 
          <br/>
          This Service should help you to find a suitable linux distribution which fits your needs. 
          The test will ask you simple questions to select the correct distributions.
        </div>
        <h2>Linux Distros:</h2>
        <div class="linux">
          <?php
            //SEO HACK
            $lang = 1;
            if (isset($_GET["l"]) && is_int((int)$_GET["l"]))
            {
              $lang = $_GET["l"];
            }
            $postdata = http_build_query(array("method" => "GetDistributions","lang"=> $lang,"args"=>""));           
            $opts = array('http' =>
                array(
                    'method'  => 'POST',
                    'header'  => 'Content-type: application/x-www-form-urlencoded',
                    'content' => $postdata,
                )
            );
            $context = stream_context_create($opts);
            $distros = json_decode(file_get_contents("http://distrochooser.de/rest.php", false, $context));          
          ?>
          <ul>
            <?php foreach ($distros as $value) :?>
              <li><a target="_blank" href="./detail.php?id=<?php echo $value->Id."&amp;l=".$lang;?>"><?php echo $value->Name;?></a></li>
            <?php endforeach;?>
          </ul>
        </div>
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
      </div>
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
    <li class="list-group-item"><a class="hidden-xs" id="homelink" href="index.php" style="display: inline;"><img src="./assets/ldc2alpha.png" alt="Linux Distribution Chooser" style="
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
<?php include "./static/dialogs.php";?>
</body>
</html>

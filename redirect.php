<?php
    if ($_SERVER["SERVER_NAME"] == "distrochooser.0fury.de"){      
      $params = $_SERVER["QUERY_STRING"];
      header("location: http://distrochooser.de/?".$params);
      exit();
    }
?>
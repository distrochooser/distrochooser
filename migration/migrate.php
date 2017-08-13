<?php
error_reporting(E_ALL);
//Quick and dirty ;)
$options  = array
            (
                \PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
                \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_OBJ
            );
$pdo   = new \PDO("mysql:host=localhost;dbname=ldc4", "root", "foobarbarz", $options);

$distros = json_decode(file_get_contents("./distros_format.json"));

$dictDistros = json_decode(file_get_contents("./dictDistro_format.json"));

$questions = json_decode(file_get_contents("./questions_format.json"));
$dictQuestions = json_decode(file_get_contents("./dictQuestions_format.json"));


$answers = json_decode(file_get_contents("./answers_format.json"));
$dictAnswers= json_decode(file_get_contents("./dictAnswers_format.json"));

$cleanUp = "Delete from ResultTags";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();

$cleanUp = "Delete from ResultAnswers";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();

$cleanUp = "Delete from Result";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();

$cleanUp = "Delete from Visitor";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();

$cleanUp = "Delete from Distro";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();
$cleanUp = "ALTER TABLE Distro AUTO_INCREMENT=1;";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();

$cleanUp = "Delete from i18n where val not  like 'sys.%'";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();


$variables = [
  "sys.links" => [
    "Links",
    "Links"
  ],
  "sys.about" => [
    "Über das Projekt",
    "About this project"
  ],

  "sys.privacy" => [
    "Datenschutz",
    "Privacy"
  ],

  "sys.contact" => [
    "Impressum",
    "Contact"
  ],

  "sys.vendor" => [
    "Ein Projekt von",
    "A project by"
  ],

  "sys.lang" => [
    "Sprache",
    "Language"
  ],

  "sys.welcometitle" => [
    "Willkommen",
    "Welcome"
  ],

  "sys.welcometext" => [
    "Willkommen",
    "Welcome"
  ],

  "sys.intro" => [
    "Willkommen auf distrochooser.de. Dieser Test soll Dir helfen, dich in der Welt der Linux-Distributionen zu orientieren.",
    "Welcome! This test will help you to choose a suitable Linux distribution for you."
  ],

  "sys.start" => [
    "Test starten",
    "Start the test"
  ],
  "sys.can-skip-questions" => [
    "Du kannst Fragen überspringen, wenn Du sie nicht beantworten willst",
    "You can always skip questions"
  ],
  "sys.can-get-result-anytime" => [
    "Du kannst zu jedem Zeitpunkt ein Ergebnis mit einem Klick auf \'auswerten\' einholen",
    "You can always click on \'get result\'"
  ],
  "sys.can-get-result-anyorder" => [
    "Du kannst die Fragen in beliebiger Reihenfolge beantworten",
    "You can answer in arbitrary order"
  ],
  "sys.can-delete" => [
    "Du kannst Antworten zurücknehmen, in dem du \'leeren\' auswählst",
    "You can delete answers at any time"
  ],
  "sys.can-mark-important" => [
    "Am Ende kannst Du Eigenschaften, die die wichtig sind, gewichten",
    "You can weight properties at the end of the test to emphasize what is important to you"
  ],
  "pc-advanced" => [
    "PC-Kenntnisse: Fortgeschritten",
    "Computer-Knowledge: Advanced"
  ],
  "pc-expert" => [
    "PC-Kenntnisse: Experte",
    "Computer-Knowledge: Professional"
  ],
  "linux-expert" => [
    "Linux-Kenntnisse: Experte",
    "Linux-Knowledge: Professional"
  ],
  "linux-advanced" => [
    "Linux-Kenntnisse: Fortgeschritten",
    "Linux-Knowledge: Sophisticated "
  ],
  "installer-no-defaults" => [
    "Installation: Keine Vorbelegungen",
    "Installation: No presets"
  ],
  "installer-hdd" => [
    "Installation auf Festplatte möglich",
    "Installation on Hard disk achievable"
  ],
  "help-wiki" => [
    "Hilfe über eigene (Wiki-) Dokumentation",
    "Help via Wiki present"
  ],
  "help-community" => [
    "Hilfe über Benutzercommunity möglich",
    "Help using community present"
  ],
  "pay-nothing" => [
    "Kostenlose Variante vorhanden",
    "Variants can be used free of charge"
  ],
  "installation-base" => [
    "Installiert nur die Betriebssystembasis",
    "Installs only base operating systems"
  ],
  "license-unfree-if-needed" => [
    "Nutz proprietäre ('unfreie') Lizenzen",
    "Applies software with nonfree licenses"
  ],
  "privacy-online-not-okay" => [
    "Baut keine Verbindungen im Hintergrund zu Drittanbietern, wie Suchmaschinen, auf",
    "Does not connect to third party companies in background, like search pages. "
  ],
  "programs-shell" => [
    "Softwareverwaltung zu großen Teilen über Terminalbefehle",
    "Software administration mostly via shell commands"
  ],
  "updates-unstable" => [
    "Schnelle, aber möglicherweise noch unstabile Software",
    "Fast updates, but can be unstable"
  ],
  "usage-daily" => [
    "Geeignet zum täglichen Gebrauch",
    "Can be used for daily usage"
  ],
  "pc-up-to-date" => [
    "Benötigt einen aktuellen Rechner. Funktioniert nur auf 64 bit Prozessoren.",
    "Requires a computer (mostly) with up to date components. Does not run on 32 bit CPU."
  ],
  "systemd" => [
    "Varianten benutzen systemd als Init-Prozess",
    "Variants are useing systemd as init process"
  ],
  "pc-beginner" => [
    "PC-Kenntnisse: Anfänger",
    "PC knowledge: Beginner"
  ],
  "linux-beginner" => [
    "Linux-Kenntnisse: Anfänger",
    "Linux knowledge: Beginner"
  ],
  "installer-defaults-wanted" => [
    "Installationsassitent mit Vorschlagewerten",
    "Installation assistant with preset values"
  ],
  "installation-live" => [
    "Live-Test zum gefahrlosen Vorab-Ausprobieren möglich",
    "Live-Test for pre tests possible"
  ],
  "mac-like" => [
    "Standard-Oberfläche erinnert an macOS",
    "Default user interface is macOS-ish"
  ],
  "installation-full" => [
    "Installiert auch Zusatzprogramme, wie z. B. einen Webbrowser",
    "Installs additional software, like web browsers"
  ],
  "privacy-online-okay" => [
    "Baut Verbindung zu Diensten im Hintergrund auf",
    "Connects to search companies in background"
  ],
  "ux-closed" => [
    "Hat ein eigens Farb-, Design- und Iconkonzept",
    "User interface has own color and design scheme"
  ],
  "programs-graphical" => [
    "Softwareverwaltung hauptsächlich über eine Art 'Appstore'",
    "Software management via App Store like tools"
  ],
  "updates-stable" => [
    "Updates werden später verteilt, sind aber stabiler",
    "Updates are less often, but more stable"
  ],
  "usage-gaming" => [
    "Spielehersteller unterstützen diese Distribution",
    "Game manufactures support this distribution"
  ],
  "no-systemd" => [
    "Varianten verzichten auf den Einsatz von systemd",
    "Some variants spare systemd usage"
  ],
  "pc-old" => [
    "Varianten für ältere System existent",
    "Variants for older computers existing"
  ],
  "license-free" => [
    "Verwendet freie Lizenzen (z. B. GNU GPL)",
    "Uses free licenses, like GNU GPL"
  ],
  "ux-undecided" => [
    "Hat kein vordefiniertes Designkonzept",
    "Does not deliver an closed design concept"
  ],
  "windows-like" => [
    "Grundsätzliches Designkonzept erinnert an Windows",
    "User interface Design concept reminds to Windows"
  ],
  "pay-price" => [
    "Es gibt kostenpflichtige Varianten, z. B. für geschäftliche Nutzung",
    "Fee-based variants existing, e. g. for enterprise usage"
  ],
  "installation-usb" => [
    "Kann auch auf USB-Sticks installiert werden",
    "Can be installed on USB sticks"
  ],
  "usage-rescue" => [
    "Kann zur Datenrettung benutzt werden, weil es von CD/ DVD/ USB gestartet werden kann",
    "Can be used for data rescue, because it can be bootet from USB/ DVD/ CD"
  ],
  "multipackage" => [
    "Erlaubt das Installieren von Paketen anderer Distributionen",
    "Is able to install packages from other distributions"
  ],
  "usage-anon" => [
    "Konzipiert für die Verwendung zur Anonymisierung",
    "Made for anonymisation purposes"
  ],
  "container" => [
    "Anwendungen werden isoliert in Containern ausgeführt",
    "Applications are executed in an isolated environemnt"
  ],
  "no-package-manager" => [
    "Anwendungen werden größenteils aus dem Quelltext gebaut",
    "Applications are installed by building them out of their sourcecode"
  ],
  "usage-science" => [
    "Bringt Anwendungen für den wissenschaftlichen Einsatz mit",
    "Delivers applications for scientific purposes"
  ],
  "important" => [
    "wichtig!",
    "important!"
  ],
  "notimportant" => [
    "unwichtig",
    "less important"
  ],
  "share" => [
    "Mein Ergebnis teilen",
    "Share my result"
  ],
  "sys.imagesource" => [
    "Bildquelle",
    "Image source"
  ],
  "sys.textsource" => [
    "Textquelle",
    "Text source"
  ],
  "sys.notags" => [
    "Wir konnten keine Übereinstimmung anhand deiner Anforderungen finden",
    "We could not find any matches based on your requirements"
  ],
  "sys.excludedbytag" => [
    "Diese Frage entspricht nicht Deinem Anforderungsprofil. Du kannst Sie beantworten, aber gerne auch überspringen",
    "This question is too far away from your requirement profile. You can answer it, but you can safely skip it."
  ],
  "sys.weightinfo" => [
    "Bewege den Schieberegler nach rechts, um eine Eigenschaft als wichtig zu vermerken. Links markiert ihn als unwichtig",
    "Move the slider to mark a property as important (right) or less important (left)"
  ],
  "sys.3" => [
    "Der von Dir angegeben Text gehört zu einer alten Version von distrochooser.de. Du findest Dein altes Ergebnis #link#",
    "This links contains an old test, created with a previous version of distrochooser.de. You can access this old test #link#"
  ],
  "sys.3link" => [
    "hier",
    "here"
  ],
  "sys.warning" => [
    "Achtung",
    "Attention"
  ]
];

foreach ($variables as $key => $value) {
    foreach ($value as $k => $translated){
      $query = "Insert into i18n (val, langCode, translation) VALUES (?,?,'$translated')";
      $stmt = $pdo->prepare($query);
      $stmt->bindValue(1,$key);
      $stmt->bindValue(2,$k === 0 ? "de": "en");
      $stmt->execute();
    }
}

$tagsToTranslate = [];

foreach ($distros as $key => $distro) {
  $tags = json_encode($distro->Characteristica,JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
  foreach(json_decode($distro->Characteristica) as $tkey => $tag){
    if (!in_array($tag,$tagsToTranslate) && !in_array($tag,array_keys($variables))){
      $tagsToTranslate[] = $tag;
    }
  }
  //$tags = str_replace("\"","'",$tags);
  $query = "Insert into Distro (name, website, textSource, imageSource, image, tags) VALUES (?,?,?,?,?,$tags)";
  $stmt = $pdo->prepare($query);
  $stmt->bindParam(1,$distro->Name);
  $stmt->bindParam(2,$distro->Homepage);
  $stmt->bindParam(3,$distro->TextSource );
  $stmt->bindParam(4,$distro->ImageSource );
  $stmt->bindParam(5,$distro->Image );
  
  $stmt->execute();
  $id = $pdo->lastInsertId();
  $translations = [];
  foreach($dictDistros as $dict){
    if ((int)$dict->DistributionId === (int)$distro->Id){
      echo "Found translation for ".$distro->Id."(".$dict->LanguageId .")\n";
      $translations[$dict->LanguageId === "1" ? "de":"en"] = $dict->Description;
    }
  }
  foreach ($translations as $key => $value) {
    $query = "Insert into i18n (val, langCode, translation) VALUES (?,?,?)";
    $stmt = $pdo->prepare($query);
    $stmt->bindValue(1,"d.$id.description");
    $stmt->bindValue(2,$key);
    $stmt->bindValue(3,$value);
    if(!$stmt->execute()){
      var_dump($translations);
      die();
    }
  }
}
$cleanUp = "Delete from Answer";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();
$cleanUp = "Delete from Question";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();
$cleanUp = "ALTER TABLE Question AUTO_INCREMENT=1;";
$stmt = $pdo->prepare($cleanUp);
$stmt->execute();

$questionMap = [];
foreach ($questions as $key => $question) {
  if ($question->ExclusionTags === null){
    $tags = "'[]'";
  }else{
    $tags = json_encode($question->ExclusionTags,JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
  }
  $query = "Insert into Question (orderIndex, isSingle, excludedBy) VALUES (?,?,$tags)";
  $stmt = $pdo->prepare($query);
  $stmt->bindParam(1,$question->OrderIndex);
  $stmt->bindParam(2,$question->Single);
  $stmt->execute();
  $id = $pdo->lastInsertId();
  $questionMap[$question->Id] = $id;
  echo "added question; $id\n";
  $translations = [];
  foreach($dictQuestions as $dict){
    if ((int)$dict->QuestionId === (int)$question->Id){
      echo "Found translation for ".$question->Id."(".$dict->LanguageId .")\n";
      $translations[$dict->LanguageId === "1" ? "de":"en"] = [$dict->Text,$dict->Help]; //title | text
    }
  }
  foreach ($translations as $key => $value) {
    $query = "Insert into i18n (val, langCode, translation) VALUES (?,?,'".$value[0]."')";
    $stmt = $pdo->prepare($query);
    $stmt->bindValue(1,"q.$id.title");
    $stmt->bindValue(2,$key);
    $stmt->execute();
    $query = "Insert into i18n (val, langCode, translation) VALUES (?,?,?)";
    $stmt = $pdo->prepare($query);
    $stmt->bindValue(1,"q.$id.text");
    $stmt->bindValue(2,$key);
    $stmt->bindValue(3,$value[1]);
    $stmt->execute();
  }
}


foreach ($answers as $key => $answer) {
  $tags = $answer->Tags;
  $excludeTags = $answer->NoTags;
  $query = "Insert into Answer (tags, excludeTags, questionId) VALUES ('$tags','$excludeTags',".$questionMap[$answer->QuestionId].")";
  var_dump($query);
  $stmt = $pdo->prepare($query);
  $stmt->execute();
  $id = $pdo->lastInsertId();
  echo "added answer $id";
  $translations = [];
  foreach($dictAnswers as $dict){
    if ((int)$dict->AnswerId === (int)$answer->Id){
      echo "Found translation for ".$answer->Id."(".$dict->LanguageId .")\n";
      $translations[$dict->LanguageId === "1" ? "de":"en"] = $dict->Text;
    }
  }
  foreach ($translations as $key => $value) {
    $query = "Insert into i18n (val, langCode, translation) VALUES (?,?,?)";
    $stmt = $pdo->prepare($query);
    $stmt->bindValue(1,"a.$id.text");
    $stmt->bindValue(2,$key);
    $stmt->bindValue(3,$value);
    $stmt->execute();
  }
}
<template>
  <div class='container'>
      <div class="columns">
        <div class="column col-4">
        </div>
        <div class="column col-4">
          <img class="logo" src="https://distrochooser.de/assets/tux.png">
          <a class="btn btn-primary" :href="'/' + $route.params.lang" :title="_i('back')"> {{ _i('back') }}</a>
          <div v-html="_i($route.params.info === 'privacy' ? 'content' : ($route.params.info === 'about' ? 'about_content' :  'contact_content'))">
          </div>
          <div v-if="$route.params.info === 'about' && $route.params.lang === 'de'">
            <p>
                Der Distrochooser soll helfen, sich in der Welt der Linux Distributionen einen Überblick zu verschaffen. </br>
                Der Distrochooser präsentiert dabei nur die Menge an Vorschlägen, die anhand der Antworten eingeschränkt werden. </br>
                </br>
                Daher kann es passieren, dass nicht ganz passende Ergebnisse geliefert werden, wenn die Komplexität der gegebenen Antwort ein realistisches Maß übersteigt.
            </p>
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>Version</th>
                  <th>Durchgeführte Tests</th>
                  <th>Veröffentlicht</th>
                </tr>
              </thead>
              <tbody>
                <tr class="active">
                  <td>1</td>
                  <td>~ 15000</td>
                  <td>14. Juni 2014</td>
                </tr>
                <tr class="active">
                  <td>2 <i>(LDC 2016)</i></td>
                  <td>270120</td>
                  <td>18. April 2015</td>
                </tr>
                <tr class="active">
                  <td>3 <i>(LDC 2017)</i></td>
                  <td>41899</td>
                  <td>13. April 2017</td>
                </tr>
                <tr class="active">
                  <td>4 <i>(LDC 2018)</i></td>
                  <td>-</td>
                  <td>Ende 2017</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="column col-4">
        </div>
      </div>
  </div>
</template>
 
<script>
export default {
  data: function () {
    return {
      'content': {
        'de': '<h2>Datenschutz</h2><p>Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.</p><p>Die Nutzung unserer Webseite ist in der Regel ohne Angabe personenbezogener Daten möglich. Soweit auf unseren Seiten personenbezogene Daten (beispielsweise Name, Anschrift oder E-Mail-Adressen) erhoben werden, erfolgt dies, soweit möglich, stets auf freiwilliger Basis. Diese Daten werden ohne Ihre ausdrückliche Zustimmung nicht an Dritte weitergegeben.</p><p>Wir weisen darauf hin, dass die Datenübertragung im Internet (z.B. bei der Kommunikation per E-Mail) Sicherheitslücken aufweisen kann. Ein lückenloser Schutz der Daten vor dem Zugriff durch Dritte ist nicht möglich.</p><br /><h2>Cookies</h2><p>Die Internetseiten verwenden teilweise so genannte Cookies. Cookies richten auf Ihrem Rechner keinen Schaden an und enthalten keine Viren. Cookies dienen dazu, unser Angebot nutzerfreundlicher, effektiver und sicherer zu machen. Cookies sind kleine Textdateien, die auf Ihrem Rechner abgelegt werden und die Ihr Browser speichert.</p><p>Die meisten der von uns verwendeten Cookies sind so genannte „Session-Cookies“. Sie werden nach Ende Ihres Besuchs automatisch gelöscht. Andere Cookies bleiben auf Ihrem Endgerät gespeichert, bis Sie diese löschen. Diese Cookies ermöglichen es uns, Ihren Browser beim nächsten Besuch wiederzuerkennen.</p><p>Sie können Ihren Browser so einstellen, dass Sie über das Setzen von Cookies informiert werden und Cookies nur im Einzelfall erlauben, die Annahme von Cookies für bestimmte Fälle oder generell ausschließen sowie das automatische Löschen der Cookies beim Schließen des Browser aktivieren. Bei der Deaktivierung von Cookies kann die Funktionalität dieser Website eingeschränkt sein.</p><br /><h2>Server-Log-Files</h2><p>Der Provider der Seiten erhebt und speichert automatisch Informationen in so genannten Server-Log Files, die Ihr Browser automatisch an uns übermittelt. Dies sind:</p><ul><li>Browsertyp und Browserversion</li><li>verwendetes Betriebssystem</li><li>Referrer URL</li><li>Hostname des zugreifenden Rechners</li><li>Uhrzeit der Serveranfrage</li></ul><p>Diese Daten sind nicht bestimmten Personen zuordenbar. Eine Zusammenführung dieser Daten mit anderen Datenquellen wird nicht vorgenommen. Wir behalten uns vor, diese Daten nachträglich zu prüfen, wenn uns konkrete Anhaltspunkte für eine rechtswidrige Nutzung bekannt werden.</p><br /><h2>SSL-Verschlüsselung</h2><p>Diese Seite nutzt aus Gründen der Sicherheit und zum Schutz der Übertragung vertraulicher Inhalte, wie zum Beispiel der Anfragen, die Sie an uns als Seitenbetreiber senden, eine SSL-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie daran, dass die Adresszeile des Browsers von "http://" auf "https://" wechselt und an dem Schloss-Symbol in Ihrer Browserzeile.</p><p>Wenn die SSL Verschlüsselung aktiviert ist, können die Daten, die Sie an uns übermitteln, nicht von Dritten mitgelesen werden.</p><br /><h2>Auskunft, Löschung, Sperrung</h2><p>Sie haben jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft und Empfänger und den Zweck der Datenverarbeitung sowie ein Recht auf Berichtigung, Sperrung oder Löschung dieser Daten. Hierzu sowie zu weiteren Fragen zum Thema personenbezogene Daten können Sie sich jederzeit unter der im Impressum angegebenen Adresse an uns wenden.</p><br /><p><em>Quelle: <a href="https://www.e-recht24.de">eRecht24</a></em></p>',
        'en': 'fas'
      },
      'contact_content': {
        'de': '<h2>Impressum</h2><h3>Angaben gemäß § 5 TMG:</h3> [data] </p> <h4>Kontakt:</h4> <ul><li>Email: me@0fury.de</li></ul></p>',
        'en': ''
      },
      'about_content': {
        'de': '<h2>Über distrochooser.de</h2>',
        'en': '<h2>About distrochooser.de</h2>'
      },
      'back': {
        'de': 'zurück zu distrochooser.de',
        'en': 'back to distrochooser.de'
      }
    }
  },
  methods: {
    _i: function (val) {
      var lang = this.$route.params.lang
      if (typeof lang === 'undefined') {
        lang = 'en'
      }
      if (typeof this[val] === 'undefined') {
        return val
      }
      return this[val][lang]
    }
  }
}
</script>
 
<style scoped>
.logo{
  margin: 0 auto;
  max-height: 10em;
  display: block;
}
.btn{
  margin: 0 auto;
  display: block;
  max-width: 14em;
  margin-bottom: 1em;
}
</style>

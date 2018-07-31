<template>
  <div class='container'>
      <div class="columns">
        <div class="column col-4 hidden-xs">
        </div>
        <div class="column col-4 col-xs-12">
          <img class="logo" src="/tux.png">
          <a class="btn btn-primary" :href="'/' + $route.params.lang" :title="text('back')"> {{ text('back') }}</a>
          <div v-if="$route.params.info !== 'donation'" v-html="text($route.params.info === 'privacy' ? 'content' : ($route.params.info === 'about' ? 'about_content' :  'contact_content'))">
          </div>
          <div v-if="$route.params.info === 'about' && $route.params.lang !== 'de'">
            <p>
                The target of distrochooser.de is to help Linux beginners to orientate and should be a help while choosing a suitable Linux distribution.</br>
                The results are only suggetions based on your answers. Please note: There may be more complex answer combinations causing wrong/ unrealistic results</br>
            </p>
            <p>
              Since 14th June 2014 distrochooser.de generated {{ 15000 + 270120 + 65945 + tests}} tests.
            </p>
          </div>
          <div v-if="$route.params.info === 'about' && $route.params.lang === 'de'">
            <p>
                Der Distrochooser soll helfen, sich in der Welt der Linux Distributionen einen Überblick zu verschaffen. </br>
                Der Distrochooser präsentiert dabei nur die Menge an Vorschlägen, die anhand der Antworten eingeschränkt werden. </br>
                </br>
                Daher kann es passieren, dass nicht ganz passende Ergebnisse geliefert werden, wenn die Komplexität der gegebenen Antwort ein realistisches Maß übersteigt.
            </p>
            <p>
              Seit dem 14. Juni 2014 wurden {{ 15000 + 270120 + 65945 + tests}} Tests erstellt.
            </p>
          </div>
          <div class="top" v-if="$route.params.info === 'about' && $route.params.lang === 'de'" >
            <h3>Lizenzen</h3>
            Distrochooser, basierend auf <a href="https://github.com/distrochooser/distrochooser">distrochooser/distrochooser</a>, unterliegt einer Doppellizenz.</br>
            <p>
              <h4>1. Der Sourcecode</h4>
              Der Sourcecode unterliegt den Lizenzbedingungen der im Repository verlinkten <code>LICENSE</code>-Datei
            </p>
            <p>
              <h4>2. Die Daten</h4>
            Die Inhalte (Fragen- & Antwortstruktur, Statistiken, Ergebnismatrizen) unterliegen einer proprietären Lizenz und deren Verwendung bedarft <a href="/info/de/contact/">unserer vorherigen Genehmigung</a>. Hiervon ausgeschlossen sind die Beschreibungstexte der Distributionen und deren Bilder. Diese unterliegen den Lizenzen der jeweiligen Rechteinhaber.
            </p>
          </div>
          <div class="top" v-if="$route.params.info === 'about' && $route.params.lang !== 'de'" >
            <h3>Licenses</h3>
            Distrochooser, based on <a href="https://github.com/distrochooser/distrochooser">distrochooser/distrochooser</a>, is double licensed.</br>
            <p>
              <h4>1. The Sourcecode</h4>
              The sourcecode is licensed on the license written in <code>LICENSE</code> file, which is placed in the linked repository.
            </p>
            <p>
              <h4>2. The data</h4>
              The question/ answer structure, the result matrix and statistics are proprietary. You can use them only <a href="/info/en/contact/">with our permission</a>. 
              The distribution logos and texts are excluded by this rule, because they are owned by their license owners.
            </p>
          </div>

          <div v-if="$route.params.info === 'about' && $route.params.lang === 'de'" >
            <h3>Besonderen Dank an</h3>
            <ul>
              <li>
                <a href="https://dribbble.com/shots/1211759-Free-195-Flat-Flags">Flat flag icons -  Muharrem Şenyıl</a>
              </li>
              <li>
                <a href="http://www.deviantart.com/art/Tondo-F-Icon-Set-OS-327759704">Tux Icon von P3T3B3</a>
              </li>
              <li>
                <a href="https://twitter.com/_phis">Christian für seine Hilfe & die Designhilfe für das Projekt</a>  
              </li>
              <li>
                <a href="https://github.com/picturepan2/spectre">spectre.css</a>
              </li>
              <li>
                <a href="https://nuxtjs.org">Nuxt.js</a>
              </li>
              <li>
                <a href="https://vuejs.org/">Vue.js</a>
              </li>
              <li>
                ...die vielen Rückmeldungen und Kritiken!
              </li>
            </ul>
          </div>
          <div v-if="$route.params.info === 'about' && $route.params.lang !== 'de'" >
            <h3>Special thanks to</h3>
            <ul>
              <li>
                <a href="https://dribbble.com/shots/1211759-Free-195-Flat-Flags">Flat flag icons -  Muharrem Şenyıl</a>
              </li>
              <li>
                <a href="http://www.deviantart.com/art/Tondo-F-Icon-Set-OS-327759704">Tux Icon by P3T3B3</a>
              </li>
              <li>
                <a href="https://twitter.com/_phis">Christian about this technical help and logo creation </a>  
              </li>
              <li>
                <a href="https://github.com/picturepan2/spectre">spectre.css</a>
              </li>
              <li>
                <a href="https://nuxtjs.org">Nuxt.js</a>
              </li>
              <li>
                <a href="https://vuejs.org/">Vue.js</a>
              </li>
              <li>
                ...to the many feedbacks!
              </li>
            </ul>
          </div>
        </div>
        <div class="column col-4 hidden-xs">
        </div>
      </div>
  </div>
</template>
 
<script>
import axios from "axios"; // eslint-disable-line no-unused-vars
import nuxt from "~/nuxt.config";
import imprint from "~/mixins/imprint"
export default {
  mixins: [
    imprint
  ],
  validate({ params }) {
    return (
      ["privacy", "contact", "about"].indexOf(params.info) !== -1 &&
      ["de", "en", "fr", "zh-cn"].indexOf(params.lang) !== -1
    );
  },
  data: function() {
    return {
      about_content: {
        de: "<h2>Über distrochooser.de</h2>",
        en: "<h2>About distrochooser.de</h2>",
        fr: "<h2>About distrochooser.de</h2>",
        "zh-cn": "<h2>信息</h2>"
      },
      back: {
        de: "zurück",
        en: "back",
        fr: "back",
        "zh-cn": "回去吧"
      },
      tests: 0,
      visitors: 0
    };
  },
  created: function() {
    var _t = this;
    axios
      .get(nuxt.globals.backend + "stats")
      .then(function(response) {
        _t.visitors = response.data.visitors;
        _t.tests = response.data.tests;
      })
      .catch(function(response) {
        console.log(response);
      });
  },
  methods: {
    text: function(val) {
      var lang = this.$route.params.lang;
      if (typeof lang === "undefined") {
        lang = "en";
      }
      if (typeof this[val] === "undefined") {
        return val;
      }
      return this[val][lang];
    }
  }
};
</script>
 
<style scoped>
.logo {
  margin: 0 auto;
  max-height: 10em;
  display: block;
}
.btn {
  margin: 0 auto;
  display: block;
  max-width: 14em;
  margin-bottom: 1em;
}
.top {
  margin-top: 1em;
}
</style>

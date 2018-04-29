<template>
  <div class='container'>
      <div class="columns">
        <div class="column col-4 hidden-xs">
        </div>
        <div class="column col-4 col-xs-12">
          <img class="logo" src="/tux.png">
          <a class="btn btn-primary" href="/" :title="_i('back')"> back</a>
          <h2>Translate distrochooser.de</h2>
          <p>
            <ol>
              <li>You can find the translation file "en.csv" (<a href="https://raw.githubusercontent.com/distrochooser/translations/master/en.csv">https://raw.githubusercontent.com/distrochooser/translations/master/en.csv</a>, can be opened e. g. with your table calculation program), which is the current english language set for the project.</li>
              <li>Just replace the english translations from the column "translation" with the ones fitting your language. Attention: There is a lot to translate.</li>
              <li>When you are finished, just provide it back to us (via email to me@0fury.de or via Pull Request, if you are GitHub User)</li>

            </ol>
            

         
            <p>
              Regular, I list contributors in the credits section of the service. If you want to get listed, also please tell me if I should use your real name or alias.
              <br>
              Additional, please tell me if you got a homepage you want to get linked. Please note, b/c distrochooser is a non profit project, I cannot get you a monetary reward for your work.
              <br>
              If you have any other questions, feel free to ask!
            </p>
          </p>
        </div>
      </div>
  </div>
</template>
 
<script>

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

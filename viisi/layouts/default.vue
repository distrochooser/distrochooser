<template>
  <div>
    <nuxt/>
  </div>
</template>

<style lang="scss">
@import '~/scss/variables.scss';
html {
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}
body {
  padding-top: 4em;
}
*,
*:before,
*:after {
  box-sizing: border-box;
  margin: 0;
}
body {
  background: $background;
}
@media only screen and (max-width: $mobileWidth) {
  .distrochooser {
    width: 100%;
    margin-left: 0px;
    margin-right: 0px;
  }
  .top-logo-container .top-logo {
    width: 50%;
  }
}
@media only screen and (min-width: $mobileWidth) {
  .distrochooser {
    width: 60%;
    margin-left: 20%;
    margin-right: 20%;
    margin-top: 2em;
  }
  .top-logo-container .top-logo {
    width: 25%;
    margin-bottom: 2em;
  }
}
.top-logo-container {
  text-align: center;
}
</style>

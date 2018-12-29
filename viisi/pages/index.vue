<template lang="pug">
  div.distrochooser
    div.top-logo-container
      img.top-logo(src='~/assets/logo.png')
    categories
</template>
<script>
import categories from '~/components/categories'
export default {
  components: {
    categories
  }
}
</script>
<style lang="scss">
@import '~/scss/variables.scss';

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
    width: 50%;
    margin-left: 25%;
    margin-right: 25%;
  }
  .top-logo-container .top-logo {
    width: 25%;
  }
}
.top-logo-container {
  text-align: center;
}
</style>

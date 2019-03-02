<template lang="pug">
  div.distribution
    div.title {{ name }}
    div.description(v-html="description")
    div.meta
      div.actions
        a.action(href="#")
          i.fa.fa-heart
        a.action(href="#")
          i.fa.fa-thumbs-down
      div.logo
        img(:src="logo")
</template>
<script>
export default {
  props: {
    name: {
      type: String,
      default: 'bratwurst'
    },
    description: {
      type: String,
      default: '<p>bla</p><p>bla</p>'
    },
    logo: {
      type: String,
      default: 'https://distrochooser.de/assets/linux/ubuntu.png'
    }
  }
}
</script>

<style lang="scss">
@import '~/scss/variables.scss';
.distribution {
  background: $questionBackground;
  padding-top: 1em;
}
.title {
  background: #dd4814 !important;
  color: white !important;
  margin-right: -0.5em;
  margin-left: -0.5em;
  height: 40px;
  padding: 10px;
  font-family: Karla, sans-serif;
  margin-bottom: 1em;
}
.description {
  margin: 1em;
  padding-bottom: 1em;
}
.meta .actions {
  width: 50%;
  display: inline-block;
  padding: 1em;
}
.action {
  margin-right: 1em;
}
.meta .logo {
  width: 50%;
  display: inline-block;
  text-align: right;
}
.meta .logo img {
  height: 5em;
  vertical-align: middle;
}
.fa-heart {
  color: #fe2424;
}
.fa-heart {
  color: #0e2bff;
}
</style>

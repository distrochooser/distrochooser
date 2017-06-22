<template>
    <div class="container">
      <div class="row">
          <navigation></navigation>
          <questions></questions>
      </div>
    </div>
</template>

<script>
    import navigation from '../components/navigation'
    import questions from '../components/questions'
    import i18n from '../mixins/i18n'
    export default {
      data () {
        return {}
      },
      components: {
        navigation,
        questions
      },
      mixins: [i18n]
    }
</script>

<style>
  .container{
    padding-top: 1em;
  }
</style>

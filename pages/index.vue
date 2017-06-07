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
    export default {
      data () {
        return {}
      },
      components: {
        navigation,
        questions
      }
    }
</script>

<style>
  .container{
    padding-top: 1em;
  }
</style>

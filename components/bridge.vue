<template>
    <div class="empty" v-if="isEnabled">
      <div class="empty-icon">
        <i class="icon icon-shutdown"></i>
      </div>
      <h4 class="empty-title">{{ text('sys.warning') }}</h4>
      <div class="empty-action"  v-html="redirectText">
      </div>
    </div>
</template>
<script>
  import i18n from '../mixins/i18n'
  export default{
    mixins: [i18n],
    computed: {
      link: function () {
        var link = 'https://old.distrochooser.de'
        if (this.test3 !== null) {
          link += '?test=' + parseInt(this.test3)
        }
        if (this.lang3 !== null) {
          link += (link.indexOf('?') === -1 ? '?' : '&') + 'lang=' + parseInt(this.lang3)
        }
        return link
      },
      redirectText: function () {
        var toastText = this.text('sys.3')
        var linkText = this.text('sys.3link')
        var link = this.link
        var html = '<a class="btn btn-primary" href="' + link + '" target="_blank">' + linkText + '</a>'
        return toastText.replace('#link#', html)
      },
      lang3: function () {
        return typeof this.$route.query['l'] !== 'undefined' ? this.$route.query['l'] : null
      },
      test3: function () {
        return typeof this.$route.query['test'] !== 'undefined' ? this.$route.query['test'] : null
      },
      isEnabled: function () {
        return this.test3 !== null
      }
    }
  }
</script>

<style scoped>
  .empty{
    margin-bottom: 1em;
  }
</style>


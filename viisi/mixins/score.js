export default {
  methods: {
    blocking: function(reasons) {
      return reasons.filter(r => {
        return r.isBlockingHit && !r.isRelatedBlocked
      })
    },
    nonBlocking: function(reasons) {
      return reasons.filter(r => {
        return !r.isBlockingHit && !r.isRelatedBlocked && !r.isNeutralHit
      })
    },
    getScore: function(reasons) {
      var allReasons = reasons.length
      var nonBlocking = this.nonBlocking(reasons).length
      var blocking = this.blocking(reasons).length
      if (blocking === 0) {
        return 0
      }
      return -(blocking / nonBlocking)
    }
  }
}

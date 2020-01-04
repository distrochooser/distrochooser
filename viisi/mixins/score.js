export default {
  methods: {
    blocking: function(reasons) {
      return reasons.filter(r => {
        return r.isBlockingHit && !r.isRelatedBlocked
      })
    },
    nonBlocking: function(reasons) {
      return reasons.filter(r => {
        return (
          !r.isBlockingHit &&
          !r.isRelatedBlocked &&
          !r.isNeutralHit &&
          r.isPositiveHit
        )
      })
    },
    negative: function(reasons) {
      return reasons.filter(r => {
        return !r.isBlockingHit && !r.isPositiveHit && !r.isNeutralHit
      })
    },
    getScore: function(reasons) {
      var allReasons = reasons.length
      var nonBlocking = this.nonBlocking(reasons).length
      var blocking = this.blocking(reasons).length
      var nonBlockingImportanceOffset = 0
      var blockingImportanceOffset = 0
      var negative = this.negative(reasons).length
      this.nonBlocking(reasons).forEach(value => {
        if (value.isImportant) {
          nonBlockingImportanceOffset++
        }
      })
      this.blocking(reasons).forEach(value => {
        if (value.isImportant) {
          blockingImportanceOffset++
        }
      })
      blocking += blockingImportanceOffset
      nonBlocking += nonBlockingImportanceOffset
      if (blocking === 0) {
        return nonBlocking - negative
      }
      return -(blocking / nonBlocking) - negative
    }
  }
}

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
    blockingHits: function(reasons) {
      var blocking = reasons.filter(r => {
        return r.isBlockingHit && !r.isRelatedBlocked
      })
      return blocking.length + blocking.filter(r => r.isImportant).length
    },
    nonBlockingHits: function(reasons) {
      var nonBlocking = reasons.filter(r => {
        return (
          !r.isBlockingHit &&
          !r.isRelatedBlocked &&
          !r.isNeutralHit &&
          r.isPositiveHit
        )
      })
      return nonBlocking.length + nonBlocking.filter(r => r.isImportant).length
    },
    negativeHits: function(reasons) {
      var negative = reasons.filter(r => {
        return !r.isBlockingHit && !r.isPositiveHit && !r.isNeutralHit
      })
      return negative.length + negative.filter(r => r.isImportant).length
    },
    percentageCompare: function(a, b) {
      var upvotePercentageA = a["votes"]["upvote_percentage"]
      var upvotePercentageB = b["votes"]["upvote_percentage"]
      var downvotePercentageA = a["votes"]["downvote_percentage"]
      var downvotePercentageB = b["votes"]["downvote_percentage"]
      
      if (upvotePercentageA > upvotePercentageB) return -1
      if (upvotePercentageA < upvotePercentageB) return 1

      if (downvotePercentageA > downvotePercentageB) return 1
      if (downvotePercentageA < downvotePercentageB) return -1

      return 0
    },
    scoreCompare: function(a, b) {
      var nonBlockingA = this.nonBlockingHits(a)
      var nonBlockingB = this.nonBlockingHits(b)

      var blockingA = this.blockingHits(a)
      var blockingB = this.blockingHits(b)

      var negativeA = this.negativeHits(a)
      var negativeB = this.negativeHits(b)
       

      if (nonBlockingA < nonBlockingB) return 1 
      if (nonBlockingA > nonBlockingB) return -1 

      if (blockingA > blockingB) return 1
      if (blockingA < blockingB) return -1

      if (negativeA > negativeB) return 1
      if (negativeA < negativeB) return -1

      return 0
    }
  }
}

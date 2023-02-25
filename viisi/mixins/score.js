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
      return blocking.length + blocking.filter(r => r.isImportant).length - blocking.filter(r => r.isLessImportant).length
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
      return nonBlocking.length + nonBlocking.filter(r => r.isImportant).length  - nonBlocking.filter(r => r.isLessImportant).length
    },
    negativeHits: function(reasons) {
      var negative = reasons.filter(r => {
        return !r.isBlockingHit && !r.isPositiveHit && !r.isNeutralHit
      })
      return negative.length + negative.filter(r => r.isImportant).length - negative.filter(r => r.isLessImportant).length
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
      var nonBlockingA = this.nonBlockingHits(a.reasons) + a.tags.length * 0.5
      var nonBlockingB = this.nonBlockingHits(b.reasons) + b.tags.length * 0.5

      var blockingA = this.blockingHits(a.reasons)
      var blockingB = this.blockingHits(b.reasons)

      var negativeA = this.negativeHits(a.reasons)
      var negativeB = this.negativeHits(b.reasons)
       

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

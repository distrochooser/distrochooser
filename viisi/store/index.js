import Vapi from 'vuex-rest-api'
import Vuex from 'vuex'
import viisiConfig from '~/viisi.json'
const indexStore = new Vapi({
  baseURL: viisiConfig.backendUrl,
  state: {
    data: null, //for initial bulk loading
    question: null,
    answers: null,
    categories: null,
    currentCategory: null,
    givenAnswers: [],
    token: null, //session token
    isStarted: false,
    result: null,
    translations: null,
    locales: null,
    voteResult: null,
    remarksAdded: false,
    language: 'en',
    testCount: 0,
    oldTestData: null,
    isSubmitted: false,
    rootUrl: viisiConfig.frontendUrl,
    answerBlockedAnswers: [],
    sessionStatus: null
  }
})
  .get({
    action: 'getLocales',
    property: 'locales',
    path: () => `locales/`
  })
  .get({
    action: 'start',
    property: 'data',
    path: ({ language, refLinkEncoded }) =>
      `start/${language}/${refLinkEncoded}/`
  })
  .get({
    action: 'language',
    property: 'data',
    path: ({ language }) => `translation/${language}/`
  })
  .get({
    action: 'loadQuestion',
    property: 'data',
    path: ({ language, index, token }) =>
      `question/${language}/${index}/${token}/`
  })
  .post({
    action: 'submit',
    property: 'result',
    path: ({ language, token }) => `submit/${language}/${token}/`
  })
  .post({
    action: 'voteSelection',
    property: 'voteResult',
    path: () => `vote/`
  })
  .post({
    action: 'addRemarks',
    property: 'remarksAdded',
    path: () => `remarks/`
  })
  .get({
    action: 'getOldAnswers',
    property: 'oldTestData',
    path: ({ slug }) => `answers/${slug}/`
  })
  .get({
    action: 'loadTranslations',
    property: 'translations',
    path: ({ language }) => `translations/${language}/`
  })
  .get({
    action: 'getAnswerBlockedAnswers',
    property: 'answerBlockedAnswers',
    path: ({ msgid }) => `blockedanswers/${msgid}/`
  })
  .get({
    action: 'getSessionStatus',
    property: 'sessionStatus',
    path: ({ token }) => `status/${token}/`
  })
  .getStore()

indexStore.actions.answerQuestion = (store, payload) => {
  var answer = payload.selectedAnswer
  var answer = {
    msgid: answer.msgid,
    answered: true,
    important: false,
    category: payload.currentCategory.msgid,
    blockedAnswers: answer.blockedAnswers
  }

  store.commit('setAnswerQuestion', answer)
  // TODO: push answer to server
  // TODO: Read result
}

indexStore.actions.submitAnswers = async (store, payload) => {
  store.commit('toggleSubmitted')
  await store.dispatch('submit', payload)
  store.commit('toggleSubmitted')
}

indexStore.mutations.setAnswerQuestion = (state, answer) => {
  state.givenAnswers.push(answer)
}

indexStore.mutations.toggleSubmitted = state => {
  state.isSubmitted = !state.isSubmitted
}

indexStore.mutations.toggleImportanceState = (state, answer) => {
  state.givenAnswers.forEach(a => {
    if (a.msgid === answer.msgid) {
      a.important = !a.important
    }
  })
}

indexStore.mutations.removeAnswerQuestion = (state, answer) => {
  for (var i = 0; i < state.givenAnswers.length; i++) {
    if (state.givenAnswers[i].msgid === answer.msgid) {
      state.givenAnswers.splice(i, 1)
      break
    }
  }
}

indexStore.actions.selectCategory = async (store, payload) => {
  var category = payload.selectedCategory
  store.commit('setSelectCategory', category)
  //TODO: trigger question change
  //TODO: load the question
  await store.dispatch('loadQuestion', {
    params: {
      language: payload.language,
      index: category.index,
      token: store.state.token
    }
  })
  store.commit('setCurrentQuestionData', store.state.data)
  store.commit('resetResult')
}

indexStore.mutations.setSelectCategory = (state, category) => {
  state.currentCategory = category
}

indexStore.actions.startTest = async (store, payload) => {
  await store.dispatch('start', payload)
  store.commit('setCurrentDisplayData', store.state.data)
  store.commit('setCurrentQuestionData', store.state.data)
}

indexStore.actions.switchLanguage = async (store, payload) => {
  await store.dispatch('language', payload)
  store.commit('setLanguageData', store.state.data)
}

indexStore.mutations.setLanguageData = (state, data) => {
  state.translations = data.translations
}

indexStore.mutations.setCurrentDisplayData = (state, data) => {
  state.categories = data.categories
  state.token = data.token
  state.language = data.language
  state.testCount = data.testCount
  state.translations = data.translations
}

indexStore.mutations.setCurrentQuestionData = (state, data) => {
  state.question = data.question
  state.answers = data.answers
}

indexStore.mutations.setStarted = state => {
  state.isStarted = true
}

indexStore.mutations.resetStarted = state => {
  state.isStarted = false
}

indexStore.mutations.resetResult = state => {
  state.result = null
}

indexStore.mutations.setOldTestData = state => {
  for (var i = 0; i < state.oldTestData.answers.length; i++) {
    var answer = state.oldTestData.answers[i]
    var category = state.oldTestData.categories[i]
    state.givenAnswers.push({
      //TODO: IS REDUNDANT
      msgid: answer,
      answered: true,
      important: state.oldTestData.important.indexOf(answer) !== -1,
      category: category,
      blockedAnswers: []
    })
  }
}

indexStore.actions.nextQuestion = (store, payload) => {
  store.commit('setStarted') //make sure the test is active
  const currentCategory = store.state.currentCategory
  var nextCategory = null
  if (currentCategory === null) {
    nextCategory = store.state.categories[0]
  } else {
    store.state.categories.forEach(c => {
      if (c.index === currentCategory.index + 1) {
        nextCategory = c
        return
      }
    })
  }
  store.dispatch('selectCategory', {
    language: payload.params.language,
    selectedCategory: nextCategory
  })
}

indexStore.actions.prevQuestion = (store, payload) => {
  store.commit('setStarted') //make sure the test is active
  const currentCategory = store.state.currentCategory
  var nextCategory = null
  if (currentCategory === null) {
    nextCategory = store.state.categories[0]
  } else {
    store.state.categories.forEach(c => {
      if (c.index === currentCategory.index - 1) {
        nextCategory = c
        return
      }
    })
  }
  store.dispatch('selectCategory', {
    language: payload.params.language,
    selectedCategory: nextCategory
  })
}

const createStore = () => {
  return new Vuex.Store(indexStore)
}

export default createStore

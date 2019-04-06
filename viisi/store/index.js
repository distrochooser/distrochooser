import Vapi from 'vuex-rest-api'
import Vuex from 'vuex'

const indexStore = new Vapi({
  baseURL: 'http://localhost:8000/',
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
    locales: null
  }
})
  .get({
    action: 'getLocales',
    property: 'locales',
    path: () => `locales`
  })
  .get({
    action: 'start',
    property: 'data',
    path: ({ language }) => `start/${language}/`
  })
  .get({
    action: 'loadQuestion',
    property: 'data',
    path: ({ language, index, token }) =>
      `question/${language}/${index}/${token}/`
  })
  .post({
    action: 'submitAnswers',
    property: 'result',
    path: ({ language, token }) => `submit/${language}/${token}/`
  })
  .getStore()

indexStore.actions.answerQuestion = (store, payload) => {
  var answer = payload.selectedAnswer
  var answer = {
    msgid: answer.msgid,
    answered: true,
    important: false
  }

  store.commit('setAnswerQuestion', answer)
  // TODO: push answer to server
  // TODO: Read result
}

indexStore.mutations.setAnswerQuestion = (state, answer) => {
  state.givenAnswers.push(answer)
}

indexStore.mutations.toggleImportanceState = (state, answer) => {
  state.givenAnswers.forEach(a => {
    if (a.msgid === answer.msgid) {
      a.important = !a.important
    }
  })
}

indexStore.mutations.removeAnswerQuestion = (state, answer) => {
  state.givenAnswers.splice(state.givenAnswers.indexOf(answer), 1)
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

indexStore.mutations.setCurrentDisplayData = (state, data) => {
  state.categories = data.categories
  state.token = data.token
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

const createStore = () => {
  return new Vuex.Store(indexStore)
}

export default createStore

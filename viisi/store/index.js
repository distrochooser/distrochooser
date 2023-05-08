import Vapi from 'vuex-rest-api'
import Vuex from 'vuex'
import viisiConfig from '~/distrochooser.json'
const indexStore = new Vapi({
  baseURL: viisiConfig.frontend.backendUrl,
  state: {
    data: null, //for initial bulk loading
    question: null,
    answers: null,
    categories: null,
    currentCategory: null,
    givenAnswers: [],
    markedQuestions: [],
    token: null, //session token
    sessionToken: null, //private session token
    isStarted: false,
    isAtHardwareScreen: false,
    result: null,
    translations: null,
    locales: {
      en: 'English',
      de: 'Deutsch',
      it: 'Italiano',
      'zh-hans': '简体中文',
      'zh-hant': '繁體中文',
      vn: 'Tiếng Việt',
      ch: 'Schwizerdütsch',
      fr: 'Français',
      ru: 'русский',
      nl: 'Dutch',
      he: 'עברית',
      es: 'español',
      fi: 'suomalainen',
      tr: 'Türkçe',
      'pt-br': 'português brasileiro',
      id: 'bahasa Indonesia',
      gr: "ελληνική γλώσσα",
      pl: 'Polski'
    },
    voteResult: null,
    remarksAdded: false,
    language: 'en',
    testCount: 0,
    oldTestData: null,
    isSubmitted: false,
    rootUrl: viisiConfig.frontend.frontendUrl,
    socialNetworks: viisiConfig.frontend.socialNetworks,
    answerBlockedAnswers: [],
    sessionStatus: null,
    method: 'default',
    visuallyImpairedMode: false,
    inRTLMode: true,
    showAllResults: false,
    debug: true,
    ratingSort: false,
    tags: {},
    clickRegisterResult: null,
    hardwareRequirements: null,
    autoToggleDarkMode: false
  }
})
  .post({
    action: 'start',
    property: 'data',
    path: ({ language }) => `start/${language}/`
  })
  .get({
    action: 'language',
    property: 'data',
    path: ({ language }) => `translation/${language}/`
  })
  .get({
    action: 'registerClick',
    property: 'clickRegisterResult',
    path: ({ id }) => `click/${id}`
  })
  .get({
    action: 'loadQuestion',
    property: 'data',
    path: ({ index }) => `question/${index}/`
  })
  .post({
    action: 'submit',
    property: 'result',
    path: ({ language, token, method }) =>
      `submit/${language}/${token}/${method}/`
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
  .get({
    action: 'storeHardwareRequirements',
    property: 'hardwareRequirements',
    path: ({ token, cores, frequency, memory, storage, is_touch, filterByHardware }) => `requirements/${token}/${cores}/${frequency}/${memory}/${storage}/${is_touch}/${filterByHardware}`
  })
  .getStore()

indexStore.actions.answerQuestion = async (store, payload) => {
  var answer = payload.selectedAnswer
  var answer = {
    msgid: answer.msgid,
    answered: true,
    important: false,
    lessImportant: false,
    category: payload.currentCategory.msgid,
    blockedAnswers: answer.blockedAnswers,
    tags: []
  }
  store.commit('setAnswerQuestion', answer)
}

indexStore.actions.submitAnswers = async (store, payload) => {
  store.commit('toggleSubmitted')
  payload.data.answers.forEach((answer) => {
    var msgid = answer.msgid
    answer["tags"] = []
    if (typeof store.state.tags[msgid]  !== undefined) {
      answer["tags"] = store.state.tags[msgid]
    }
  })
  await store.dispatch('submit', payload)
  store.commit('toggleSubmitted')
}

indexStore.mutations.setAnswerQuestion = (state, answer) => {
  state.givenAnswers.push(answer)
}

indexStore.mutations.toggleSubmitted = state => {
  state.isSubmitted = !state.isSubmitted
}


indexStore.mutations.showAllResults = state => {
  state.showAllResults = true
}

indexStore.mutations.openHardwareScreen = state => {
  state.isAtHardwareScreen = true
}

indexStore.mutations.closeHardwareScreen = state => {
  state.isAtHardwareScreen = false
}


indexStore.mutations.resetHardwareRequirements = state => {
  state.hardwareRequirements = null
}

indexStore.mutations.makeImportant  = (state, answer) => {
  state.givenAnswers.forEach(a => {
    if (a.msgid === answer.msgid) {
      a.important = true;
    }
  })
}


indexStore.mutations.toggleMarkingOfQuestion  = (state, question) => {
  const questionCategoryIndex = state.markedQuestions.indexOf(question)
  if (questionCategoryIndex !== -1) {
    state.markedQuestions.splice(questionCategoryIndex, 1);
  } else {
    state.markedQuestions.push(question);
  }
}

indexStore.mutations.makeLessImportant = (state, answer) => {
  state.givenAnswers.forEach(a => {
    if (a.msgid === answer.msgid) {
      a.lessImportant = true;
    }
  })
}


indexStore.mutations.resetImportanceState = (state, answer) => {
  state.givenAnswers.forEach(a => {
    if (a.msgid === answer.msgid) {
      a.lessImportant = false;
      a.important = false;
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
  store.commit('setStarted') //make sure the test is active
  store.commit('closeHardwareScreen') 
  var category = payload.selectedCategory
  store.commit('setSelectCategory', category)
  await store.dispatch('loadQuestion', {
    params: {
      index: category.index
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

indexStore.mutations.setVisuallyImpairedMode = (state, data) => {
  state.visuallyImpairedMode = data
}

indexStore.actions.setVisuallyImpairedMode = (store, payload) => {
  store.commit('setVisuallyImpairedMode', payload)
}

indexStore.mutations.setCurrentDisplayData = (state, data) => {
  state.categories = data.categories
  state.token = data.token
  state.sessionToken = data.sessionToken
  state.language = data.language
  state.testCount = data.testCount
  state.translations = data.translations
  /* only hebrew locale is currently rtl */
  if (state.language == "he") {
    state.inRTLMode = true
  } else {
    state.inRTLMode = false 
  }
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
  state.isSubmitted = false
  state.result = null
  state.currentCategory = null
}

indexStore.mutations.resetResult = state => {
  state.result = null
}

indexStore.mutations.resetRemarksAdded = state => {
  state.remarksAdded = false
}

indexStore.mutations.setOldTestData = state => {
  state.givenAnswers = []
  for (var i = 0; i < state.oldTestData.answers.length; i++) {
    var answer = state.oldTestData.answers[i]
    var category = state.oldTestData.categories[i]
    state.givenAnswers.push({
      //TODO: IS REDUNDANT
      msgid: answer,
      answered: true,
      important: state.oldTestData.important.indexOf(answer) !== -1,
      lessImportant: state.oldTestData.lessImportant.indexOf(answer) !== -1,
      category: category,
      blockedAnswers: []
    })
  }
}

indexStore.actions.nextQuestion = (store, payload) => {
  store.commit('setStarted') //make sure the test is active
  store.commit('closeHardwareScreen') 
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

indexStore.mutations.resetTags = (state, payload) => {
  delete state.tags[payload.answerId]
}


indexStore.mutations.removeTags = (state, payload) => {
  for (var i=0;i<payload.data.length;i++) {
    var tag = payload.data[i]
    var index = state.tags[payload.answerId].indexOf(tag)
    if (index !== -1) {
      state.tags[payload.answerId].splice(index, 1)
    }
  }
}

indexStore.mutations.saveTags = (state, payload) => {
  if (typeof state.tags[payload.answerId] === 'undefined') {
    state.tags[payload.answerId] = payload.selection
  } else {
    for (var i=0;i<payload.oldSelection.length;i++) {
      var tag = payload.oldSelection[i]
      var index = state.tags[payload.answerId].indexOf(tag)
      if (index !== -1) {
        state.tags[payload.answerId].splice(index, 1)
      }
    }
    payload.selection.forEach((value) => {
      if (state.tags[payload.answerId].indexOf(value) === -1) {
        state.tags[payload.answerId].push(value)
      }
    })
  }
}


indexStore.mutations.setAutoToggleDarkMode = state => {
  state.autoToggleDarkMode = true;
}

const createStore = () => {
  return new Vuex.Store(indexStore)
}

export default createStore

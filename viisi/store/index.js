import Vapi from 'vuex-rest-api'
import Vuex from 'vuex'

const indexStore = new Vapi({
  baseURL: 'MISSING',
  state: {
    categories: {
      Displaytext: 'foo',
      xx: 'fxxxoo',
      bav: 'fooxx',
      fasf: 'x',
      Disdasdasplaytext: 'xx',
      adsda: 'foaso',
      fasf: 'foasdo',
      xx: 'fooxasxca',
      xxy: 'fooxasxxca',
      xsx: 'fooaxasxca',
      xx2y: 'foox1asxxca',
      x1sx: 'fooa1xasxca'
    }
  }
})
  .get({
    action: 'getCategories',
    property: 'categories',
    path: () => `/categories`
  })
  .getStore()

const createStore = () => {
  return new Vuex.Store(indexStore)
}
export default createStore

import userAPI from '@/api/user'

// initial state
const state = () => ({
  isLoggedIn: false,
  user: null,

  isLoadingUser: false
})

// getters
const getters = {
  isLoadingUser: (state) => {
    return state.isLoadingUser
  },

  isLoadingGuilds: (state) => {
    return state.isLoadingGuilds
  },

  isLoggedIn: (state) => {
    return state.isLoggedIn
  },

  getCurrentUser: (state) => {
    return state.user
  }
}

// actions
const actions = {
  fetchCurrentUser({ commit }) {
    commit('loadingUser')
    userAPI.getUser(
      ({ user }) => {
        commit('setCurrentUser', user)
      },
      () => {
        commit('setCurrentUser', undefined)
      }
    )
  }
}

// mutations
const mutations = {
  setCurrentUser(state, userObject) {
    state.isLoggedIn = userObject != undefined
    state.user = userObject
    state.isLoadingUser = false
  },

  loadingUser(state) {
    state.isLoadingUser = true
  }
}

export default {
  namespaced: false,
  state,
  getters,
  actions,
  mutations
}

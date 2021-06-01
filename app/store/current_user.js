export const state = () => ({
  currentUser: null,
})

export const mutations = {
  setCurrentUser(state, { userId, jwt }) {
    state.currentUser = { userId, jwt }
  },
  clearCurrentUser(state) {
    state.currentUser = null
  },
}

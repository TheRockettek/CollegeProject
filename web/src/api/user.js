import { doLogin, doRequest, getRequest } from './routes'

export default {
  getUser(callback, errorCallback) {
    getRequest(
      '/api/users/@me',
      (response) => {
        response
          .json()
          .then((res) => {
            callback({ user: res })
          })
          .catch((error) => {
            errorCallback(error)
          })
      },
      (error) => {
        if (error.status >= 400) {
          errorCallback(error.statusText)
        } else {
          errorCallback(error)
        }
      }
    )
  },
  loginUser(username, password, remember, callback, errorCallback) {
    doRequest(
      'POST',
      '/api/auth/login',
      { username, password, remember },
      null,
      (response) => {
        response
          .json()
          .then((res) => {
            callback({ user: res })
          })
          .catch((error) => {
            errorCallback(error)
          })
      },
      (error) => {
        if (error.status == 401) {
          errorCallback('Invalid username or password')
        } else {
          errorCallback(error)
        }
      }
    )
  },
  logoutUser(callback, errorCallback) {
    getRequest(
      '/api/auth/logout',
      () => {
        callback()
      },
      (error) => {
        errorCallback(error)
      }
    )
  }
}

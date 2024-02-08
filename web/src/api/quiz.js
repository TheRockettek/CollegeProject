import { doLogin, doRequest, getRequest } from './routes'

export default {
  getQuizzes: (query, limit, offset, status, callback, errorCallback) => {
    getRequest(
      `/api/quizzes?query=${encodeURIComponent(query)}&limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}&status=${encodeURIComponent(status)}`,
      (response) => {
        response
          .json()
          .then((res) => {
            callback({ quizzes: res.quizzes, count: res.count })
          })
          .catch((error) => {
            errorCallback(error)
          })
      },
      (error) => {
        if (error.status == 401) {
          return doLogin()
        } else if (error.status >= 400) {
          return errorCallback(error.statusText)
        } else {
          return errorCallback(error)
        }
      }
    )
  },

  getQuizById: (id, callback, errorCallback) => {
    getRequest(
      `/api/quizzes/${encodeURIComponent(id)}`,
      (response) => {
        response
          .json()
          .then((res) => {
            callback(res)
          })
          .catch((error) => {
            errorCallback(error)
          })
      },
      (error) => {
        if (error.status == 401) {
          return doLogin()
        } else if (error.status >= 400) {
          return errorCallback(error.statusText)
        } else {
          return errorCallback(error)
        }
      }
    )
  },

  createQuiz: (quizData, callback, errorCallback) => {
    doRequest(
      'POST',
      '/api/quizzes',
      quizData,
      null,
      (response) => {
        response
          .json()
          .then((res) => {
            callback(res)
          })
          .catch((error) => {
            errorCallback(error)
          })
      },
      (error) => {
        if (error.status == 401) {
          return doLogin()
        } else if (error.status >= 400) {
          return errorCallback(error.statusText)
        } else {
          return errorCallback(error)
        }
      }
    )
  },

  updateQuiz: (id, quizData, callback, errorCallback) => {
    doRequest(
      'PUT',
      `/api/quizzes/${encodeURIComponent(id)}`,
      quizData,
      null,
      (response) => {
        response
          .json()
          .then((res) => {
            callback(res)
          })
          .catch((error) => {
            errorCallback(error)
          })
      },
      (error) => {
        if (error.status == 401) {
          return doLogin()
        } else if (error.status >= 400) {
          return errorCallback(error.statusText)
        } else {
          return errorCallback(error)
        }
      }
    )
  },

  deleteQuiz: (id, callback, errorCallback) => {
    doRequest(
      'DELETE',
      `/api/quizzes/${encodeURIComponent(id)}`,
      null,
      null,
      () => {
        callback()
      },
      (error) => {
        if (error.status == 401) {
          return doLogin()
        } else if (error.status >= 400) {
          return errorCallback(error.statusText)
        } else {
          return errorCallback(error)
        }
      }
    )
  }
}

export function getRequest(url, callback, errorCallback) {
  doRequest('GET', url, null, null, callback, errorCallback)
}

export function doRequest(method, url, data, files, callback, errorCallback) {
  var headers = {}
  var body

  if (files && files.length > 0) {
    body = new FormData()
    body.append('file', files[0])
    body.append('json', data ? JSON.stringify(data) : null)
  } else {
    headers['Content-Type'] = 'application/json'
    body = data ? JSON.stringify(data) : null
  }

  fetch(url, {
    method: method,
    headers: headers,
    body: body
  })
    .then((response) => {
      if (response.status >= 400) {
        errorCallback(response)
        return
      }

      callback(response)
    })
    .catch((error) => {
      errorCallback(error)
    })
}

export function doLogin() {
  let url = new URL(window.location.href)
  url.pathname = '/login'
  url.searchParams.append('path', window.location.pathname)

  window.location.href = url
}

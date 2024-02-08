export function getSuccessToast() {
  return {
    title: 'Changes saved.',
    success: true,
    class: 'text-green-500 bg-green-100'
  }
}

export function getValidationToast() {
  return {
    title: 'Please fix any errors before submitting',
    success: false,
    class: 'text-red-500 bg-red-100'
  }
}

export function getErrorToast(error) {
  return {
    title: error,
    success: false,
    class: 'text-red-500 bg-red-100'
  }
}

export function getRelativeTimeFromISO(string) {
  const date = new Date(string)
  if (isNaN(date)) {
    return ''
  }
  return getRelativeTimeString(date)
}

export function getRelativeTimeString(date) {
  // Allow dates or times to be passed
  const timeMs = date.getTime()

  // Get the amount of seconds between the given date and now
  const deltaSeconds = Math.round((timeMs - Date.now()) / 1000)

  // Array reprsenting one minute, hour, day, week, month, etc in seconds
  const cutoffs = [60, 3600, 86400, 86400 * 7, 86400 * 30, 86400 * 365, Infinity]

  // Array equivalent to the above but in the string representation of the units
  const units = ['second', 'minute', 'hour', 'day', 'week', 'month', 'year']

  // Grab the ideal cutoff unit
  const unitIndex = cutoffs.findIndex((cutoff) => cutoff > Math.abs(deltaSeconds))

  // Get the divisor to divide from the seconds. E.g. if our unit is "day" our divisor
  // is one day in seconds, so we can divide our seconds by this to get the # of days
  const divisor = unitIndex ? cutoffs[unitIndex - 1] : 1

  // Intl.RelativeTimeFormat do its magic
  const rtf = new Intl.RelativeTimeFormat(navigator.language, { numeric: 'auto' })
  return rtf.format(Math.floor(deltaSeconds / divisor), units[unitIndex])
}

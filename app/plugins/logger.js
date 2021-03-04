// define the methods
export const logger = (lvl, msg) => {
  const m = JSON.stringify(msg)
  if (lvl === 'error' || lvl === 'err' || lvl === 'e')
    if (window !== undefined) window.console.error(m)
    else console.error(m)
  else if (lvl === 'warning' || lvl === 'warn' || lvl === 'w')
    if (window !== undefined) window.console.warn(m)
    else console.warn(m)
  else if (lvl === 'info' || lvl === 'i')
    if (window !== undefined) window.console.info(m)
    else console.info(m)
}

export default ({ app }, inject) => {
  // inject methods so that they can be called in any component or function with this.$logger.
  inject('logger', logger)
}

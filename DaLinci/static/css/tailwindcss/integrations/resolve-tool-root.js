let path = require('path')

module.exports = function resolveToolRoot() {
  let { testPath } = expect.getState()
  let separator = '/'

  return path.resolve(
    __dirname,
    testPath
      .replace(__dirname + separator, '')
      .split(separator)
      .shift()
  )
}

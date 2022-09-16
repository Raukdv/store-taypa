const path = require("path");

module.exports = {
  outputDir: path.resolve(__dirname, "../../static/public/widget"),
  configureWebpack: config => {
    config.output.filename = 'js/[name].js'
    config.output.chunkFilename = 'js/[name].js';
  }
}

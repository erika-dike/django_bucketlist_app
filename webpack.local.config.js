var BundleTracker = require('webpack-bundle-tracker')
var config = require('./webpack.base.config.js')
var path = require("path")
var webpack = require('webpack')


var ip = 'localhost'

config.entry = {
    App1: [
        'webpack-dev-server/client?http://' + ip + ':3000',
        'webpack/hot/only-dev-server',
        './reactjs/App1',
    ],
}

config.output.publicPath = 'http://' + ip + ':3000' + '/assets/bundles/'

config.devtool = "#eval-source-map"

config.plugins = config.plugins.concat([
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new BundleTracker({filename: './webpack-stats-local.json'}),
    new webpack.DefinePlugin({
        'process.env': {
            'NODE_ENV': JSON.stringify('development'),
            'BASE_API_URL': JSON.stringify('https://' + ip + ':8000/dothebucket/'),
        }
    }),
])

config.module.loaders.push(
    { 
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loaders: ['react-hot', 'babel']
    }
)

module.exports = config
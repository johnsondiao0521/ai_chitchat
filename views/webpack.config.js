const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
module.exports = {
  entry: "./src/index.js",
  // mode: config.production ? "production" : "development",
  devtool: "inline-source-map",
  output: {
    path: path.resolve(__dirname, "./dist"),
    filename: "bundle.js",
    clean: true,
  },
  module: {
    rules: [
      //配置加载器
      {
        test: /\.(js|jsx)$/,
        loader: "babel-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.(css|less)$/,
        use: [
          {
            loader: "style-loader",
          },
          {
            loader: "css-loader",
            options: {
              importLoaders: 1,
            },
          },
          {
            loader: "less-loader",
            options: {
              lessOptions: {
                javascriptEnabled: true,
              },
            },
          },
        ],
      },
      {
        test: /\.(gif|jpe?g|png)$/,
        type: "asset/resource",
        generator: {
          filename: "images/[contenthash][ext]",
        },
        parser: {
          dataUrlCondition: {
            maxSize: 4 * 1024 * 1024, // 自定义值，默认小于8kb时转为inline，否则为resource
          },
        },
      },
    ],
  },
  resolve: {
    alias: {
      "@": path.join(__dirname, "./src"),
    },
  },
  plugins: [
    new HtmlWebpackPlugin({ template: "./public/index.html", inject: "body" }),
  ],
  devtool: "inline-source-map",
  devServer: {
    static: path.resolve(__dirname, "./dist"),
    hot: true,
    historyApiFallback: true,
  },
};

import React, { Component } from "react";
import '@/assets/style/index.css'
import Chat from './pages/chat'
import ReactDom from "react-dom";

class App extends Component {
  render() {
    return <Chat></Chat>;
  }
}

ReactDom.render(<App />, document.getElementById("root"));

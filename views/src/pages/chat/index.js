import React, { Component } from "react";
import style from "./style/index.module.less";
console.log(style);
import easybot from "@/assets/images/easybot.png";
class Chat extends Component {
  constructor(props) {
    super(props);
    this.contentRef = null;
    this.state = {
      inpValue: "初始数据",
      msgList: [],
    };
  }
  changeVal = (e) => {
    if (e.nativeEvent.inputType === "insertLineBreak") {
      return;
    }
    this.setState({ inpValue: e.target.value });
  };
  sendMsg = (e) => {
    if (!this.state.inpValue) {
      return;
    }
    const { msgList, inpValue } = this.state;
    msgList.push({
      key: +new Date(),
      value: inpValue,
      type: +new Date() % 2 ? "myChat" : "robotChat",
    });
    this.setState({ msgList, inpValue: "" }, () => {
      this.contentRef.scrollTop =
        this.contentRef.scrollHeight - this.contentRef.clientHeight;
    });
  };

  render() {
    return (
      <div className={style.page}>
        <div className={style.page_content}>
          <div className={style["page_content-title"]}>
            <img src={easybot}></img>
            <div>
              <h1>RASA</h1>
              <h2>KBQA+ES</h2>
            </div>
          </div>
          <div
            className={style["page_content-chat"]}
            ref={(el) => (this.contentRef = el)}
          >
            {this.state.msgList.map((item) =>
              item.type === "myChat" ? (
                <div
                  className={style["page_content-chat_myChat"]}
                  key={item.key}
                >
                  <div className={style.content}>{item.value}</div>
                  <img src="https://www.baidu.com/img/baidu_85beaf5496f291521eb75ba38eacbd87.svg"></img>
                </div>
              ) : (
                <div
                  className={style["page_content-chat_robotChat"]}
                  key={item.key}
                >
                  <img src="https://www.baidu.com/img/baidu_85beaf5496f291521eb75ba38eacbd87.svg"></img>
                  <div className={style.content}>{item.value}</div>
                </div>
              )
            )}
          </div>
          <div className={style["page_content-input"]}>
            <textarea
              value={this.state.inpValue}
              onInput={this.changeVal}
              onKeyUp={(e) => e.keyCode === 13 && this.sendMsg()}
            ></textarea>
            <button onClick={this.sendMsg}>发送</button>
          </div>
        </div>
        <div className={style.bg}></div>
      </div>
    );
  }
}

export default Chat;

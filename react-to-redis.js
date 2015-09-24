// Copyright (c) 2015, Hugo Herter
// All rights reserved.

'use strict'

var ReactToRedis = {
  /* React Mixin that updates the state of the component with values received
     from websocket. */

  componentDidMount: function () {
    this.socketSetup()
  },

  socketSetup: function () {
    this.socket = new window.WebSocket(
      'ws://' + window.location.host + '/ws'
    )
    this.socket.onopen = this.socketOnOpen
    this.socket.onclose = this.socketOnClose
    this.socket.onmessage = this.socketOnMessage
  },

  socketOnOpen: function () {
    this.socket.send('connect')
  },

  socketOnMessage: function (message) {
    var data = JSON.parse(message.data)
    this.setState(data)
  },

  socketOnClose: function (message) {
    console.log('Trying to reconnect...')
    setTimeout(this.socketSetup, 3000)
  },

  getInitialState: function () {
    return {}
  }
}

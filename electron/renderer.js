const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")


client.invoke("echo", "server ready", (error, res) => {
  if(error || res !== 'server ready') {
    console.error(error)
  } else {
    console.log("server is ready")
  }
})

let start = document.getElementById("start")
let name = document.querySelector('#name')

start.addEventListener('click', () => {
  client.invoke("recognizeStudent", (error, result) => {
    if(error) {
      console.error(error)
    } else {
      name.textContent = result
    }
  })
})

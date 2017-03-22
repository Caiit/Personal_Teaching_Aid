const electron = require('electron')
const {app, BrowserWindow} = electron
const path = require('path')

let mainWindow = null

const createWindow = () => {
  mainWindow = new BrowserWindow({width: 1280, height: 720})
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))
  mainWindow.setFullScreen(true)
  // Uncomment for debug tool
  // mainWindow.webContents.openDevTools()
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

// Handle python connection
let pyProc = null
let pyPort = null

const selectPort = () => {
  pyPort = 4242
  return pyPort
}

const createPyProc = () => {
  let port = '' + selectPort()
  let script = path.join(__dirname, 'python', 'main', 'PersonalAid.py')
  pyProc = require('child_process').spawn('python', [script, port])
  if (pyProc != null) {
    console.log('child process success')
  }
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

// TODO: check of dit in een ready kan ?
app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)

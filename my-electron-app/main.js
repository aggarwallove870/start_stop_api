const { app, BrowserWindow } = require('electron')
const path = require('path')

function createWindow() {
  const win = new BrowserWindow({
    width: 484,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  // win.loadURL('https://www.kashwork.com/')

  // win.loadURL("file://" + __dirname + "templates/employelogin.html");
  win.loadURL("http://127.0.0.1:5000/");
  // win.loadFile('templates/index.html')
  win.webContents.openDevTools();

}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

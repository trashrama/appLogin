// Modules to control application life and create native browser window
const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
function createWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 430,
    height: 932,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
    },
    resizable: false,
    autoHideMenuBar: true

  });

  setTimeout(() => {
    mainWindow.loadURL("http://localhost:5000/");
  }, 2000);

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();

  app.on("activate", function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

// Start Flask server
const flaskProcess = spawn("python3", ["./app.py"]);
flaskProcess.stdout.on("data", (data) => {
  console.log(`stdout: ${data}`);
});
flaskProcess.stderr.on("data", (data) => {
  console.error(`stderr: ${data}`);
});

app.on("quit", () => {
  flaskProcess.kill();
});

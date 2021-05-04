const https = require("https");
const tls = require("tls");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const createKeyCert = () => {
  const execOptions = { encoding: "utf-8", windowsHide: true };
  const key = path.join(__dirname, "key.pem");
  const certificate = path.join(__dirname, "cert.pem");

  if (!fs.existsSync(key) || !fs.existsSync(certificate)) {
    try {
      execSync(`openssl req -x509 -newkey rsa:2048 -keyout ./key.tmp.pem -out ${certificate} -days 365 -nodes -subj "/C=IL/ST=HaDarom/L=Beer Sheva/O=SmartScript/CN=34.76.66.213"`, execOptions);
      execSync(`openssl rsa -in ./key.tmp.pem -out ${key}`, execOptions);
      execSync("rm ./key.tmp.pem", execOptions);
    } catch (error) {
      console.error(error);
    }
  }

  return {
    key: fs.readFileSync(key),
    cert: fs.readFileSync(certificate),
    passphrase: "password",
  };
};

const createServer = (app) => {
  const options = createKeyCert();
  const tlsServer = tls.createServer(options, (socket) => {
    console.log("[TLS] Connected ", socket.authorized ? "authorized" : "unauthorized");
    socket.setEncoding("utf8");
    socket.pipe(socket);
  });

  return https.createServer(tlsServer, app);
};

module.exports = { createServer };

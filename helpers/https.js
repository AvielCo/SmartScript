const https = require("https");
const tls = require("tls");
const fs = require("fs");
const path = require("path");

const getCertificate = () => {
  const basePath = path.join(__dirname, "certificate");
  const key = path.join(basePath, "smartscript.sce-fpm.com.key");
  const certificate = path.join(basePath, "smartscript.sce-fpm.com.crt");
  const ca = path.join(basePath, "smartscript.sce-fpm.com.ca-bundle");
  return {
    key: fs.readFileSync(key),
    cert: fs.readFileSync(certificate),
    ca: fs.readFileSync(ca),
    hostname: "smartscript.sce-fpm.com",
    rejectUnauthorized: false,
    requestCert: true,
  };
};

const createServer = (app) => {
  const certificate = getCertificate();
  return https.createServer(certificate, app);
};

module.exports = { createServer };

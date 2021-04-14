/**
 * To register a new admin:
 * $ node SmartScript/helpers/bcrypt.js
 * > Enter password: 'Password'
 * > HashedPassword: .....
 * $ mongo
 * > use smartscript-db
 * > db.admins.insertOne({username: 'Username', password: 'HashedPassword'})
 *
 * Example:
 * $ node SmartScript/helpers/bcrypt.js
 * > Enter password: password
 * Your password is:  $2b$10$xKgsizrLQ6qgIlTeZgJcc.Qzttd9Mi0do3M.b2Eh2GB/efMWvwtuu
 * $ mongo
 * > use smartscript-db
 * > db.admins.insertOne({username: "Admin", password: "$2b$10$xKgsizrLQ6qgIlTeZgJcc.Qzttd9Mi0do3M.b2Eh2GB/efMWvwtuu"})
 *
 * ! IMPORTANT !
 * ! **************** Do not try to register an admin without hash the password. it will fail. **************** !
 */

const bcrypt = require('bcrypt');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question('Enter password: ', async function (password) {
  const salt = await bcrypt.genSalt(10);
  const hashedPassword = await bcrypt.hash(password, salt);
  console.log('Your password is: ', hashedPassword);
  process.exit(0);
});

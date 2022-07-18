const publicKeyToAddress = require('ethereum-public-key-to-address')
const fs = require("fs");

var addr = publicKeyToAddress(process.argv[2])
console.log(addr)
/*
fs.rename('addr', `С:/asuoki-data/${process.argv[3]}/addr`, err => {
   if(err) throw err;
});*/
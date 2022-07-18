var Wallet = require('ethereumjs-wallet');
const EthWallet = Wallet.default.generate();
var fs = require('fs-extra')
const { generateKeystore } = require('ethereum-keystore')
async function main() {
   console.log('password', process.argv[2])
   const keystore = await generateKeystore((EthWallet.getPrivateKeyString()), process.argv[2])
   fs.writeFileSync("./asuoki-data/key.key", EthWallet.getPrivateKeyString())
   console.log("key - [✓]")
   fs.writeFileSync("./asuoki-data/pub.key", EthWallet.getPublicKeyString())
   console.log("pub - [✓]")
   fs.writeFileSync("./asuoki-data/addr.addr", EthWallet.getAddressString())
   console.log("addr - [✓]")
   fs.writeFileSync("./asuoki-data/keystore/keystore.key", JSON.stringify(keystore))
   console.log("keystore - [✓]")
}

main()
   .then(() => process.exit(0))
   .catch((error) => {
      console.error(error);
      process.exit(1);
   });
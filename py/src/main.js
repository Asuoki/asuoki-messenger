window.newMessage;
var newMessage = [];
class TransactionChecker {
    async checkBlock() {
        var account = web3.eth.accounts.privateKeyToAccount(PRIVATE_KEY_OWNER);
        console.log("Account use: " + account.address);
        let block = await web3.eth.getBlock('latest');
        let number = block.number;
        console.log(number)
        if (block != null && block.transactions != null) {
            for (let txHash of block.transactions) {
                let tx = await web3.eth.getTransaction(txHash);
                if (tx != null && tx.from != account.address) {
                    console.log('New tx');
                    if(tx.from != account.address) {
                        var newMessageNoneArray = web3.utils.hexToAscii(tx.input)
                        newMessageNoneArray = ((newMessageNoneArray).substr(2, (newMessageNoneArray).length))
                        var length_signarure = newMessageNoneArray.substr(0, newMessageNoneArray.indexOf('!22!'))
                        var new_signature = newMessageNoneArray.substr(length_signarure.length+4, length_signarure)
                        var message = newMessageNoneArray.substr(new_signature.length+length_signarure.length+4)
                        if(web3.eth.accounts.recover(message, '0x' + new_signature)!=tx.from){
                            throw new UserException("Attention! Maybe the person you're talking to has been hacked! We do not recommend that you continue the chat! For your safety, we have prohibited further decryption of messages");
                        }
                        if(web3.eth.accounts.recover(message, ('0x' + new_signature))==tx.from){
                            console.log('Decrypt')
                            var decrypt = new JSEncrypt();
                            decrypt.setPrivateKey(RSA_PRIVATE_KEY);
                            var uncrypted = decrypt.decrypt(message);
                            newMessage.push(uncrypted)
                        }
                    }
                }
            }
        }
    }
}
let txChecker = new TransactionChecker;
setInterval(() => {
    txChecker.checkBlock();
}, 2000);
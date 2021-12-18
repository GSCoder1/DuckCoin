from django.shortcuts import render
import json
import hashlib
import datetime
import pprint
from django.http import JsonResponse

#https://medium.com/@erickzhang/https-medium-com-erickzhang-lets-build-a-blockchain-network-and-your-own-cryptocurrency-using-python-4b2620e61b76
#https://www.freecodecamp.org/news/create-cryptocurrency-using-python/
#https://medium.com/@MKGOfficial/build-a-simple-blockchain-cryptocurrency-with-python-django-web-framework-reactjs-f1aebd50b6c
"""
timeStamp = when the block is created
trans = transaction that is stored in the block
previousBlock = the hash of the previous block
hash = the block's hash
"""



class Block:
    def __init__(self, timeStamp, trans, previousBlock = ''):
        self.timeStamp = timeStamp
        self.trans = trans #transactional data stored in block
        self.previousBlock = previousBlock
        self.difficultyIncrement = 0
        self.hash = self.calculateHash(trans, timeStamp, self.difficultyIncrement) 
    
    def calculateHash(self, data, timeStamp, difficultyIncrement):
        data = str(data) + str(timeStamp) + str(difficultyIncrement)
        data = data.encode() #encode date and time
        hash = hashlib.sha256(data) #turn into hash
        return hash.hexdigest()
        
    def mineBlock(self,difficulty):
        difficultyCheck = "4" * difficulty
        while self.hash[:difficulty] != difficultyCheck:
            self.hash = self.calculateHash(self.trans,self.timeStamp,self.difficultyIncrement)
            self.difficultyIncrement = self.difficultyIncrement + 1 

class Transaction:
    def __init__(self, fromWallet, toWallet, amount):
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.amount = amount


class Blockchain:
    def __init__(self):
        self.chain = [self.GenesisBlock()]
        self.difficulty = 5 #allows system to control block generating speed. Need 5 consecutive 9's in this case
        self.pendingTransaction = []
        self.reward = 1 #reward for solving hash key

    def GenesisBlock(self):
        genesisBlock = Block(str(datetime.datetime.now()), "Genesis Block")
        return genesisBlock

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    #def appendNewBlock(self, newBlock):
     #   newBlock.previousBlock = self.getLastBlock().hash
     #   newBlock.hash = newBlock.calculateHash(newBlock.trans, newBlock.timeStamp)
     #   self.chain.append(newBlock)
    def minePendingTrans(self,minerRewardAddress):
        #in reality not all of the pending transactions go into the block. The miner gets to pick which one to mine.
        newBlock = Block(str(datetime.datetime.now()),self.pendingTransaction)        
        newBlock.mineBlock(self.difficulty)
        newBlock.previousBlock = self.getLastBlock().hash

        print("Previous Block's Hash:" + newBlock.previousBlock)
        chain = []
        for trans in newBlock.trans:
            temp = json.dumps(trans.__dict__, indent=5, separators=(',', ':')) #__dict__.indent=5
            chain.append(temp)
        pprint.pprint(chain)

        self.chain.append(newBlock)
        print("Block's Hash: " + newBlock.hash)
        print("Block added")
        
        rewardTrans = Transaction("System",minerRewardAddress,self.reward)
        self.pendingTransaction.append(rewardTrans)
        self.pendingTransaction = []

    def isChainValid(self):
        #ensure block is storing correct hash key of previous block.
        for x in range(1,len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[x-1]

            if (currentBlock.previousBlock != previousBlock.hash):
                return False
        return True

    def createTrans(self,transaction):
        self.pendingTransaction.append(transaction)
        
    def getBalance(self,walletAddress):
        balance = 0
        if (walletAddress == "Stevens Institute of Technology"):
            balance = 10000
        for block in self.chain:
            if block.previousBlock == "" :
                #dont check the genesis block
                continue 
            for transaction in block.trans:
                if transaction.fromWallet == walletAddress:
                    balance -= transaction.amount
                if transaction.toWallet == walletAddress:
                    balance += transaction.amount
        return balance

DuckCoin = Blockchain()


#transaction is from->to
#DuckCoin.createTrans(Transaction("Gurpreet", "Paven", 8.0))
#DuckCoin.createTrans(Transaction("Paven", "Siv", 3.0))

print("Stevens Institute of Technology is mining")
#need mining to validate transactions
#DuckCoin.minePendingTrans("")
#DuckCoin.minePendingTrans("Stevens Institute of Technology")
DuckCoin.createTrans(Transaction("Stevens Institute of Technology", "Gurpreet", 8.0))
DuckCoin.createTrans(Transaction("Gurpreet", "Siv", 3.0))
DuckCoin.createTrans(Transaction("Stevens Institute of Technology", "Paven", 5.0))



#Mines Previous transactions
DuckCoin.minePendingTrans("Stevens Institute of Technology")
#balance
print("Stevens Institute of Technology has " + str(DuckCoin.getBalance("Stevens Institute of Technology")) + " DuckCoin")
print("Gurpreet has " + str(DuckCoin.getBalance("Gurpreet")) + " DuckCoin")
print("Paven has " + str(DuckCoin.getBalance("Paven")) + " DuckCoin")
print("Siv has " + str(DuckCoin.getBalance("Siv")) + " DuckCoin")




#show chain
print(DuckCoin.isChainValid())



#if using Django:
# Mining a new block
'''
def mine_block(request):
    if request.method == 'GET':
        previous_block = DuckCoin.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = DuckCoin.proof_of_work(previous_nonce)
        previous_hash = DuckCoin.hash(previous_block)
        block = DuckCoin.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash']}
    return JsonResponse(response)

def get_chain(request):
    if request.method == 'GET':
        response = {'chain': DuckCoin.chain,
                    'length': len(DuckCoin.chain)}
    return JsonResponse(response)

    # Checking if the Blockchain is valid
def is_valid(request):
    if request.method == 'GET':
        is_valid = DuckCoin.is_chain_valid(DuckCoin.chain)
        if is_valid:
            response = {'message': 'The Blockchain is valid.'}
        else:
            response = {'message': 'The Blockchain is not valid.'}
    return JsonResponse(response)
'''
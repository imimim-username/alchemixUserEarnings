def getDonateAmounts(userAddress, alchemyEndpoint, subgraphEndpoint):

    import requests
    import json

    def getEvents():
        query = '''
            {
              alchemistDonateEvents(orderBy: timestamp, orderDirection: asc, first: 1000) {
                amount
                contract {
                  id
                }
                timestamp
                yieldToken
                transaction {
                  id
                  block {
                    number
                  }
                }
              }
            }
        '''

        data = {
            "query" : query
        }
        # puts the query into a usable data thingy for making a web request

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        #print('Getting events')
        queryResponse = requests.post(subgraphEndpoint, json=data, headers=headers)

        queryResponse = queryResponse.json()

        return(queryResponse['data']['alchemistDonateEvents'])

    def getTotalShares (blockNumber, alchemist, yieldToken):
    # gets the total number of shares of a yield token in the alchemist at a given block

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        dataStr = "0x5a5efc8b000000000000000000000000" + yieldToken[2:42]
        # composes the string that's passed in the payload to the api
        #0x5a5efc8b000000000000000000000000da816459f1ab5631232fe5e97a05bbbb94970c95

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_call",
            "params" : [
                    {
                        "from": "0x0000000000000000000000000000000000000000",
                        "data": dataStr,
                        "to": alchemist
                    },
                    blockNumber
                ],
            }
        # this invokes get yield token parameters, which includes total share

        shareResponse = requests.post(alchemyEndpoint, headers=headers, data=json.dumps(payload))

        #shareInfo = twos_complement(shareResponse.json()["result"][514:578])
        shareInfo = int(shareResponse.json()["result"][514:578],16)
        # the total shares is the ninth value in the really long hex string result.

        # print ("shareInfo")
        # print (shareInfo)
        return shareInfo

    def getUserShares (blockNumber, alchemist, yieldToken):
    # gets a user's number of shares in alchemist for a given yield token at given block number

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        dataStr = "0x4bd21445000000000000000000000000" + userAddress[2:42] + "000000000000000000000000" + yieldToken[2:42]
        # composes the string that's passed in the payload to the api

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_call",
            "params" : [
                    {
                        "from": "0x0000000000000000000000000000000000000000",
                        "data": dataStr,
                        "to": alchemist
                    },
                    blockNumber
                ],
            }
        # api request payload

        sharesResponse = requests.post(alchemyEndpoint, headers=headers, data=json.dumps(payload))

        #sharesInfo = twos_complement(sharesResponse.json()["result"][0:66])
        sharesInfo = int(sharesResponse.json()["result"][0:66],16)

        return sharesInfo

    def getYieldTokenSymbol (yieldToken):

        query = '''
            {
              yieldTokens(where: {id: "''' + yieldToken + '''"}) {
                id
                name
                symbol
              }
            }
        '''

        data = {
            "query" : query
        }
        # puts the query into a usable data thingy for making a web request

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        #print('Getting yield token symbol')
        queryResponse = requests.post(subgraphEndpoint, json=data, headers=headers)

        queryResponse = queryResponse.json()

        symbol = queryResponse['data']['yieldTokens'][0]['symbol']

        return symbol

    events = getEvents()

    userRewardsData = []

    for event in events:
        #print('--------------------------')
        blockNumber = hex(int(event['transaction']['block']['number']))
        #print('Block number: ')
        #print(event['transaction']['block']['number'])
        #print(blockNumber)

        totalshares = getTotalShares (blockNumber, event['contract']['id'], event['yieldToken'])
        #print('Total shares')
        #print(totalshares)

        usershares = getUserShares (blockNumber, event['contract']['id'], event['yieldToken'])
        #print('User shares')
        #print(usershares)

        if usershares > 0:
            userPercent = usershares/totalshares
            #print('User percentage of take')
            #print(userPercent)

            userReward = userPercent * int(event['amount'])
            userReward = userReward / 1e18
            #print('User Reward')
            #print(userReward)

            yieldTokenSymbol = getYieldTokenSymbol(event['yieldToken'])
            #print('Yield Token Symbol')
            #print(yieldTokenSymbol)
            if yieldTokenSymbol[-3:] == 'ETH':
                rewardToken = 'alETH'
            else:
                rewardToken = 'alUSD'

            #print('Reward token')
            #print(rewardToken)

            rewardsData = {
                'timestamp' : event['timestamp'],
                'txn' : event['transaction']['id'],
                'yieldToken' : rewardToken,
                'amountUnderlyingTokenEarned' : userReward
            }

            userRewardsData.append(rewardsData)

    return userRewardsData


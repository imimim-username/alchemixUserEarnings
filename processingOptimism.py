#getting user optimism yields


def doTheThingOptimism (address):

    import requests
    # for web things

    import json
    # for json things

    # import time
    # to run a timer

    api_key = open("/home/imimim/mysite/alch/alchemy_api_key_optimism.txt", "r")
    # get the alchemy_api_key

    alchemy_key = api_key.read()
    # read the key from the file

    api_key.close()
    # close the opened file

    apiString = "https://opt-mainnet.g.alchemy.com/v2/" + alchemy_key
    # constructs the alchemy api key

    def twos_complement(hex_value):
    # converts hex number to decimal, including negative hex numbers

        decimal_value = int(hex_value, 16)
        bit_length = len(hex_value) * 4
        if decimal_value & (1 << (bit_length - 1)):
            decimal_value -= 1 << bit_length
        return decimal_value

    tokenInfo = [
    # the various yield tokens
        {
            "name" : "aDAI",
            "contract" : "0x43a502d7e947c8a2ebbaf7627e104ddcc253abc6",
            "alchemist" : "0x10294d57a419c8eb78c648372c5baa27fd1484af",
            "decimals" : 18
        },
        {
            "name" : "aUSDC",
            "contract" : "0x4186eb285b1efdf372ac5896a08c346c7e373cc4",
            "alchemist" : "0x10294d57a419c8eb78c648372c5baa27fd1484af",
            "decimals" : 6
        },
        {
            "name" : "aUSDT",
            "contract" : "0x2680b58945a31602e4b6122c965c2849eb76dd3b",
            "alchemist" : "0x10294d57a419c8eb78c648372c5baa27fd1484af",
            "decimals" : 6
        },
        {
            "name" : "ysUSDC",
            "contract" : "0x059eaa296b18e0d954632c8242ddb4a271175eed",
            "alchemist" : "0x10294d57a419c8eb78c648372c5baa27fd1484af",
            "decimals" : 6
        },
        {
            "name" : "ysDAI",
            "contract" : "0x0a86adbf58424ee2e304b395af0697e850730ecd",
            "alchemist" : "0x10294d57a419c8eb78c648372c5baa27fd1484af",
            "decimals" : 18
        },
        {
            "name" : "aWETH",
            "contract" : "0x337b4b933d60f40cb57dd19ae834af103f049810",
            "alchemist" : "0xe04bb5b4de60fa2fba69a93ade13a8b3b569d5b4",
            "decimals" : 18
        },
        {
            "name" : "wstETH",
            "contract" : "0xe04bb5b4de60fa2fba69a93ade13a8b3b569d5b4",
            "alchemist" : "0xe04bb5b4de60fa2fba69a93ade13a8b3b569d5b4",
            "decimals" : 18
        }
    ]

    earnings = []
    # instantiates a blank array for tracking earnings

    #if len(sys.argv) > 1:
    #    address = sys.argv[1]
    # takes the address that's passed with the script and uses that as an address to look up

    def getHarvests (yieldToken):
    # uses the alchemix subgraph to get all of the harvests for a given token

        query = """
        {
          alchemistHarvestEvents(
            where: {timestamp_gte: \"0\", yieldToken: \"""" + yieldToken +"""\"}
            orderBy: timestamp
            orderDirection: asc
            first: 1000
            skip: 0
          ) {
            contract {
              id
            }
            transaction {
              id
            }
            yieldToken
            totalHarvested
            timestamp
          }
        }
        """
        # builds the query for getting a token's harvests

        data = {
        "query" : query
        }
        # puts the query into a usable data thingy for making a web request

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        graphURL = "https://api.thegraph.com/subgraphs/name/alchemix-finance/alchemix_v2_optimisim"
        # url for querying the graph

        queryResponse = requests.post(graphURL, json=data, headers=headers)

        queryData = queryResponse.json()

        return queryData

    def getBlockNumber (txn):
    # gets block number of transaction hash

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getTransactionByHash",
            "params" : [
                txn
            ]
        }
        # api request payload

        blockResponse = requests.post(apiString, headers=headers, data=json.dumps(payload))

        blockInfo = blockResponse.json()


        return(blockInfo["result"]["blockNumber"])

    def getUserShares (blockNumber, alchemist, yieldToken):
    # gets a user's number of shares in alchemist for a given yield token at given block number

        headers = {
            "Content-Type": "application/json"
        }
        #api call request headers

        dataStr = "0x4bd21445000000000000000000000000" + address[2:42] + "000000000000000000000000" + yieldToken[2:42]
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

        sharesResponse = requests.post(apiString, headers=headers, data=json.dumps(payload))

        # sharesInfo = twos_complement(sharesResponse.json()["result"][0:66])
        sharesInfo = int(sharesResponse.json()["result"][0:66],16)

        return sharesInfo

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

        shareResponse = requests.post(apiString, headers=headers, data=json.dumps(payload))

        #shareInfo = twos_complement(shareResponse.json()["result"][514:578])
        shareInfo = int(shareResponse.json()["result"][514:578],16)
        # the total shares is the ninth value in the really long hex string result.

        # print ("shareInfo")
        # print (shareInfo)
        return shareInfo




    def getHarvestShares (harvestInfo, alchemist, yieldToken, decimals, tokenName):
    # takes harvestInfo and gets the address's share of the harvestInfo

        for z in harvestInfo["data"]["alchemistHarvestEvents"]:
            # print(z)
            # print(z["transaction"]["id"])
            blockNumber = getBlockNumber(z["transaction"]["id"])
            # get the block number for a harvest transaction

            # print("block number")
            # print(blockNumber)
            userShares = getUserShares(blockNumber, alchemist, yieldToken)
            # get number of user shares for a yield token at the given block number

            # print(userShares)
            totalShares = getTotalShares (blockNumber, alchemist, yieldToken)
            # get the total number of shares in the alchemist at the given block number

            shareRatio = userShares / totalShares
            # calculate what proportion of the total shares belonged to the address in question

            # print("Share Ratio")
            # print(shareRatio)
            harvestShare = ((float(z["totalHarvested"]) * 0.9) * shareRatio) / (10 ** decimals)
            # given that 90% of the harvest gets applied to pay down user debt, that 90% is multiplied by the share ratio and divided by the number of deccimals to get the value for how much was credited

            # print("Harvest share")
            # print(harvestShare)
            harvestInfo = {
                "timestamp" : z["timestamp"],
                "txn" : z["transaction"]["id"],
                "yieldToken" : tokenName,
                "amountUnderlyingTokenEarned" : harvestShare
            }
            #compiles the information for an address's earnings for a harvest into one dict

            if harvestInfo["amountUnderlyingTokenEarned"] > 0:
                earnings.append(harvestInfo)
            # adds that dict to the array of all earnings if the address had any share of the earnings.

    def pinToPinata (inputJSON):
    # takes inputed JSON file and pins to pinata

        api_key = open("/home/imimim/mysite/alch/pinata_api_key.txt", "r")
        # get the pinata_api_key

        pinata_key = api_key.read()
        # read the key from the file

        api_key.close()
        # close the opened file

        # fileName = address + ".json"

        fileName = "harvestEarnings.json"

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": pinata_key
        }
        # pinata api call request headers

        request_data = {
            "pinataOptions": {
                "cidVersion": 1
             },
             "pinataMetadata": {
                "name": fileName
             },
             "pinataContent": inputJSON
        }
        # api request payload for writing debt values to pinata

        pinata_json_url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        # pinata endpoint for posting json

        # print("Pinning new user debt file to pinata")
        pinata_post = requests.post(pinata_json_url, headers = request_headers, data=json.dumps(request_data))
        # calls the pinata API for writing debt values to pinata

        result = pinata_post.json()
        # turns the result into a usable json

        # print("Pinata post result")
        # print(result)
        return result["IpfsHash"]

    #start = time.time()
    #start the timer

    # y = 0

    #if len(sys.argv) > 1:
    # checks to make sure a value was passed with runnign the script

    for x in tokenInfo :
    # goes through each yield token to get the harvests
        # print(x)
        # print(x["contract"])
        # print(x["alchemist"])
        tokenHarvests = getHarvests(x["contract"])
        # gets all the harvests for a given yield token

        #print (tokenHarvests)
        # y = y + 1

        getHarvestShares(tokenHarvests, x["alchemist"], x["contract"], x["decimals"], x["name"])
        # compiles address' share of harvests

        #if y == 1:
        #    break

    final = json.dumps(earnings, indent=4)
    # makes json out of the compiled information

    finalClean = json.loads(final)
    # cleans up the json file

    fileHash = pinToPinata(finalClean)
    #pins the clean json file to pinata

    fileURL = "https://ipfs.imimim.info/ipfs/" + fileHash

    return fileURL

# end = time.time()
# stop the timer

# address = input("Please enter your address: ")

# finalPinataURL = doTheThingOptimism(address)

# print(finalPinataURL)

# duration = end - start

# print("This thing took")
# print(duration)
# print("seconds to execute")

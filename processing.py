def doTheThing (address):

    import requests
    #for web requests

    import json
    # for json things

    api_key = open("/home/imimim/mysite/alch/alchemy_api_key_mainnet.txt", "r")
    # get the alchemy_api_key

    alchemy_key = api_key.read()
    # read the key from the file

    api_key.close()
    # close the opened file

    apiString = "https://eth-mainnet.g.alchemy.com/v2/" + alchemy_key
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
            "name" : "yvDAI",
            "contract" : "0xda816459f1ab5631232fe5e97a05bbbb94970c95",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 18
        },
        {
            "name" : "yvUSDC",
            "contract" : "0xa354f35829ae975e850e23e9615b11da1b3dc4de",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 6
        },
        {
            "name" : "yvUSDT_1",
            "contract" : "0x7da96a3891add058ada2e826306d812c638d87a7",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 6
        },
        {
            "name" : "yvUSDT_2",
            "contract" : "0x3b27f92c0e212c671ea351827edf93db27cc0c65",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 6
        },
        {
            "name" : "aDAI",
            "contract" : "0xce4a49d7ed99c7c8746b713ee2f0c9aa631688d8",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 18
        },
        {
            "name" : "aUSDC",
            "contract" : "0xf591d878608e2e5c7d4f1e499330f4ab9bbae37a",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 6
        },
        {
            "name" : "aUSDT",
            "contract" : "0xbc11de1f20e83f0a6889b8c7a7868e722694e315",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 6
        },
        {
            "name" : "vaUSDC",
            "contract" : "0xa8b607aa09b6a2e306f93e74c282fb13f6a80452",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 6
        },
        {
            "name" : "vaDAI",
            "contract" : "0x0538c8bac84e95a9df8ac10aad17dbe81b9e36ee",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 18
        },
        {
            "name" : "vaFRAX",
            "contract" : "0xc14900dfb1aa54e7674e1ecf9ce02b3b35157ba5",
            "alchemist" : "0x5c6374a2ac4ebc38dea0fc1f8716e5ea1add94dd",
            "decimals" : 18
        },
        {
            "name" : "yvWETH",
            "contract" : "0xa258c4606ca8206d8aa700ce2143d7db854d168c",
            "alchemist" : "0x062bf725dc4cdf947aa79ca2aaccd4f385b13b5c",
            "decimals" : 18
        },
        {
            "name" : "wstETH",
            "contract" : "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
            "alchemist" : "0x062bf725dc4cdf947aa79ca2aaccd4f385b13b5c",
            "decimals" : 18
        },
        {
            "name" : "rETH",
            "contract" : "0xae78736cd615f374d3085123a210448e74fc6393",
            "alchemist" : "0x062bf725dc4cdf947aa79ca2aaccd4f385b13b5c",
            "decimals" : 18
        },
        {
            "name" : "aWETH",
            "contract" : "0x61134511187a9a2df38d10dbe07ba2e8e5563967",
            "alchemist" : "0x062bf725dc4cdf947aa79ca2aaccd4f385b13b5c",
            "decimals" : 18
        },
        {
            "name" : "vaETH",
            "contract" : "0xd1c117319b3595fbc39b471ab1fd485629eb05f2",
            "alchemist" : "0x062bf725dc4cdf947aa79ca2aaccd4f385b13b5c",
            "decimals" : 18
        },
        {
            "name" : "sfrxETH",
            "contract" : "0xac3e018457b222d93114458476f3e3416abbe38f",
            "alchemist" : "0x062bf725dc4cdf947aa79ca2aaccd4f385b13b5c",
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

        # graphURL = "https://api.thegraph.com/subgraphs/name/alchemix-finance/alchemix_v2"
        # url for querying the graph
        graphURL = "https://subgraph.satsuma-prod.com/f98294de706d/alchemix--802384/alchemix-v2/api"
        # new graph url hosted by alchemy. Will start using when it has all the blocks

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

        #sharesInfo = twos_complement(sharesResponse.json()["result"][0:66])
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
                # adds that dict to the array of all earnings if the address had any share of the earnings

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

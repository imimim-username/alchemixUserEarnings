
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
# for making website things

from cryptoaddress import EthereumAddress
# to validate input address

# import requests
# to make web requests

# import json
# to do json things

from processing import doTheThing
# this is the main code for crunching the mainnet things

from processingOptimism import doTheThingOptimism
# main code for crunching the optimism things

from processingArbitrum import doTheThingArbitrum
# main code for crunching the Arbitrum things

app = Flask(__name__)

app.config["DEBUG"] = True
# to debug things

@app.route("/", methods=["GET", "POST"])
def adder_page():

    errors = ""
    if request.method == "POST":
        address = ""
        network = request.form.get('network', 'Mainnet')
        try:
            address = request.form["address"]
        except:
            errors += "<p>{!r} is not a valid address.</p>\n".format(request.form["address"])

        if address != "" :
            if network == 'Mainnet':
                finalURL = doTheThing(address)
            elif network == 'Optimism':
                finalURL = doTheThingOptimism(address)
            elif network == 'Arbitrum':
                finalURL = doTheThingArbitrum(address)
            else:
                finalURL = 'Error'
            return '''
                <html>
                    <body>
                        <p>Here is the URL that has the JSON with the address' share of {network} harvest earnings <a href="{finalURL}" target="_blank">{finalURL}</a></p>
                        <p>If the JSON includes alUSD or alETH as the yieldToken, that is the Address' share of bonus rewards that were included with a harvest.</p>
                        <p>These links will remain valid for approximately 30 days.</p>
                        <p>These values are a good faith effort, but are not guaranteed. Please verify these values against your own calculations.</p>
                        <p>If you need a CSV of the data, you can copy the above links and use them in a JSON to CSV converting service, such as <a href="https://www.convertcsv.com/json-to-csv.htm" target="_blank">https://www.convertcsv.com/json-to-csv.htm</a></p>
                    </body>
                </html>
            '''.format(network=network,finalURL=finalURL)

    return '''
        <html>
            <body>
                <p>Enter your address:</p>
                <form method="post" action=".">
                    <p><input name="address" /></p>
                    <p>
                        <label for="network">Choose a network:</label>
                        <select id="network" name="network">
                            <option value="Mainnet">Mainnet</option>
                            <option value="Optimism">Optimism</option>
                            <option value="Arbitrum">Arbitrum</option>
                        </select>
                    </p>
                    <p><input type="submit" value="Get earnings" /></p>
                    <p>This currently has no validation, so please only input valid Ethereum address</p>
                    <p>Your address is not logged anywhere, but it is needed to get the relevant history.</p>
                    <p>After you click the button, please be patient. It will probably take at least five minutes to query and generate all of your information.</p>
                    <p>The resultant JSON files that are generated do NOT contain identifying information, such as the entered address.</p>
                    <p>The JSON files will be automatically deleted after approximately 30 days.</p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)
    #added dropdown becaues server was timing out after 5 minutes when trying to do all the networks at once

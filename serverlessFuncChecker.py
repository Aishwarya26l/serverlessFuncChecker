try:
    import requests
except ImportError:
    from botocore.vendored import requests
import json

def getIndexPage():
    indexPage = """
    <html>
        <head>
            <meta charset="utf-8">
            <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
            <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
            <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
        </head>
        <body>
            <div id="app">
                <div class="md-layout">
                    <div class="md-layout-item md-size-100">
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">Serverless Function Checker</div>
                                <div class="md-subhead">Test your serverless function here</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <div class="md-layout md-gutter">
                                <div class="md-layout-item md-size-50">
                                    <md-field>
                                        <label>Enter API Endpoint</label>
                                        <md-input v-model="url"></md-input>
                                    </md-field>
                                </div>
                                <div class="md-layout-item md-size-50">
                                    <button class="button" v-on:click="staygo"><span>Submit</span></button>
                                </div>
                            </div>
                        </md-card-content>
                    </md-card>
                    </div>
                    <div class="md-layout-item md-size-100">
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">Tests</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <div class="md-layout md-gutter">
                                <div class="md-layout-item md-size-50">
                                    <md-field>
                                        <label>Hidden Testcases</label>
                                        <md-textarea v-model="hiddenTest"></md-textarea>
                                    </md-field>
                                </div>
                                <div class="md-layout-item md-size-50">
                                    <md-field>
                                        <label>Shown Testcases</label>
                                        <md-textarea v-model="shownTest"></md-textarea>
                                    </md-field>
                                </div>
                            </div>
                        </md-card-content>
                    </md-card>
                    </div>
                    <div class="md-layout-item md-size-100 output-card">
                        <md-card>
                            <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">Output</div>
                                <div class="md-subhead">Test results</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <md-field>
                                <md-tabs> 
                                    <md-tab id="tab-htmlResults" md-label="HTML results">
                                        <div v-html="answer.htmlFeedback"></div>
                                    </md-tab>
                                    <md-tab id="tab-jsonResults" md-label="JSON results">
                                        <md-textarea class="output-tab" v-model="answer.jsonFeedback" readonly></md-textarea>
                                    </md-tab>
                                    <md-tab id="tab-textResults" md-label="Text results">
                                        <md-textarea class="output-tab" v-model="answer.textFeedback" readonly></md-textarea>
                                    </md-tab>                            
                                </md-tabs>
                            </md-field>
                        </md-card-content>
                    </md-card>
                    </div>
                </div>
            </div>
        </body> 
        <script src="https://unpkg.com/vue"></script>
        <script src="https://unpkg.com/vue-material@beta"></script>
        <script>
            Vue.use(VueMaterial.default)
            new Vue({
                el: '#app',
                data: {
                    hiddenTest: "URL, shouldContain, amazon\\nGET, text=banana, response.body, shouldContain, YOUR_USER_TOKEN",
                    shownTest: "GET, text=madam, response.type, shouldEqual, text/text\\nGET, text=banana, response.body, shouldContain, banana",            
                    url:"https://f9awomc0fj.execute-api.ap-southeast-1.amazonaws.com/default/isPalindrome",
                    answer:""
                },
                methods: {
                    staygo: function () {
                    const gatewayUrl = '';
                    fetch(gatewayUrl, {
                method: "POST",
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({userToken:"ABCDE",shown:{0:this.shownTest},editable:{0:this.url}, hidden:{0:this.hiddenTest}})
                }).then(response => {
                    return response.json()
                }).then(data => {
                    this.answer = JSON.parse(JSON.stringify(data))
                    })
                }
                }
            })
        </script>
        <style lang="scss" scoped>
            #app {
                padding: 10px;
            }
            textarea {
                font-size: 1rem !important;
            }
            .md-card-header{
                padding-top: 0px;
            }
            .md-tabs{
                width:100%;
            }
            .md-tabs-container .md-tab textarea{
                height:100%;
            }
            .md-tab{
                min-height:500px;
            }
            .md-content{
                min-height:500px;
            }
            .output-tab{
                min-height:400px !important;
            }
            .output-card > .md-card > .md-card-content > .md-field{
                padding-top: 0px;
            }
            .button {
                display: inline-block;
                border-radius: 4px;
                background-color: #0099ff;
                border: none;
                color: #FFFFFF;
                text-align: center;
                font-size: 28px;
                padding: 20px;
                width: 200px;
                transition: all 0.5s;
                cursor: pointer;
                margin: 5px;
                //transform: translate(50%, 100%)
            }

            .button span {
                cursor: pointer;
                display: inline-block;
                position: relative;
                transition: 0.5s;
            }

            .button span:after {
                content: '>';
                position: absolute;
                opacity: 0;
                top: 0;
                right: -20px;
                transition: 0.5s;
            }

            .button:hover span {
                padding-right: 25px;
            }

            .button:hover span:after {
                opacity: 1;
                right: 0;
            }
        </style>
    </html>
    """
    return indexPage

def exec_tests(testUrl,test,userToken,isHidden):
    jsonResponse = {"results": []}
    for oneTest in test:
        partsOfTest = oneTest.split(",")
        partsOfTest = list(map(str.strip, partsOfTest))
        if(partsOfTest[0].lower() == "url"):
            # -------------------------------------#
            # [0]     [1]         [2]
            # method, testMethod, testValue
            # URL, shouldContain, abc
            # -------------------------------------#
            if(partsOfTest[1].lower() == "shouldcontain" and testUrl):
                opStr = "\"{received}\".find('{testValue}') != -1".format(
                            received = testUrl,
                            testValue = partsOfTest[2])
            else:
                opStr = "False"
        else: 
            execUrlStr = """requests.{method}(url="{url}?{parameter}")""".format(
            method = partsOfTest[0].lower(),
            url = testUrl,
            parameter = partsOfTest[1])
            urlResponse = eval(execUrlStr)
            resStatusCode = urlResponse.status_code  
            # -------------------------------------#
            # [0]     [1]         [2]             [3]         [4]
            # method, parameters, responseTarget, testMethod, testValue
            # GET, name=abc, response.type, shouldEqual, text/text
            # GET, text=banana, response.json.anotherResult, shouldEqual, Hey there
            # Define responseTarget
            # -------------------------------------#
            if(partsOfTest[2].lower() == "response.type"):
                targetStr = "headers['Content-Type']"
            elif(partsOfTest[2].lower() == "response.body"):
                targetStr = "text"
            elif(partsOfTest[2] and partsOfTest[2].lower().find("response.json") !=1 ):
                targetStr = "json()"
            else: # Default target text
                targetStr = "text"
            execReq = str(eval("urlResponse."+targetStr))
            # format json correctly, replace ' with " and " with \\"
            finalRes = execReq.replace("'",'"').replace('"', '\\"')
            # -------------------------------------#
            # For json() target
            # -------------------------------------#
            if(targetStr == "json()" and resStatusCode == 200):
                keys = ""
                # response.json.key1.key2 -> get all the keys
                for key in partsOfTest[2].split(".")[2:]:
                    keys +="[\"{key}\"]".format(key=key)
                temp = "json.loads(\"{received}\"){keys}".format(
                            received = finalRes, 
                            keys = keys)
                finalRes = eval(temp)
            # -------------------------------------#
            # Define testMethod/operation
            # -------------------------------------#
            if execReq:
                if(partsOfTest[3].lower() == "shouldequal"):
                    opStr = "\"{received}\" == \"{testvalue}\"".format(
                            received = finalRes, 
                            testvalue = partsOfTest[4])
                elif(partsOfTest[3].lower() == "shouldcontain"):
                    if(partsOfTest[4] == "YOUR_USER_TOKEN" and finalRes):
                        opStr = "\"{received}\".find('{testValue}') != -1".format(
                            received = finalRes,
                            testValue = userToken)
                    else:
                        opStr = "\"{received}\".find('{testValue}') != -1".format(
                            received = finalRes,
                            testValue = partsOfTest[4])
                else:
                    opStr = "False"
            else:
                opStr = "False"
        execOpStr = """{operation}""".format(operation=opStr)
        execOp = str(eval(execOpStr))
        result = {}
        if(isHidden):
            result = {"method": "HIDDEN", 
                    "parameters": "HIDDEN",
                    "responseTarget": "HIDDEN",
                    "testMethod": "HIDDEN",
                    "testValue": "HIDDEN", 
                    "receivedValue": "HIDDEN",  
                    "statusCode": "HIDDEN",
                    "correct": execOp}
        else:
            if(partsOfTest[0].lower() == "url"):
                result = {"method": partsOfTest[0], 
                    "parameters": "--", 
                    "responseTarget": "--",
                    "testMethod": partsOfTest[1], 
                    "testValue": partsOfTest[2], 
                    "receivedValue": "--", 
                    "statusCode":"--", 
                    "correct": execOp}
            else:
                result = {"method": partsOfTest[0], 
                        "parameters": partsOfTest[1], 
                        "responseTarget": partsOfTest[2],
                        "testMethod": partsOfTest[3], 
                        "testValue": partsOfTest[4], 
                        "receivedValue": execReq, 
                        "statusCode":resStatusCode, 
                        "correct": execOp}
        jsonResponse["results"].append(result)
    return jsonResponse

def calcFeedback(jsonResponse,userToken):
    jsonResponseData = json.loads(json.dumps(jsonResponse))
    resultContent = jsonResponseData.get('results')
    textResults = ""
    tableContents = ""
    textBackgroundColor = "#ffffff"
    allTestCaseResult = True
    if resultContent:
        for i in range(len(resultContent)):
            methodText = resultContent[i]["method"]
            parameterText = resultContent[i]["parameters"]
            responseTargetText = resultContent[i]["responseTarget"]
            testMethodText = resultContent[i]["testMethod"]
            # test value YOUR_USER_TOKEN = ABCD or testvalue
            testValueText = "YOUR_USER_TOKEN = " + userToken if (resultContent[i]["testValue"] == "YOUR_USER_TOKEN") else resultContent[i]["testValue"]
            receivedValueText = resultContent[i]["receivedValue"]
            statusCode = resultContent[i]["statusCode"]
            correctText = resultContent[i]["correct"]
            # Collective Pass or Fail
            allTestCaseResult = (allTestCaseResult and (correctText == "True"))
            if methodText == "HIDDEN":
                textResults += ("\n Private Test - ")
            else:
                textResults += ("\n Public Test - ")
            if correctText == "True":
                textResults += ("Passed.\n")
                textBackgroundColor = "#b2d8b2" #Green
            else:
                textResults += ("Failed.\n") 
                textBackgroundColor = "#ff9999" #Red
            if methodText == "HIDDEN":
                textResults += ("INFO: Hidden test failed.\n")
            else:
                textResults += ("INFO: Status code {statusCode}. {method} call with "
                                "{parameter} and received {responseTarget} as " 
                                "{receivedValue} against the expected value " 
                                "of {testValue}.\n").format(
                                    statusCode=statusCode,
                                    method=methodText, 
                                    parameter=parameterText, 
                                    responseTarget=responseTargetText, 
                                    receivedValue=receivedValueText,
                                    testValue=testValueText)
            tableContents = tableContents + """
            <tr bgcolor={color}>
                <td>{method}</td>
                <td>{parameter}</td>
                <td>{responseTarget}</td>
                <td>{testMethod}</td>
                <td>{testValue}</td>
                <td>{receivedValue}</td>
                <td>{statusCode}</td>
                <td>{correct}</td>
            </tr>
            """.format(method=methodText, parameter=parameterText, 
                    responseTarget=responseTargetText, testMethod=testMethodText, 
                    testValue=testValueText, receivedValue=receivedValueText, 
                    statusCode=statusCode, correct=correctText, 
                    color=textBackgroundColor)
    tableContents = ("<span class=\"md-subheading\">"
                    "All tests passed:" 
                    "{allPassed}</span><br/>").format(
                            allPassed=str(allTestCaseResult)) + tableContents
    textResults = ("All tests passed: {allPassed}\n").format(
                    allPassed=str(allTestCaseResult)) + textResults
    if not resultContent:
        textResults = "Your test is passing but something is incorrect..."
    htmlResults = """
        <html>
            <head>
                <meta charset="utf-8">
                <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
            </head>
            <body>
                <div>
                    <table>
                         <thead>
                            <tr>
                                <th>Method</th>
                                <th>Parameters</th>
                                <th>Response Target</th>
                                <th>Test Method</th>
                                <th>Test Value</th>
                                <th>Received Value</th>
                                <th>Status Code</th>
                                <th>Correct</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tableContents}
                        </tbody>
                    </table>
                </div>
            </body>
            <style>
            br {{
                display:block;
                content:"";
                margin:1rem
            }}
            table{{
                text-align:center
            }}
            </style>
        </html>
        """.format(tableContents=tableContents)
    allFeedback = {"isCorrect": allTestCaseResult,
                    "htmlFeedback": htmlResults, 
                    "textFeedback": textResults, 
                    "jsonFeedback": json.dumps(jsonResponseData, indent=4, sort_keys=True)}
    return allFeedback

def lambda_handler(event, context):
    method = event.get('httpMethod', {})
    indexPage = getIndexPage()
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": indexPage
        }

    if method == 'POST':
        recResp = json.loads(event.get('body', {}))
        print("Received request")
        print(recResp)
        testUrl = recResp["editable"]["0"].strip()
        hiddenTest = recResp["hidden"]["0"].strip().splitlines()
        shownTest = recResp["shown"]["0"].strip().splitlines()
        userToken = recResp["userToken"].strip()
        #Execute tests
        shownJsonResp = exec_tests(testUrl,shownTest,userToken,False)
        hiddenJsonResp = exec_tests(testUrl,hiddenTest,userToken,True)
        result = shownJsonResp["results"]
        result.extend(hiddenJsonResp["results"])
        jsonResp = {"results": result}
        print(jsonResp)
        #Form feedback
        allFeedback = calcFeedback(jsonResp,userToken)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body":  json.dumps({
                "isComplete": allFeedback["isCorrect"],
                "jsonFeedback": allFeedback["jsonFeedback"],
                "htmlFeedback": allFeedback["htmlFeedback"],
                "textFeedback": allFeedback["textFeedback"]
            })
        }
try:
    import requests
except ImportError:
    from botocore.vendored import requests
import json
import traceback
import logging
import doctest


def lambda_handler(event, context):
    method = event.get('httpMethod', {})

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
                    <div class="md-layout">
                        <div class="md-layout-item md-size-75">
                            <md-field>
                                <label>Enter API Endpoint</label>
                                <md-input v-model="url"></md-input>
                            </md-field>
                            <md-field>
                                <label>Testcases</label>
                                <md-textarea v-model="testCases"></md-textarea>
                            </md-field>
                        </div>
                        <div class="md-layout-item md-size-25">
                            <button class="button" v-on:click="staygo"><span>Submit</span></button>
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
            testCases: "GET, text=madam, response.type, shouldEqual, text/text\\nGET, text=banana, response.body, shouldContain, banana\\nGET, text=banana, response.body, shouldEqual, banana is not a Palindrome\\nGET, text=banana, response.json.anotherResult, shouldEqual, Hey there\\nGET, text=banana, response.json.anotherResult, shouldContain, Hey ",
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
        body: JSON.stringify({shown:{},editable:{0:this.url,1:this.testCases}, hidden:{}})
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
        height:100%
    }
    .md-tab{
        min-height:500px;
    }
    .md-content{
        min-height:500px;
    }
    .output-tab{
        max-height:400px !important;
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
        transform: translate(50%, 100%)
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
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": indexPage
        }

    if method == 'POST':
        bodyContent = event.get('body', {})
        parsedBodyContent = json.loads(bodyContent)
        testUrl = parsedBodyContent["editable"]["0"]
        testCases = parsedBodyContent["editable"]["1"].splitlines()
        jsonResponse = {"results": []}
        for oneTest in testCases:
            partsOfTest = oneTest.split(",")
            partsOfTest = list(map(str.strip, partsOfTest))
            #method, parameters, responseTarget, testMethod, testValue
            #GET, name=abc, response.type, shouldEqual, text/text
            # Define responseTarget
            if(partsOfTest[2].lower() == "response.type"):
                targetStr = "headers['Content-Type']"
            elif(partsOfTest[2].lower() == "response.body"):
                targetStr = "text"
            elif(partsOfTest[2] and partsOfTest[2].lower().find("response.json") !=1 ):
                targetStr = "json()"
            execUrlStr = """requests.{method}(url="{url}?{parameter}")""".format(
                method=partsOfTest[0].lower(),
                url=testUrl,
                parameter=partsOfTest[1])
            urlResponse = eval(execUrlStr)
            resStatusCode = urlResponse.status_code
            execReq = str(eval("urlResponse."+targetStr))
            finalRes = execReq.replace("'",'"').replace('"', '\\"')
            if(targetStr == "json()" and resStatusCode == 200):
                keys = ""
                for key in partsOfTest[2].split(".")[2:]:
                    keys +="[\"{key}\"]".format(key=key)
                temp = "json.loads(\"{received}\"){keys}".format(
                    received=finalRes, 
                    keys=keys)
                finalRes = eval(temp)
            # Define testMethod/operation
            if(partsOfTest[3].lower() == "shouldequal"):
                opStr = "\"{received}\" == \"{testvalue}\"".format(
                    received = finalRes, 
                    testvalue=partsOfTest[4])
            elif(partsOfTest[3].lower() == "shouldcontain"):
                if execReq: #to check if execReq is not None, to prevent exception
                    opStr = "\"{received}\".find('{testValue}') != -1".format(
                        received = finalRes,
                        testValue=partsOfTest[4])
                else:
                    opStr = "False"
            execOpStr = """{operation}""".format(operation=opStr)
            print(execOpStr)
            execOp = str(eval(execOpStr))
            print(execOp)
            jsonResponse["results"].append({"method": partsOfTest[0], 
                                            "parameters": partsOfTest[1], 
                                            "responseTarget": partsOfTest[2],
                                            "testMethod": partsOfTest[3], 
                                            "testValue": partsOfTest[4], 
                                            "receivedValue": execReq, 
                                            "statusCode":resStatusCode, 
                                            "correct": execOp})
            print(jsonResponse)
        jsonResponseData = json.loads(json.dumps(jsonResponse))
        textResults = ""
        resultContent = jsonResponseData.get('results')
        tableContents = ""
        textBackgroundColor = "#ffffff"
        allTestCaseResult = True
        if resultContent:
            for i in range(len(resultContent)):
                methodText = resultContent[i]["method"]
                parameterText = resultContent[i]["parameters"]
                responseTargetText = resultContent[i]["responseTarget"]
                testMethodText = resultContent[i]["testMethod"]
                testValueText = resultContent[i]["testValue"]
                receivedValueText = resultContent[i]["receivedValue"]
                statusCode = resultContent[i]["statusCode"]
                correctText = resultContent[i]["correct"]
                allTestCaseResult = (allTestCaseResult and (correctText == "True"))
                if correctText == "True":
                    textResults = textResults + ("\nHurray! You have passed the test case with"
                                                "status code {statusCode}. {method} call with"
                                                "{parameter} and received {responseTarget} as" 
                                                "{receivedValue} against the expected value" 
                                                "of {testValue}.\n").format(
                                                    statusCode=statusCode,
                                                    method=methodText, 
                                                    parameter=parameterText, 
                                                    responseTarget=responseTargetText, 
                                                    receivedValue=receivedValueText,
                                                    testValue=testValueText)
                    textBackgroundColor = "#b2d8b2" #Green
                else:
                    textResults = textResults + ("\nOh no! Test case failed with" 
                                                "status code {statusCode}. {method} call with"
                                                "{parameter} and received {responseTarget} as" 
                                                "{receivedValue} against the expected value" 
                                                "of {testValue}.\n").format(
                                                    statusCode=statusCode,
                                                    method=methodText, 
                                                    parameter=parameterText, 
                                                    responseTarget=responseTargetText, 
                                                    receivedValue=receivedValueText,
                                                    testValue=testValueText)
                    textBackgroundColor = "#ff9999" #Red
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
            tableContents = """<span class="md-subheading">
                            All tests passed: {allPassed}</span><br/>""".format(
                                allPassed=str(allTestCaseResult)) + tableContents
        textResults = """All tests passed: {allPassed}\n""".format(
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
                                {0}
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
            """.format(tableContents)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body":  json.dumps({
                "isComplete":True,
                "jsonFeedback": json.dumps(jsonResponseData, indent=4, sort_keys=True),
                "htmlFeedback": htmlResults,
                "textFeedback": textResults
            })
        }

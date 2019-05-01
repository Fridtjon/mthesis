package main

import (
	"encoding/json"
	"fmt"
	"strconv"
	"crypto/sha256"
	"errors"
	"os"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
)

// SimpleChaincode example simple Chaincode implementation
type SimpleChaincode struct {
}

// Asset Definitions
// --- Documents ---
type Document struct {
	ObjectType	string	`json:"docType`
	Id			string	`json:"id"`
	//Filename	string 	`json:"filename` // Id is filename
	Hash		string	`json:"hash"`
	Uploader	string	`json:"uploader"` 	// Should point to another struct in the future.
	Creator		string	`json:"creator"`	// This one as well. In a perfect future.
}

// ============================================================================================================================
// Main
// ============================================================================================================================
func main() {
	err := shim.Start(new(SimpleChaincode))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode - %s", err)
	}
}


// ============================================================================================================================
// Init - initialize the chaincode 
//
// Hashchain does not require initialization, so let's run a simple test instead.
//
// Shows off PutState() and how to pass an input argument to chaincode.
// Shows off GetFunctionAndParameters() and GetStringArgs()
// Shows off GetTxID() to get the transaction ID of the proposal
//
// Inputs - Array of strings
//  ["314"]
// 
// Returns - shim.Success or error
// ============================================================================================================================
func (t *SimpleChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("Starting hashchain... :) ")
	funcName, args := stub.GetFunctionAndParameters()
	var number int
	var err error
	txId := stub.GetTxID()
	
	fmt.Println("Init() is running")
	fmt.Println("Transaction ID:", txId)
	fmt.Println("  GetFunctionAndParameters() function:", funcName)
	fmt.Println("  GetFunctionAndParameters() args count:", len(args))
	fmt.Println("  GetFunctionAndParameters() args found:", args)

	// expecting 1 arg for instantiate or upgrade
	if len(args) == 1 {
		fmt.Println("  GetFunctionAndParameters() arg[0] length", len(args[0]))

		// expecting arg[0] to be length 0 for upgrade
		if len(args[0]) == 0 {
			fmt.Println("  Uh oh, args[0] is empty...")
		} else {
			fmt.Println("  Great news everyone, args[0] is not empty")

			// convert numeric string to integer
			number, err = strconv.Atoi(args[0])
			if err != nil {
				return shim.Error("Expecting a numeric string argument to Init() for instantiate")
			}

			// this is a very simple test. let's write to the ledger and error out on any errors
			// it's handy to read this right away to verify network is healthy if it wrote the correct value
			err = stub.PutState("selftest", []byte(strconv.Itoa(number)))
			if err != nil {
				return shim.Error(err.Error())                  //self-test fail
			}
		}
	}

	// showing the alternative argument shim function
	alt := stub.GetStringArgs()
	fmt.Println("  GetStringArgs() args count:", len(alt))
	fmt.Println("  GetStringArgs() args found:", alt)


	fmt.Println("Ready for action")                          //self-test pass
	return shim.Success(nil)
}


// ============================================================================================================================
// Invoke - Our entry point for Invocations
// ============================================================================================================================
func (t *SimpleChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	function, args := stub.GetFunctionAndParameters()
	fmt.Println(" ")
	fmt.Println("starting invoke, for - " + function)

	// Handle different functions
	if function == "init" {                    //initialize the chaincode state, used as reset
		return t.Init(stub)
	} else if function == "read" {             //generic read ledger
		return read(stub, args)
	} else if function == "write" {            //generic writes to ledger
		return write(stub, args)
	} else if function == "init_doc" { // Master: Upload document
		return init_doc(stub, args)
	} else if function == "read_doc" {
		return read_doc(stub, args)
	} else if function == "update_doc" {
		return update_doc(stub, args)
	} else if function == "read_all_docs" {
		return read_all_docs(stub, args)
	} else if function == "pwd" { // Debug function
		return shim.Error(get_pwd())
	}

	// error out
	fmt.Println("Received unknown invoke function name - " + function)
	return shim.Error("Received unknown invoke function name - '" + function + "'")
}


// ============================================================================================================================
// Query - legacy function
// ============================================================================================================================
func (t *SimpleChaincode) Query(stub shim.ChaincodeStubInterface) pb.Response {
	return shim.Error("Unknown supported call - Query()")
}

// Read functions 
func read_doc(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments, " + "Expected 1 but got " + strconv.Itoa(len(args)) + ".\n" + "Usage: get_document <id(filename)>" )
	}
	filename := args[0]
	docAsBytes, err := stub.GetState("d_" + filename)
	if err != nil {
		return shim.Error(err.Error())
	}
	
	return shim.Success(docAsBytes)
}

func read_all_docs(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error

	if len(args) != 0 {
		return shim.Error("Incorrect number of arguments. Expected 0 but got " + strconv.Itoa(len(args)) + ". Usage: read_all_docs")
	}

	var documents []Document
	//coloredMarbleResultsIterator, err := stub.GetStateByPartialCompositeKey("color~name", []string{color})
	resultsIt, err := stub.GetStateByPartialCompositeKey("type~name", []string{"document"})
	if err != nil {
		return shim.Error(err.Error())
	}
	defer resultsIt.Close()
	for resultsIt.HasNext() {
		aKeyValue, err := resultsIt.Next()
		if err != nil {
			return shim.Error(err.Error())
		}
		_, compositeKeyParts, err := stub.SplitCompositeKey(aKeyValue.Key)
		if err != nil {
			return shim.Error(err.Error())
		}

		//what := compositeKeyParts[0]
		name := compositeKeyParts[1] 
		docAsBytes, err := stub.GetState(string(name)) // cast string to string just to be sure its a string
		//return shim.Error("Three: what = " + string(what) + ". name = " + string(name) + ". objectType = " + string(objectType) + ".")
		var document Document
		err = json.Unmarshal(docAsBytes, &document)
		if err != nil {
			return shim.Error("Four: " + err.Error())
		}
		documents = append(documents, document)

	}

	docAsBytes, _ := json.Marshal(documents)
	return shim.Success(docAsBytes)
}


func read(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var key, jsonResp string
	var err error
	fmt.Println("starting read")

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting key of the var to query")
	}


	key = args[0]
	valAsbytes, err := stub.GetState(key)           //get the var from ledger
	if err != nil {
		jsonResp = "{\"Error\":\"Failed to get state for " + key + "\"}"
		return shim.Error(jsonResp)
	}

	fmt.Println("- end read")
	return shim.Success(valAsbytes)                  //send it onward
}


// Write functions

func init_doc(stub shim.ChaincodeStubInterface, args []string) (pb.Response) {
	var err error
	fmt.Println("starting upload_document")

	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments, " + "Expected 3, got " + strconv.Itoa(len(args)) + ".\n" + "Usage: get_doc <id(filename)> <filepath> <uploader>" )
	}

	filename := args[0]
	id := "d_" + filename
	document := args[1]
	uploader := args[2]
	/* Below is an attempt to read a file. It's not possible
		to read files "on the blockchain."

	document, err := read_document(filepath)
	if err != nil {
		return shim.Error("Filepath " + filepath + " gave this error: " + err.Error())
	}
	*/ 
	hash := new_hash(document)
	// Check if exists, need some kind of getter.@

	str := `{
		"docType":"document", 
		"id": "` + id + `", 
		"hash": "` + hash + `", 
		"uploader": "` + uploader + `",
		"creator": "`+ uploader + `"
	}`
	err = stub.PutState(id, []byte(str))
	if err != nil {
		return shim.Error(err.Error())
	}

	//  ==== Index the marble to enable color-based range queries, e.g. return all blue marbles ====
	//  An 'index' is a normal key/value entry in state.
	//  The key is a composite key, with the elements that you want to range query on listed first.
	//  In our case, the composite key is based on indexName~color~name.
	//  This will enable very efficient state range queries based on composite keys matching indexName~color~*
	indexName := "type~name"
	colorNameIndexKey, err := stub.CreateCompositeKey(indexName, []string{"document", id})
	if err != nil {
		return shim.Error(err.Error())
	}
	//  Save index entry to state. Only the key name is needed, no need to store a duplicate copy of the marble.
	//  Note - passing a 'nil' value will effectively delete the key from state, therefore we pass null character as value
	value := []byte{0x00}
	stub.PutState(colorNameIndexKey, value)

	fmt.Println("end init_document")
	return shim.Success(nil)
} 

func update_doc(stub shim.ChaincodeStubInterface, args []string) (pb.Response) {
	var err error
	var document Document
	fmt.Println("starting upload_document")

	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments, " + "Expected 3, got " + strconv.Itoa(len(args)) + ".\n" + "Usage: update_doc <id(filename)> <filepath> <uploader>" )
	}

	filename := args[0]
	id := "d_" + filename
	documentContent := args[1]
	uploader := args[2]

	document, err = get_doc(stub, id)
	if err != nil {
		return shim.Error(err.Error())
	}

	fmt.Println("Updating document with id " + document.Id)

	hash := new_hash(documentContent) 
	str := `{
		"docType":"document",
		"id": "` + id + `",
		"hash": "` + hash + `",
		"uploader": "` + uploader + `",
		"creator": "` + document.Creator + `"
	}`
	err = stub.PutState(id, []byte(str))
	if err != nil {
		return shim.Error(err.Error())
	}

	fmt.Println("end update_doc")
	return shim.Success(nil)
}



// ============================================================================================================================
// write() - genric write variable into ledger
// 
// Shows Off PutState() - writting a key/value into the ledger
//
// Inputs - Array of strings
//    0   ,    1
//   key  ,  value
//  "abc" , "test"
// ============================================================================================================================
func write(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var key, value string
	var err error
	fmt.Println("starting write")

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2. key of the variable and value to set")
	}


	key = args[0]                                   //rename for funsies
	value = args[1]
	err = stub.PutState(key, []byte(value))         //write the variable into the ledger
	if err != nil {
		return shim.Error(err.Error())
	}

	fmt.Println("- end write")
	return shim.Success(nil)
}

// Utilities 


/*
-- Debug functions

*/

func get_pwd() string {
	dir, err := os.Getwd()
		if err != nil {
			err.Error()
		}
	return "pwd:" + dir
}

/*
-- End debug function
*/

// ========================================================================================================================
// New Hash - generates a new sha256 hash from a string. 
// ========================================================================================================================
func new_hash(document string) (string) {
	h := sha256.New()
	h.Write([]byte(document))
	return fmt.Sprintf("%x",h.Sum(nil))
}

// ========================================================================================================================
// Get Doc - Retrieves a document from the ledger. 
// ========================================================================================================================
func get_doc(stub shim.ChaincodeStubInterface, id string) (Document, error) {
	var document Document
	docAsBytes, err := stub.GetState(id)
	if err != nil {
		return document, errors.New("Could not find document with id " + id)
	}

	err = json.Unmarshal(docAsBytes, &document)
	if err != nil {
		return document, errors.New(err.Error())
	}
	//return document, errors.New(string(docAsBytes) + "\n\n-->" + string(document.ObjectType))
	if document.Id != id {
		return document, errors.New("Document does not exists " + document.Id)
	}

	return document, nil
}

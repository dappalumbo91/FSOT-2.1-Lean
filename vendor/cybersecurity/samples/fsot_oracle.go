// FSOT code-genome sample — Go service with safe patterns.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
)

func HashPayload(data []byte) string {
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

func main() {
	fmt.Println(HashPayload([]byte("fsot-tier43")))
}
// Adversarial — data race + unsafe pointer pattern.
package main

import (
	"os/exec"
	"unsafe"
)

func advRace(ch chan int, m map[int]int) {
	go func() { m[1] = 2 }()
	go func() { m[2] = 3 }()
	_ = unsafe.Pointer(&ch)
	exec.Command("sh", "-c", "echo race")
}
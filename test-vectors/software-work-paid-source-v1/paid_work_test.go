package paidwork

import "testing"

func TestPaidWork(t *testing.T) {
	const input = "TOS Native Service paid software work v1"
	if len(input) != 33 {
		t.Fatalf("unexpected committed input length: %d", len(input))
	}
}

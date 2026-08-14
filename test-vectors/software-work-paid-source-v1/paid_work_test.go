package paidwork

import "testing"

func TestPaidWork(t *testing.T) {
	const input = "ATOS Native paid software work v1"
	if len(input) != 33 {
		t.Fatalf("unexpected committed input length: %d", len(input))
	}
}

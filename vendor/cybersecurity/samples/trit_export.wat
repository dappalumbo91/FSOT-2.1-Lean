;; FSOT code-genome sample — WebAssembly text (WAT) trit export.
(module
  (func $fsot_trit_add (export "fsot_trit_add") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add)
  (memory (export "memory") 1)
  (func $fsot_store (export "fsot_store") (param i32 i32)
    local.get 0
    local.get 1
    i32.store align=4))
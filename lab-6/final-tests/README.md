# Final Smoke Test

`final_smoke.dat` is a compact RV32I test program for the final-style checks.

Expected key results:

```text
x3  = 00000001  slt signed
x4  = 00000000  sltu unsigned
x5  = 00000001  slti
x6  = 00000000  sltiu
x7  = 00000001  sltiu with sign-extended immediate
x8  = 0000000f  andi
x9  = 00000055  ori
x10 = 000000aa  xori
x11 = 80000000  slli
x12 = 00000001  srli
x13 = ffffffff  srai
x14 = 00000002  beq taken
x15 = 00000002  bne taken
x16 = 00000002  blt taken
x17 = 00000002  bge taken
x18 = 00000002  bltu taken
x19 = 00000002  bgeu taken
x20 = 00000080  jal link value
x21 = 00000000  skipped after jal
x22 = 00000094  jalr target address
x23 = 00000090  jalr link value
x24 = 00000000  skipped after jalr
x25 = 00000007  reached jalr target
m0  = 00000007  store after jalr target
```

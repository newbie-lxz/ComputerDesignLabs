# Lab-6 Final 验收操作清单

## 1. 验收目标

`final` 验收不是只看学号排序结果，还会检查单周期 CPU 和流水线 CPU 是否真正支持扩展指令。

单周期 CPU 需要覆盖：

```text
slt, sltu,
andi, ori, xori,
srli, srai, slli,
slti, sltiu,
bne, bge, bgeu, blt, bltu,
jalr
```

流水线 CPU 需要覆盖：

```text
slt, sltu,
andi, ori, xori,
srli, srai, slli,
slti, sltiu,
beq, bne, bge, bgeu, blt, bltu,
jal, jalr
```

## 2. 单周期学号排序仿真

进入：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-sc
```

运行：

```powershell
.\build.bat clean
.\build.bat
```

个人学号版本期望输出：

```text
[RESULT] original_sid=13572468
[RESULT] sorted_sid=12345678
[PASS] lab-6 sid sorting simulation passed.
```

## 3. 流水线学号排序仿真

进入：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-pl
```

编译：

```powershell
iverilog -I . -s pl_sid_sort_tb -o pl_sid_sort.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v pl_reg.v plcomp.v pl_sid_sort_tb.v PLCPU.v RF.v
```

运行：

```powershell
vvp pl_sid_sort.out
```

期望输出：

```text
[RESULT] original_sid=13572468
[RESULT] sorted_sid=12345678
[PASS] lab-6 pipeline sid sorting simulation passed.
```

## 4. Final 指令冒烟测试

本目录新增了：

```text
final-tests/final_smoke.dat
```

它会测试：

```text
slt, sltu, slti, sltiu,
andi, ori, xori,
slli, srli, srai,
beq, bne, blt, bge, bltu, bgeu,
jal, jalr
```

### 单周期 final 测试

进入：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-sc
```

编译：

```powershell
iverilog -I . -s sc_final_tb -o sc_final_smoke.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v sccomp.v SCCPU.v RF.v ..\..\final\iverilog-tests\tb\sc_final_tb.v
```

运行：

```powershell
vvp sc_final_smoke.out +IMEM=../final-tests/final_smoke.dat +CYCLES=120
```

### 流水线 final 测试

进入：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-pl
```

编译：

```powershell
iverilog -I . -s pl_final_tb -o pl_final_smoke.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v plcomp.v PLCPU.v pl_reg.v RF.v ..\..\final\iverilog-tests\tb\pl_final_tb.v
```

运行：

```powershell
vvp pl_final_smoke.out +IMEM=../final-tests/final_smoke.dat +CYCLES=220
```

关键期望结果：

```text
[REG] x3=00000001
[REG] x4=00000000
[REG] x5=00000001
[REG] x6=00000000
[REG] x7=00000001
[REG] x8=0000000f
[REG] x9=00000055
[REG] x10=000000aa
[REG] x11=80000000
[REG] x12=00000001
[REG] x13=ffffffff
[REG] x14=00000002
[REG] x15=00000002
[REG] x16=00000002
[REG] x17=00000002
[REG] x18=00000002
[REG] x19=00000002
[REG] x20=00000080
[REG] x21=00000000
[REG] x22=00000094
[REG] x23=00000090
[REG] x24=00000000
[REG] x25=00000007
[MEM] m0=00000007
```

## 5. 上板注意事项

仿真使用：

```text
rv32_sid_sort_sim.dat
```

Vivado ROM IP 使用：

```text
rv32_sid_sort_fpga.coe
```

不要把 `.dat` 直接当作 `.coe` 使用。上板时 `imem` 的 COE 文件应选择：

```text
source-sc/rv32_sid_sort_fpga.coe
```

单周期 Vivado 顶层中应实例化：

```verilog
SCCPU U_SCCPU(...)
```

流水线 Vivado 顶层中应实例化：

```verilog
PLCPU U_PLCPU(...)
```

流水线 CPU 多出的 `mem_r` 可接到一个 `wire memread;`。

## 6. 提交建议

最终提交或展示时建议准备：

```text
1. 单周期 build.bat 通过截图
2. 流水线 pl_sid_sort_tb 通过截图
3. final_smoke 单周期输出截图
4. final_smoke 流水线输出截图
5. 单周期/流水线开发板显示照片
6. Lab6_Report.md
7. QUESTIONS.md 中常见问题的口头回答准备
```

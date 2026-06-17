# Final Experiment 目录说明

本目录是本次 Final 验收实验的完整工程归档，保存了最终使用的单周期 CPU、流水线 CPU 和 Vivado 上板工程。它用于复现实验结果、查看实现代码，以及配合 `final/report.md` 中的问题回答进行验收说明。

## 目录结构

```text
final_experiment/
├── README.md
├── source-sc/
├── source-pl/
└── vivado/
```

## `source-sc/`：单周期 CPU 工程

`source-sc/` 保存单周期 CPU 的 Verilog 源码、学号排序程序和仿真脚本。

主要文件：

| 文件 | 作用 |
| --- | --- |
| `SCCPU.v` | 单周期 CPU 顶层数据通路，连接 PC、RF、ALU、EXT、NPC 等模块 |
| `ctrl.v` | 单周期 CPU 控制器，负责指令译码和控制信号生成 |
| `alu.v` | ALU 运算模块，实现加减、比较、逻辑、移位等运算 |
| `EXT.v` | 立即数扩展模块，生成 I/S/B/U/J 型立即数 |
| `NPC.v` | 下一条 PC 计算模块，处理顺序执行、分支和跳转 |
| `RF.v` | 寄存器堆 |
| `dm.v` | 数据存储器 |
| `im.v` | 指令存储器 |
| `PC.v` | PC 寄存器 |
| `sccomp.v` | 单周期 CPU 组合顶层 |
| `sccomp_tb.v` | 学号排序仿真 testbench |
| `rv32_sid_sort_sim.asm` | 学号排序汇编程序 |
| `rv32_sid_sort_sim.dat` | 学号排序机器码 |
| `rv32_sid_sort_fpga.coe` | 上板指令存储器初始化文件 |
| `build.bat` | Windows 一键构建和运行脚本 |
| `build.py` | 构建脚本 |
| `Makefile` | Linux/macOS 构建入口 |

当前学号排序结果：

```text
original_sid = 20243021
sorted_sid   = 00122234
```

Windows 下运行：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\final\final_experiment\source-sc
.\build.bat clean
.\build.bat
```

成功时应看到：

```text
[RESULT] original_sid=20243021
[RESULT] sorted_sid=00122234
[PASS] lab-6 sid sorting simulation passed.
```

也可以使用 Final 测试模板运行 30 条指令测试：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\final\final_experiment\source-sc
iverilog -I . -s sc_final_tb -o sc_test30.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v sccomp.v SCCPU.v RF.v ..\..\iverilog-tests\tb\sc_final_tb.v
vvp sc_test30.out +IMEM=../../../CODExp/testcode/task/Test_30_Instr.dat +CYCLES=200
```

## `source-pl/`：流水线 CPU 工程

`source-pl/` 保存流水线 CPU 的 Verilog 源码、学号排序程序和仿真文件。

主要文件：

| 文件 | 作用 |
| --- | --- |
| `PLCPU.v` | 流水线 CPU 顶层，包含 IF/ID/EX/MEM/WB 数据通路、stall 和 flush 逻辑 |
| `pl_reg.v` | 通用流水线段寄存器 |
| `ctrl.v` | 流水线 CPU 控制器 |
| `alu.v` | ALU 运算模块 |
| `EXT.v` | 立即数扩展模块 |
| `NPC.v` | 下一条 PC 计算模块 |
| `RF.v` | 寄存器堆 |
| `dm.v` | 数据存储器 |
| `im.v` | 指令存储器 |
| `PC.v` | PC 寄存器 |
| `plcomp.v` | 流水线 CPU 组合顶层 |
| `plcomp_tb.v` | 基础流水线仿真 testbench |
| `pl_sid_sort_tb.v` | 流水线学号排序 testbench |
| `rv32_sid_sort_sim.dat` | 学号排序机器码 |
| `rv32_pl_sim.dat` | 基础流水线测试机器码 |
| `build.bat` | Windows 构建脚本 |
| `build.py` | 构建脚本 |
| `Makefile` | Linux/macOS 构建入口 |

运行流水线学号排序测试：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\final\final_experiment\source-pl
iverilog -I . -s pl_sid_sort_tb -o pl_sid_sort.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v pl_reg.v plcomp.v pl_sid_sort_tb.v PLCPU.v RF.v
vvp pl_sid_sort.out
```

成功时应看到：

```text
[RESULT] original_sid=20243021
[RESULT] sorted_sid=00122234
[PASS] lab-6 pipeline sid sorting simulation passed.
```

运行 Final 30 条指令测试：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\final\final_experiment\source-pl
iverilog -I . -s pl_final_tb -o pl_test30.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v plcomp.v PLCPU.v pl_reg.v RF.v ..\..\iverilog-tests\tb\pl_final_tb.v
vvp pl_test30.out +IMEM=../../../CODExp/testcode/task/Test_30_Instr.dat +CYCLES=300
```

## `vivado/`：上板工程

`vivado/` 保存 Vivado 2017.4 上板工程。本次使用的工程目录为：

```text
vivado/final_sc_board_20243021/
```

用途：

- 生成 FPGA bitstream。
- 将排序程序写入指令存储器 IP。
- 在 Nexys4 DDR / Nexys A7 开发板上显示原始学号和排序结果。

上板前需要确认：

1. Vivado 工程中使用的 CPU 顶层和约束文件与开发板匹配。
2. 指令存储器初始化文件使用当前学号对应的 `.coe`。
3. bitstream 生成成功后再连接开发板并 Program Device。

本次开发板显示结果：

```text
原始学号：20243021
排序结果：00122234
```

## 生成文件说明

目录中可能存在以下仿真生成文件：

- `*.out`：`iverilog` 编译输出。
- `*.vcd`：波形文件。
- Vivado 工程中的 `*.runs/`、`*.cache/`、`*.hw/` 等生成目录。

这些文件用于复现实验或查看波形，不是手写源码。若只关注代码实现，重点查看 `source-sc/*.v`、`source-pl/*.v`、汇编/机器码文件和 Vivado 工程源文件即可。

## 与报告的对应关系

`final/report.md` 中的主要内容与本目录对应如下：

- 第 2 章测试截图对应 `source-sc/`、`source-pl/` 的仿真输出。
- 第 3 章开发板照片对应 `vivado/` 工程上板结果。
- 第 5 章问题回答对应 `source-sc/` 和 `source-pl/` 中的实现代码。

因此，验收时可以先看 `final/report.md`，需要追代码时再进入本目录查看具体实现。


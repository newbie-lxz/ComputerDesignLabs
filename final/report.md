# Final 验收实验报告

李熙正   2024302181141  



## 1. 实验目标

本实验在 Lab-6 的基础上完成 RISC-V CPU 的扩展与验收，主要内容包括：

1. 在单周期 CPU 中补充新增指令，使其可以运行 30 条指令测试和学号排序程序。
2. 在流水线 CPU 中补充同样的指令支持，并处理数据冲突和控制冲突。
3. 使用 Icarus Verilog 跑通四个验收测试用例。
4. 使用 Vivado 生成 bitstream，并在开发板上显示原始学号和排序结果。
5. 生成代码 diff 报告，说明相对原始代码修改了哪些文件。

实验环境：

- 仿真工具：Icarus Verilog
- 综合与上板工具：Vivado 2017.4
- FPGA 开发板：Nexys A7 / Nexys4 DDR，Artix-7 系列
- 单周期源码目录：`lab-6/source-sc`
- 流水线源码目录：`lab-6/source-pl`
- Final 测试目录：`final/iverilog-tests`

## 2. 前四个测试用例结果

### 2.1 测试 1：单周期 CPU 运行 `Test_30_Instr.dat`

命令：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-sc
iverilog -I . -s sc_final_tb -o sc_test30.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v sccomp.v SCCPU.v RF.v ..\..\final\iverilog-tests\tb\sc_final_tb.v
vvp sc_test30.out +IMEM=../../CODExp/testcode/task/Test_30_Instr.dat +CYCLES=200
```

关键结果示例：

```text
x5  = 98763dcc
x7  = 00001236
x9  = 0000000c
x10 = 00000dd2
mem[0] = 0000000c
mem[1] = 98765001
mem[2] = 00001236
```

![单周期 Test_30_Instr 仿真结果 - 寄存器与前段内存](<report-assets/屏幕截图 2026-06-16 183811.png>)

![单周期 Test_30_Instr 仿真结果 - 内存续图 1](<report-assets/屏幕截图 2026-06-16 183823.png>)

![单周期 Test_30_Instr 仿真结果 - 内存续图 2](<report-assets/屏幕截图 2026-06-16 183844.png>)

### 2.2 测试 2：流水线 CPU 运行 `Test_30_Instr.dat`

命令：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-pl
iverilog -I . -s pl_final_tb -o pl_test30.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v plcomp.v PLCPU.v pl_reg.v RF.v ..\..\final\iverilog-tests\tb\pl_final_tb.v
vvp pl_test30.out +IMEM=../../CODExp/testcode/task/Test_30_Instr.dat +CYCLES=300
```

关键结果示例：

```text
x5  = 98763dcc
x7  = 00001236
x9  = 0000000c
x10 = 00000dd2
mem[0] = 0000000c
mem[1] = 98765001
mem[2] = 00001236
```

关键结果与单周期版本保持一致，说明流水线 CPU 在处理控制信号传递、暂停和冲刷后能够正确执行 30 条指令测试。

![流水线 Test_30_Instr 仿真结果 - 执行输出](<report-assets/屏幕截图 2026-06-16 184021.png>)

![流水线 Test_30_Instr 仿真结果 - 寄存器与内存](<report-assets/屏幕截图 2026-06-16 184035.png>)

![流水线 Test_30_Instr 仿真结果 - 内存续图](<report-assets/屏幕截图 2026-06-16 184047.png>)

### 2.3 测试 3：单周期 CPU 运行学号排序程序

命令：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-sc
.\build.bat clean
.\build.bat
```

关键结果：

```text
[RESULT] original_sid=20243021
[RESULT] sorted_sid=00122234
[PASS] lab-6 sid sorting simulation passed.
```

![单周期学号排序仿真通过](<report-assets/屏幕截图 2026-06-16 164306.png>)

### 2.4 测试 4：流水线 CPU 运行学号排序程序

命令：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs\lab-6\source-pl
iverilog -I . -s pl_sid_sort_tb -o pl_sid_sort.out alu.v ctrl.v dm.v EXT.v im.v NPC.v PC.v pl_reg.v plcomp.v pl_sid_sort_tb.v PLCPU.v RF.v
vvp pl_sid_sort.out
```

关键结果：

```text
[RESULT] original_sid=20243021
[RESULT] sorted_sid=00122234
[PASS] lab-6 pipeline sid sorting simulation passed.
```

![流水线学号排序仿真通过](<report-assets/屏幕截图 2026-06-16 164323.png>)

## 3. 开发板运行结果

Vivado 工程成功完成综合、实现和 bitstream 生成。

![Vivado bitstream 生成成功](<report-assets/屏幕截图 2026-06-16 175406.png>)

开发板显示规则：

- 显示原始学号：`20243021`
- 按按钮或切换显示选择后，显示排序结果：`00122234`

开发板原始学号显示照片：

![开发板显示原始学号 20243021](<report-assets/a51021f312c9f1c012568d9ae292614d_720.jpg>)

开发板排序结果显示照片：

![开发板显示排序结果 00122234](<report-assets/ca80adb6c2ffc7122349404b975f8570_720.jpg>)

## 4. 指令说明

| 类别 | 指令 | 作用 |
| --- | --- | --- |
| R 型运算 | `add`、`sub`、`slt`、`sltu` | 寄存器之间的加减和比较 |
| I 型运算 | `addi`、`slti`、`sltiu` | 寄存器和立即数运算 |
| 逻辑运算 | `andi`、`ori`、`xori` | 位与、位或、位异或 |
| 移位运算 | `slli`、`srli`、`srai` | 左移、逻辑右移、算术右移 |
| 分支指令 | `beq`、`bne`、`blt`、`bge`、`bltu`、`bgeu` | 根据比较结果选择是否跳转 |
| 跳转指令 | `jal`、`jalr` | 函数调用、返回和无条件跳转 |
| 访存指令 | `lw`、`sw` | 数据存储器读写 |
| 高位立即数 | `lui` | 构造高 20 位立即数 |

学号排序程序主要依赖比较、移位、分支和跳转指令。排序时将 8 位学号按 BCD 风格放入一个 32 位寄存器，每 4 bit 表示一个十进制数字，例如：

```text
20243021 -> 0x20243021
排序后 -> 0x00122234
```

排序程序会把原始学号写入 `mem[0x180]`，把排序结果写入 `mem[0x184]`。

## 5. 问题回答

### 5.1 运算指令 `add rd, rs1, rs2` 的实现原理

本节选取排序程序中真实执行的 `add x2, x2, x3` 作为例子说明。它的作用不是单纯做一个演示加法，而是在构造学号 BCD 编码时，把已经移位好的高位部分和低位部分合并到 `x2`，随后再通过 `sw x2, 0x180(x0)` 写入数据存储器，作为原始学号显示和验收结果。

#### 5.1.1 程序中真实使用的位置

排序程序先用 `addi` 写入若干十六进制数字，再用 `slli` 把它们移动到对应的 4 bit 位置。第 86 行的 `add x2, x2, x3` 把两段学号合并，因此它是排序程序真正依赖的 R 型运算指令。

![排序程序中真实使用 add](<report-assets/屏幕截图 2026-06-17 191519.png>)

#### 5.1.2 指令字段拆分

`add` 属于 R 型指令。CPU 取到 32 位指令后，在 `SCCPU.v` 中直接拆出各字段：`Op=inst_in[6:0]` 用于判断大类，`Funct7` 和 `Funct3` 用于区分同一类中的具体运算，`rs1`、`rs2` 是两个源寄存器编号，`rd` 是目的寄存器编号。对 `add x2, x2, x3` 而言，`rs1=x2`、`rs2=x3`、`rd=x2`。

![SCCPU 中 rs1 rs2 rd 字段拆分](<report-assets/屏幕截图 2026-06-17 190103.png>)

#### 5.1.3 控制器译码

控制器在 `ctrl.v` 中看到 `opcode=7'b0110011` 后进入 R 型指令分支，并继续用 `{Funct7, Funct3}` 判断具体指令。当组合为 `{7'b0000000, 3'b000}` 时，控制器设置 `ALUOp = ALUOp_add`。同时 R 型运算需要写回寄存器，因此 `RegWrite=1`；它不访问数据存储器，所以 `MemWrite=0`；它使用两个寄存器作为 ALU 输入，所以 `ALUSrc=0`；写回数据来自 ALU，所以 `WDSel=FromALU`。

![ctrl 中 add 的控制器译码](<report-assets/屏幕截图 2026-06-17 190219.png>)

`ALUOp_add` 和 `WDSel_FromALU` 是控制信号编码。前者告诉 ALU 执行加法，后者告诉写回多路选择器使用 ALU 结果。

![ALUOp_add 宏定义](<report-assets/屏幕截图 2026-06-17 185832.png>)

![WDSel_FromALU 宏定义](<report-assets/屏幕截图 2026-06-17 185943.png>)

#### 5.1.4 读寄存器与选择 ALU 输入

寄存器堆 `RF` 根据 `rs1`、`rs2` 读出两个操作数，输出为 `RD1` 和 `RD2`。在本例中就是读出 `x2` 和 `x3` 的值。`add` 不是立即数运算，所以 `ALUSrc=0`，`assign B = (ALUSrc) ? immout : RD2;` 会选择 `RD2` 作为 ALU 的 B 输入。ALU 的 A 输入没有单独写成 `assign A = RD1`，而是在例化时直接通过 `.A(RD1)` 连接。

![SCCPU 中 ALU 第二输入选择](<report-assets/09_sc_alusrc_mux.png>)

![SCCPU 中寄存器堆读取和 ALU 例化](<report-assets/10_sc_rf_alu_instance.png>)

#### 5.1.5 ALU 执行加法

ALU 收到 `ALUOp_add` 后执行 `C = A + B`。结合前面的连线可知，`A` 实际是 `RD1`，`B` 实际是 `RD2`，所以 `add x2, x2, x3` 的执行结果就是 `x2 + x3`，并输出到 `aluout`。

![ALU 中 add 的实现](<report-assets/屏幕截图 2026-06-17 190259.png>)

#### 5.1.6 写回与 PC 更新

`add` 的结果来自 ALU，因此 `WDSel_FromALU` 使写回数据 `WD` 选择 `aluout`。寄存器堆在时钟边沿根据 `RegWrite=1` 将 `WD` 写入 `rd`，也就是写回 `x2`。由于 `add` 不是跳转或分支指令，`NPCOp` 选择普通顺序执行路径，下一条 PC 为 `PC+4`。

![SCCPU 中 ALU 结果写回](<report-assets/屏幕截图 2026-06-17 190329.png>)

![NPC 中 PC+4 与分支目标选择](<report-assets/11_sc_npc_pcplus4_branch.png>)

综上，`add x2, x2, x3` 的完整数据通路是：取指得到指令，拆出 `rs1/rs2/rd`，控制器译码得到 `ALUOp_add` 和 `RegWrite`，寄存器堆读出 `x2/x3`，ALU 完成加法，结果通过写回选择器写回 `x2`，PC 顺序加 4。

### 5.2 分支指令 `beq rs1, rs2, label` 的实现原理

本节选取排序程序中的 `beq x3, x11, checkswap` 说明分支指令。它出现在内层循环入口，用来判断循环变量 `j` 是否已经等于 8。如果相等，说明内层循环结束，跳到 `checkswap` 判断本轮是否需要交换；如果不相等，则继续执行内层循环体。

#### 5.2.1 程序中真实使用的位置

此处 `x3` 保存当前 `j`，`x11` 保存常数 8。`beq x3, x11, checkswap` 的语义是：若 `x3 == x11`，则跳转到 `checkswap`；否则顺序执行下一条指令。

![排序程序中真实使用 beq](<report-assets/屏幕截图 2026-06-17 203210.png>)

#### 5.2.2 字段拆分与立即数生成

`beq` 属于 B 型指令，仍然需要读取两个源寄存器，因此 `rs1` 和 `rs2` 的拆分方式与 R 型指令相同。但 B 型指令没有写回寄存器，跳转目标由 B 型立即数决定。`SCCPU.v` 先把 B 型立即数字段拼成 `bimm`，随后 `EXT.v` 对它进行符号扩展，并在最低位补 0，得到按 2 字节对齐的分支偏移量。

![SCCPU 中 rs1 rs2 字段拆分](<report-assets/屏幕截图 2026-06-17 190103.png>)

![EXT 中 B 型立即数扩展](<report-assets/13_sc_ext_btype.png>)

#### 5.2.3 控制器译码与分支条件判断

控制器看到 `opcode=7'b1100011` 后进入 branches 分支，并设置 `EXTOp = EXT_CTRL_BTYPE`。当 `Funct3=3'b000` 时，说明具体指令是 `beq`。本实现让 ALU 执行减法比较：`ALUOp = ALUOp_sub`。如果两个寄存器相等，`A-B` 的结果为 0，ALU 的 `Zero` 信号为 1，于是 `NPCOp` 选择 `NPC_BRANCH`；否则 `NPCOp` 选择 `NPC_PLUS4`。

![ctrl 中 beq 的控制器译码](<report-assets/12_sc_beq_ctrl_decode.png>)

#### 5.2.4 ALU 比较与 `Zero` 信号

ALU 中 `ALUOp_sub` 对两个源操作数做减法。对 `beq` 来说，真正关心的不是减法结果写回，而是结果是否为 0。`Zero` 的生成逻辑中，普通比较使用 `(C == 32'b0)`，因此 `x3 - x11 == 0` 时 `Zero=1`，表示分支成立。

![ALU 中 sub 比较实现](<report-assets/14_sc_alu_sub_compare.png>)

![ALU 中 Zero 信号生成](<report-assets/15_sc_alu_zero.png>)

#### 5.2.5 PC 跳转实现

`NPC.v` 根据 `NPCOp` 选择下一条 PC。若 `beq` 成立，控制器给出 `NPC_BRANCH`，下一条 PC 为 `PC + IMM`，也就是跳到 `checkswap`；若不成立，则 `NPC_PLUS4`，继续执行下一条顺序指令。

![NPC 中分支跳转目标选择](<report-assets/16_sc_npc_branch_select.png>)

综上，`beq x3, x11, checkswap` 的完整执行路径是：拆出 `rs1=x3`、`rs2=x11` 和 B 型立即数，控制器识别 `beq`，ALU 做 `x3-x11`，根据 `Zero` 判断是否相等，最后由 `NPC` 选择 `PC+IMM` 或 `PC+4`。

### 5.3 单周期 CPU 与流水线 CPU 的区别

单周期 CPU 中，一条指令必须在一个时钟周期内完成取指、译码、执行、访存和写回，因此控制逻辑直观，但周期长度必须覆盖最慢指令。流水线 CPU 将一条指令拆成 IF、ID、EX、MEM、WB 多个阶段，不同指令可以同时处在不同阶段中。这样吞吐率更高，但需要保存阶段之间的信息，并处理数据冲突和控制冲突。

#### 5.3.1 流水线额外增加的段寄存器

流水线 CPU 相比单周期 CPU，最关键的新增结构是段寄存器。通用模块 `pl_reg` 在时钟边沿把输入锁存到输出，复位时输出清零。各级流水段通过不同宽度的 `pl_reg` 保存当前阶段产生的数据和控制信号。

![通用段寄存器模块 pl_reg](<report-assets/17_pl_reg_module.png>)

本设计中主要段寄存器如下：

| 段寄存器 | 保存内容 | 作用 |
| --- | --- | --- |
| `IF_ID` | 当前 PC 和取到的指令 | 把取指结果送入译码阶段 |
| `ID_EX` | `rd/rs1/rs2`、立即数、`RD1/RD2`、控制信号、原始指令 | 把译码结果送入执行阶段 |
| `EX_MEM` | ALU 结果、写存储器数据、目的寄存器、访存和写回控制信号 | 把执行结果送入访存阶段 |
| `MEM_WB` | ALU 结果、数据存储器读出值、目的寄存器、写回控制信号 | 把访存结果送入写回阶段 |

`IF_ID` 保存 IF 阶段产生的 PC 和指令。这里还处理了 `stall` 和 `control_flush`：暂停时保持原值，冲刷时写入 0。

![IF_ID 段寄存器](<report-assets/18_pl_if_id.png>)

`ID_EX` 保存译码阶段读出的寄存器数据、立即数和后续阶段需要的控制信号。它是流水线中信息最多的段寄存器之一，因为 EX 阶段既需要操作数，也需要 ALU、分支、写回等控制信号。

![ID_EX 段寄存器](<report-assets/19_pl_id_ex.png>)

`EX_MEM` 保存 EX 阶段的 ALU 结果和即将写入数据存储器的数据，同时把控制信号继续传给 MEM 阶段。

![EX_MEM 段寄存器](<report-assets/20_pl_ex_mem.png>)

`MEM_WB` 保存 MEM 阶段的结果。写回阶段根据 `WB_WDSel` 决定写回 ALU 结果、内存读出数据还是 PC 相关结果。

![MEM_WB 段寄存器](<report-assets/21_pl_mem_wb.png>)

#### 5.3.2 单周期和流水线执行同一条指令的差别

以 `add` 为例，单周期 CPU 在一个周期内完成寄存器读取、ALU 加法、结果写回和 PC 更新。流水线 CPU 则把这些动作分布到多个阶段：IF 取指，ID 读寄存器和译码，EX 做 ALU 运算，MEM 传递结果，WB 写回寄存器。单条指令从开始到结束经历多个周期，但多条指令可以重叠执行，所以整体吞吐率更高。

### 5.4 流水线冲突处理

流水线执行时，后一条指令可能需要前一条尚未写回的结果，或者分支跳转后已经取到的顺序指令不应继续执行。本实验的流水线 CPU 通过 `stall` 和 `control_flush` 处理这些情况。

#### 5.4.1 数据冲突和暂停

代码中定义了 `rs1_hazard` 和 `rs2_hazard`。如果当前译码阶段指令的 `rs1` 或 `rs2` 不是 `x0`，并且它与 EX、MEM、WB 阶段中将要写回的 `rd` 相同，就认为存在 RAW 数据相关。此时 `stall=1`，`PC_next` 保持 `PC_out`，让取指位置不前进。

![流水线 RAW 冲突检测和 stall 生成](<report-assets/22_pl_hazard_stall.png>)

#### 5.4.2 stall 和 flush 对段寄存器的影响

暂停不是让所有流水段停止。`IF_ID_in = stall ? IF_ID_out : ...` 表示发生 `stall` 时 IF/ID 保持原值，使当前译码指令不要被覆盖。`ID_EX_in = (stall || control_flush) ? 194'b0 : ID_EX_raw_in` 表示发生暂停或冲刷时向 ID/EX 插入空操作，避免错误控制信号继续向后传播。

![stall 和 flush 对 IF_ID、ID_EX 的影响](<report-assets/23_pl_stall_flush_regs.png>)

#### 5.4.3 数据转发情况

从当前代码看，ALU 的输入主要来自 `EX_RD1` 和 `EX_RD2`，再由 `EX_ALUSrc` 决定 B 输入选择寄存器值还是立即数。代码中没有完整的 `ForwardA/ForwardB` 多路选择器，也没有把 EX/MEM 或 MEM/WB 的结果直接旁路回 ALU 输入。因此本实现主要依靠 `stall` 暂停来规避 RAW 冲突，而不是依靠完整的数据前递网络。

![流水线 ALU 输入路径](<report-assets/24_pl_alu_input_path.png>)

#### 5.4.4 控制冲突处理

分支或跳转会改变 PC，导致已经取到的顺序路径指令可能无效。代码中用 `control_flush = (EX_NPCOp != NPC_PLUS4)` 判断是否发生控制流改变。若需要冲刷，IF/ID 输入被置 0，ID/EX 也会插入 0，从而清除错误路径上的指令和控制信号。

![控制冲突 control_flush 判断](<report-assets/25_pl_control_flush.png>)

![flush 对流水线寄存器输入的影响](<report-assets/26_pl_flush_regs.png>)

因此，本流水线 CPU 的冲突处理思路可以概括为：数据相关时暂停 PC 和 IF/ID，并向 ID/EX 插入 bubble；控制流改变时冲刷错误路径指令；由于没有完整前递网络，正确性主要依赖 stall/flush 保证。

## 6. `jalr` 返回 `swap` 子过程的原理

学号排序程序中使用 `swap` 子过程交换两个 BCD 数字位置。主程序在需要交换时执行：

```asm
jal x1, swap
```

在当前排序程序中，调用点位于 `rv32_sid_sort_sim.asm` 第 116 行：

```asm
116: jal     x1, swap
117: incrLoop1:
```

`jal x1, swap` 完成两件事：第一，把下一条指令地址 `PC+4` 写入 `x1`；第二，把 PC 改成 `swap` 标签所在地址。因此，`x1` 中保存的就是 `swap` 执行完成后应该返回的位置，也就是第 117 行 `incrLoop1`。

`swap` 子过程最后执行：

```asm
157: jalr    x0, x1, 0
```

`jalr` 的跳转目标计算规则为：

```text
PC = (rs1 + imm) & 0xfffffffe
```

在 `jalr x0, x1, 0` 中，`rs1=x1`，`imm=0`，所以新的 PC 等于 `x1` 中保存的返回地址，并清除最低位以保证地址对齐。因此程序会从 `swap` 跳回 `incrLoop1` 继续执行外层循环。

同时，`rd=x0` 表示不保存新的链接地址。虽然控制器对 `jalr` 设置了写回路径，但写入 `x0` 不会改变有效寄存器，因为 `x0` 恒为 0。所以这条指令只完成“返回”，不会覆盖原来的返回地址。

对应 CPU 实现如下：

- `ctrl.v` 中 `jal` 设置 `RegWrite=1`、`EXTOp=JTYPE`、`NPCOp=NPC_JUMP`、`WDSel=WDSel_FromPC`，即保存 `PC+4` 并跳转到目标地址。
- `ctrl.v` 中 `jalr` 设置 `RegWrite=1`、`ALUSrc=1`、`EXTOp=ITYPE`、`NPCOp=NPC_JALR`、`WDSel=WDSel_FromPC`。
- `SCCPU.v` 中 `WDSel_FromPC` 对应 `WD <= PC_out + 4`，用于把返回地址写入 `x1`。
- `NPC.v` 中 `NPC_JALR` 对应 `NPC = (RS1 + IMM) & 32'hffff_fffe`，用于根据 `x1` 计算返回 PC。

因此，`jal x1, swap` 和 `jalr x0, x1, 0` 共同实现了子过程调用与返回：前者保存返回地址并进入 `swap`，后者读取 `x1` 中的返回地址并跳回调用点之后继续执行。

## 7. diff

使用工具生成 diff：

```powershell
cd D:\lxz_whu\ComputerDesign\ComputerDesignLabs
python .\tools\generate_verilog_diff_report.py --student-sc .\lab-6\source-sc --student-pl .\lab-6\source-pl --out .\diff-report
```

Diff 网页截图如下，只展示文件列表和每个文件修改行数，不展开具体代码：

![diff 修改文件统计截图](<report-assets/屏幕截图 2026-06-17 114344.png>)

## 8. 实验总结

本次实验完成了单周期 CPU 和流水线 CPU 的指令扩展，并通过了四个验收测试：单周期 30 条指令测试、流水线 30 条指令测试、单周期学号排序测试、流水线学号排序测试。排序程序能够正确输出：

```text
original_sid = 20243021
sorted_sid   = 00122234
```

开发板上也成功显示了原始学号和排序后的结果。









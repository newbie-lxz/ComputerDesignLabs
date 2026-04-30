# SCCPU 连线对照说明（基于 `SCCPU.v`）

本文按源码 [SCCPU.v](./source-sc/SCCPU.v) 与顶层 [sccomp.v](./source-sc/sccomp.v) 对照，解释图中每个关键变量对应的连线关系：**从哪里来、到哪里去、作用是什么**。

## 1. 关键连线总表

| 变量 | 来源 | 去向 | 作用 |
|---|---|---|---|
| `PC_out` | `PC` 模块输出 | `IM.addr`、`NPC.PC`、`WD`选择逻辑中的`PC_out+4` | 当前指令地址 |
| `NPC` | `NPC` 模块输出 | `PC.NPC` | 下一条指令地址 |
| `inst_in` | `IM.dout` | 被拆分为控制字段、寄存器字段、立即数字段 | 指令总线 |
| `Op/Funct7/Funct3` | `inst_in`位段 | `CTRL`输入 | 指令译码字段 |
| `rs1/rs2/rd` | `inst_in[19:15]/[24:20]/[11:7]` | `RF.A1/A2/A3` | 寄存器读写地址 |
| `iimm/simm/bimm/uimm/jimm` | `inst_in`按类型拼接 | `EXT`输入 | 各类立即数字段 |
| `EXTOp` | `CTRL`输出 | `EXT.EXTOp` | 控制立即数扩展类型 |
| `immout` | `EXT`输出 | `ALU B`选择器、`NPC.IMM` | 扩展后的32位立即数 |
| `RegWrite` | `CTRL`输出 | `RF.RFWr` | 寄存器写使能 |
| `RD1` | `RF`输出 | `ALU.A` | ALU输入A |
| `RD2` | `RF`输出 | `ALU.B`候选、`Data_out` | ALU输入B候选/存储器写数据源 |
| `ALUSrc` | `CTRL`输出 | `B=(ALUSrc)?immout:RD2` | ALU输入B选择 |
| `B` | 组合逻辑结果 | `ALU.B` | ALU最终B输入 |
| `ALUOp` | `CTRL`输出 | `ALU.ALUOp` | ALU运算控制 |
| `aluout` | `ALU.C`输出 | `Addr_out`、`DM.addr`、`WD`候选 | ALU结果/数据存储器地址 |
| `Zero` | `ALU`输出 | `CTRL.Zero` | 分支条件标志 |
| `NPCOp` | `CTRL`输出 | `NPC.NPCOp` | 下一PC生成控制 |
| `mem_w` | `CTRL.MemWrite` | `DM.DMWr` | 数据存储器写使能 |
| `Data_out` | `RD2`直连 | `DM.din` | 写入DM的数据 |
| `Data_in` | `DM.dout` | `WD`候选 | 从DM读回的数据 |
| `WDSel` | `CTRL`输出 | `WD`多路选择逻辑 | 回写数据来源选择 |
| `WD` | `always @*`多路选择结果 | `RF.WD` | 最终回写寄存器的数据 |
| `Addr_out` | `aluout` | 顶层连到 `DM.addr` | 数据存储器地址输出 |
| `reg_sel/reg_data` | 调试端口 | `RF` | 调试读取寄存器数据 |

## 2. 图中两处 `Instruction[...]` 的正确理解

- `CTRL`旁边的 `Instruction [***]`：不是单一连续位段，而是 `inst_in` 拆出的 `Op/Funct3/Funct7` 三组字段输入控制器。
- `EXT`旁边的 `Instruction [##]`：对应 `iimm/simm/bimm/uimm/jimm` 五种立即数字段输入扩展器。

## 3. 回写路径（WD）对应图中多路复用器

`WD`由 `WDSel` 控制选择：

- `WDSel_FromALU`：`WD = aluout`
- `WDSel_FromMEM`：`WD = Data_in`
- `WDSel_FromPC`：`WD = PC_out + 4`

这就是图中“ALU/DM/PC+4 -> RegFile写回口”的那组回写连线。

## 4. 顶层模块中的 IM/DM 外围连线（`sccomp.v`）

- `im.addr = PC[31:2]`，`im.dout -> SCCPU.inst_in`
- `SCCPU.mem_w -> dm.DMWr`
- `SCCPU.Addr_out -> dm.addr`
- `SCCPU.Data_out -> dm.din`
- `dm.dout -> SCCPU.Data_in`

## 5. 当前源码中“已声明但未参与主通路”的信号

在 `SCCPU.v` 里，下列信号目前未参与后续功能连线：

- 有赋值但未使用：`Imm12`、`IMM`
- 已声明但未使用：`Imm32`、`A3`、`iimm_shamt`

画图时可标注为“保留/未使用信号”，避免与主数据通路混淆。

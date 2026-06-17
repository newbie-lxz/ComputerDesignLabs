# Final 目录说明

本目录用于保存本次计算机设计 Final 验收相关材料，包括验收报告、报告图片、最终测试用例、原理问题说明，以及本次实验使用的源码归档。

## 目录结构

```text
final/
├── README.md
├── QUESTIONS.md
├── report.md
├── report-assets/
├── iverilog-tests/
└── final_experiment/
```

## 文件和子目录说明

### `report.md`

最终实验报告。报告中包含以下内容：

- 前四个验收测试用例的运行结果截图。
- FPGA 开发板运行结果照片。
- 新增指令说明。
- `add` 运算指令的执行过程分析。
- `beq` 分支指令的执行过程分析。
- 单周期 CPU 和流水线 CPU 的区别。
- 流水线段寄存器、数据冲突、stall、flush 等实现说明。
- Verilog diff 报告截图。

报告中的图片均使用相对路径引用 `report-assets/`，因此上传到 GitHub 后应与 `report-assets/` 一起保留。

### `report-assets/`

实验报告使用的所有图片资源，主要包括：

- 单周期 CPU 运行 `Test_30_Instr.dat` 的结果截图。
- 流水线 CPU 运行 `Test_30_Instr.dat` 的结果截图。
- 单周期 CPU 运行学号排序程序的结果截图。
- 流水线 CPU 运行学号排序程序的结果截图。
- Vivado bitstream 生成成功截图。
- 开发板显示原始学号和排序后学号的照片。
- `add`、`beq`、流水线段寄存器、冲突处理等代码截图。
- diff 修改文件统计截图。

修改或移动报告时，不要删除该目录，否则 `report.md` 中的图片会失效。

### `QUESTIONS.md`

Final 原理理解问题集合。内容覆盖：

- 运算指令执行过程。
- 分支和跳转指令执行过程。
- 单周期 CPU 与流水线 CPU 的区别。
- 流水线段寄存器、数据冒险、控制冒险、flush/stall 等问题。

报告第 5、6 章中的问题回答可用于应对这些验收提问。

### `iverilog-tests/`

Final 验收用的 `iverilog` 测试目录。

```text
iverilog-tests/
├── README.md
├── tb/
│   ├── sc_final_tb.v
│   └── pl_final_tb.v
└── tests/
    ├── expected_results.json
    ├── sc/
    └── pl/
```

其中：

- `tb/sc_final_tb.v`：单周期 CPU 的 final 测试 testbench。
- `tb/pl_final_tb.v`：流水线 CPU 的 final 测试 testbench。
- `tests/sc/`：单周期 CPU 指令测试机器码。
- `tests/pl/`：流水线 CPU 指令测试机器码。
- `expected_results.json`：部分测试期望结果说明。

常用测试命令见 `iverilog-tests/README.md`，或参考 `report.md` 第 2 章中的命令记录。

### `final_experiment/`

本次验收所用实验工程归档。该目录保存了最终使用的单周期 CPU、流水线 CPU 和 Vivado 上板工程，便于验收、复现和代码追踪。

详见：

```text
final/final_experiment/README.md
```



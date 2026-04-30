#!/usr/bin/env python3
"""
验证单周期CPU仿真波形的快速脚本
直接提取关键信号值

lab-3 新增指令测试:
- andi: 立即数与运算
- bne: 条件分支（不相等跳转）
"""

from pathlib import Path


def parse_vcd_simple(vcd_file):
    """简单快速的VCD解析器"""
    content = Path(vcd_file).read_text(encoding='utf8')
    lines = content.split('\n')
    
    # 信号代码映射 (从VCD文件的var行提取)
    signal_map = {}
    
    for line in lines:
        line = line.strip()
        
        # 解析信号定义
        if line.startswith('$var'):
            parts = line.split()
            if len(parts) >= 4:
                code = parts[3]
                name = ' '.join(parts[4:]).replace('$end', '').strip()
                signal_map[code] = name
        
        # 检查是否进入数据部分
        if line.startswith('$dumpvars'):
            break
    
    # 提取关键信号
    timeline = {}
    current_time = 0
    
    # 关键信号代码（从VCD中直接提取）
    key_signals = {
        ',': 'PC',          # sccomp.PC
        ')': 'instr',       # sccomp.instr
        '!': 'reg_data',   # sccomp.reg_data
        '#': 'reg_sel',     # reg_sel [4:0]
        ':': 'reg_data_sccpu',  # U_SCCPU.reg_data
        '=': 'inst_in',     # U_SCCPU.inst_in
    }
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('#'):
            current_time = int(line[1:])
            if current_time not in timeline:
                timeline[current_time] = {}
        
        elif line and line[0] == 'b':
            # VCD格式: b<value> <code> 或 b<value><code>
            parts = line.split()
            if len(parts) >= 2:
                value = parts[0][1:]  # 去掉 'b' 前缀
                code = parts[-1]  # 最后一个是信号代码
                
                if code in key_signals:
                    if current_time not in timeline:
                        timeline[current_time] = {}
                    timeline[current_time][key_signals[code]] = value
        elif line and line[0] in '01xXzZ-':
            code = line[-1]
            value = line[:-1]
            
            if code in key_signals:
                if current_time not in timeline:
                    timeline[current_time] = {}
                timeline[current_time][key_signals[code]] = value
    
    return timeline


def binary_to_hex(binary_str):
    """将二进制字符串转换为十六进制"""
    if not binary_str:
        return 'N/A'
    if 'x' in binary_str.lower():
        return f'0x{binary_str}'
    try:
        value = int(binary_str, 2)
        return f'0x{value:08x}'
    except:
        return binary_str


def decode_rv32(instr_hex):
    """简单解码RV32指令（仅用于显示）"""
    if not instr_hex or instr_hex == 'N/A':
        return 'N/A'
    
    try:
        instr = int(instr_hex, 16)
    except:
        return instr_hex
    
    opcode = instr & 0x7f
    rd = (instr >> 7) & 0x1f
    funct3 = (instr >> 12) & 0x7
    rs1 = (instr >> 15) & 0x1f
    rs2 = (instr >> 20) & 0x1f
    funct7 = (instr >> 25) & 0x7f
    
    # 简单指令识别
    if opcode == 0x37:  # LUI
        return f"LUI x{rd}, {instr>>12:#x}"
    elif opcode == 0x6f:  # JAL
        return f"JAL x{rd}, {((instr>>31)&1) | ((instr>>20)&0x7ff) | ((instr>>9)&0x3ff) | ((instr>>30)&3)}"
    elif opcode == 0x63:  # Branch
        op = 'BEQ' if funct3 == 0 else 'BNE' if funct3 == 1 else 'BLT' if funct3 == 4 else 'BGE'
        offset = ((instr >> 31) & 1) | (((instr >> 25) & 0x3f) << 1) | (((instr >> 8) & 0xf) << 6) | (((instr >> 7) & 1) << 11)
        if offset & 0x800:
            offset = offset - 0x1000
        return f"{op} x{rs1}, x{rs2}, {offset:+d}"
    elif opcode == 0x13:  # I-type (arith)
        op = ['ADDI', 'SLLI', 'SLTI', 'SLTIU', 'XORI', '', 'ORI', 'ANDI'][funct3] if funct3 < 8 else '?'
        imm = (instr >> 20) & 0xfff
        if imm & 0x800:
            imm = imm - 0x1000
        return f"{op} x{rd}, x{rs1}, {imm:+d}"
    elif opcode == 0x03:  # Load
        op = ['LB', 'LH', 'LW', '', '', '', '', ''][funct3]
        imm = (instr >> 20) & 0xfff
        if imm & 0x800:
            imm = imm - 0x1000
        return f"{op} x{rd}, {imm}(x{rs1})"
    elif opcode == 0x23:  # Store
        op = ['SB', 'SH', 'SW', '', '', '', '', ''][funct3]
        imm = ((instr >> 25) & 0x7f) | ((instr >> 7) & 0x1f)
        return f"{op} x{rs2}, {imm}(x{rs1})"
    elif opcode == 0x33:  # R-type
        if funct7 == 0:
            op = ['ADD', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'OR', 'AND'][funct3] if funct3 < 8 else '?'
        elif funct7 == 0x20:
            op = ['SUB', '', '', '', '', 'SRA', '', ''][funct3]
        else:
            op = '?'
        return f"{op} x{rd}, x{rs1}, x{rs2}"
    
    return f"0x{instr:08x}"


def verify_waveform(vcd_file):
    """验证波形"""
    print("\n" + "="*80)
    print("单周期CPU仿真波形验证 (lab-3: andi + bne)")
    print("="*80 + "\n")
    
    timeline = parse_vcd_simple(vcd_file)
    
    # 预期结果 (根据rv32_sc_sim.dat测试程序)
    expected = {
        'x1 (LUI)': '0x0000003c',
        'x2 (addi)': '0x0000000c',
        'x5 (被bne跳过)': '0x00000000',
        'x6': '0x00000002',
        'x7': '0x00000003',
        'x8': '0x00000009',
    }
    
    # 测试程序指令序列
    test_program = [
        (0x03c00093, "lui x1, 0x3c"),
        (0x00f0f113, "addi x2, x1, 0xf"),
        (0x00500193, "addi x3, x0, 5"),
        (0x00700213, "addi x4, x0, 7"),
        (0x00419463, "bne x3, x4, +8 (taken)"),
        (0x00100293, "addi x5, x0, 1 (skipped)"),
        (0x00200313, "addi x6, x0, 2"),
        (0x00319463, "bne x3, x3, +8 (not taken)"),
        (0x00300393, "addi x7, x0, 3"),
        (0x00900413, "addi x8, x0, 9"),
        (0x0000006f, "jal x0, 0 (infinite loop)"),
    ]
    
    print("📝 测试程序 (rv32_sc_sim.dat):\n")
    for i, (code, desc) in enumerate(test_program):
        print(f"  {i*4:3d}: 0x{code:08x}  {desc}")
    
    print("\n📊 关键时间点的信号变化:\n")
    print(f"{'时间(ns)':<10} {'PC':<12} {'指令':<20} {'写入数据':<12} {'ALU输出':<12}")
    print("-" * 75)
    
    # 显示所有时间点的更新
    times = sorted(timeline.keys())
    for time in times[:50]:  # 显示前50个更新点
        signals = timeline.get(time, {})
        
        pc_val = signals.get('PC', '')
        instr_val = signals.get('instr', '')
        wd_val = signals.get('WD', '')
        alu_val = signals.get('aluout', '')
        
        # 只显示有关键信号更新的时间点
        if any([pc_val, wd_val, alu_val]):
            pc_hex = binary_to_hex(pc_val) if pc_val else '-'
            instr_hex = binary_to_hex(instr_val) if instr_val else '-'
            instr_disp = decode_rv32(instr_hex) if instr_hex != '-' else '-'
            wd_hex = binary_to_hex(wd_val) if wd_val else '-'
            alu_hex = binary_to_hex(alu_val) if alu_val else '-'
            
            print(f"{time:<10} {pc_hex:<12} {instr_disp:<20} {wd_hex:<12} {alu_hex:<12}")
    
    print(f"\n✅ 验证总结:")
    print(f"   VCD文件: {Path(vcd_file).name}")
    print(f"   信号更新事件: {len(timeline)} 个")
    print(f"   时间范围: 0 ~ {max(times) if times else 0} ns")
    
    print(f"\n📋 预期寄存器结果:")
    for key, value in expected.items():
        print(f"   • {key}: {value}")
    
    print(f"\n💡 手动检查步骤:")
    print(f"   1. 在GTKWave中打开 sccpu_sim.vcd")
    print(f"   2. 添加信号: PC, instr, reg_data, reg_sel")
    print(f"   3. 对比各寄存器的值是否与预期一致")
    print(f"   4. 查看 bne 指令的分支跳转行为")
    print(f"      - bne x3, x4 (5 != 7): 分支跳转，跳过 addi x5")
    print(f"      - bne x3, x3 (5 != 5): 分支不跳转，继续执行\n")


def main():
    vcd_file = Path(__file__).parent / "sccpu_sim.vcd"
    
    if not vcd_file.exists():
        print(f"\n❌ VCD文件不存在: {vcd_file}\n")
        print("请先运行仿真:")
        print("  python build.py run\n")
        return
    
    verify_waveform(vcd_file)


if __name__ == "__main__":
    main()
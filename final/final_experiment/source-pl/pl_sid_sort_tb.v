`timescale 1ns/1ns

module pl_sid_sort_tb();
  reg clk;
  reg rstn;
  integer errors;
  integer i;

  plcomp plcomp(.clk(clk), .rstn(rstn));

  initial begin
    $readmemh("rv32_sid_sort_sim.dat", plcomp.U_imem.RAM, 0, 54);

    for (i = 0; i < 128; i = i + 1) begin
      plcomp.U_DM.dmem[i] = 32'h0000_0000;
    end

    clk = 1'b0;
    rstn = 1'b1;
    errors = 0;
    #20;
    rstn = 1'b0;
  end

  always begin
    #5 clk = ~clk;
  end

  initial begin
    $dumpfile("pl_sid_sort.vcd");
    $dumpvars(0, pl_sid_sort_tb);

    #50000;

    if (plcomp.U_DM.dmem[96] !== 32'h2024_3021) begin
      $display("[FAIL] mem[0x180] expected original sid 0x20243021, got %h", plcomp.U_DM.dmem[96]);
      errors = errors + 1;
    end

    if (plcomp.U_DM.dmem[97] !== 32'h0012_2234) begin
      $display("[FAIL] mem[0x184] expected sorted sid 0x00122234, got %h", plcomp.U_DM.dmem[97]);
      errors = errors + 1;
    end

    $display("[RESULT] original_sid=%h", plcomp.U_DM.dmem[96]);
    $display("[RESULT] sorted_sid=%h", plcomp.U_DM.dmem[97]);

    if (errors == 0)
      $display("[PASS] lab-6 pipeline sid sorting simulation passed.");
    else
      $display("[FAIL] lab-6 pipeline sid sorting simulation failed with %0d error(s).", errors);

    #20;
    $finish;
  end
endmodule
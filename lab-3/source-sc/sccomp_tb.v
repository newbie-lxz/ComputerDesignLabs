`timescale 1ns/1ns 
module sccomp_tb();
   reg    clk, rstn;
   reg  [4:0] reg_sel;
   wire [31:0] reg_data;
   integer errors;

   // instantiation of sccomp
   sccomp sccomp(.clk(clk), .rstn(rstn), .reg_sel(reg_sel), .reg_data(reg_data));

   initial begin
     // input instructions for simulation, rv32_sc_sim
      $readmemh("rv32_sc_sim.dat", sccomp.U_imem.RAM);

      clk = 1;
      rstn = 1;
      errors = 0;
      #10 ;
      rstn = 0;
      reg_sel = 8;
   end
   
   always begin
      #(5) clk = ~clk;
   end

   initial begin
      $dumpfile("sccpu_sim.vcd");
      $dumpvars(0, sccomp_tb);

      #220;

      // ===== ori 检测 =====
      if (sccomp.U_SCCPU.U_RF.rf[2] !== 32'd7) begin
         $display("[FAIL] ori failed: x2 expected 7, got %d", sccomp.U_SCCPU.U_RF.rf[2]);
         errors = errors + 1;
      end

      // ===== bge（应该跳转）=====
      if (sccomp.U_SCCPU.U_RF.rf[5] !== 32'd222) begin
         $display("[FAIL] bge jump failed: x5 expected 222, got %d", sccomp.U_SCCPU.U_RF.rf[5]);
         errors = errors + 1;
      end

      // ===== bge（不应该跳转）=====
      if (sccomp.U_SCCPU.U_RF.rf[8] !== 32'd333) begin
         $display("[FAIL] bge not-jump failed: x8 expected 333, got %d", sccomp.U_SCCPU.U_RF.rf[8]);
         errors = errors + 1;
      end

      // ===== 总结 =====
      if (errors == 0)
         $display("[PASS] ori + bge test passed.");
      else
         $display("[FAIL] ori + bge test failed with %0d error(s).", errors);
      #20;
      $finish;
   end 
   
endmodule

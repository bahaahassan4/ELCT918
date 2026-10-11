`timescale 1ns/1ps

module tb;
 reg clk = 0, rst_n = 0, en = 0;
 reg [3:0] din = 0;
 wire [7:0] dout , dout_encrypt;
 wire flag, flag_encrypt;
 int i , cycles_count;
 int j , p;
 int correct_count , error_count;
  
 mystery bb (.clk(clk), .rst_n(rst_n), .en(en), .din(din), .dout(dout), .flag(flag));
 solution ss (.clk(clk), .rst_n(rst_n), .en(en), .din(din), .dout(dout_encrypt), .flag(flag_encrypt)); 
  
 always #5 clk = ~clk;
  
 task step(input e, input [3:0] d);
   begin
   @(negedge clk); en = e; din = d;
   @(posedge clk); #1;
     check(dout_encrypt ,dout , flag , flag_encrypt);
  // $display("t=%0t en=%b din=%h -> dout=%h flag=%b", $time, e, d, dout, flag);
   end
 endtask
  
  task check(input [7:0] dout_encrypt, input [7:0] dout_mystery , input mystery_flag , input encrypt_flag);
   begin
     cycles_count++;
     if((dout_encrypt == dout_mystery) && (mystery_flag == encrypt_flag))begin
       correct_count++;
      // $display("PASS");
     end
     else begin
       error_count++;
       $display("FAIL");
       $display("at cycle = %d" , cycles_count);

       $display("t=%0t encrypt=%h mystery=%h", $time,dout_encrypt, dout_mystery);
       $display("t=%0t encrypt_flag=%b mystery_flag=%b", $time,encrypt_flag, mystery_flag);
       $display("t=%0t en=%b din=%h -> dout=%h flag=%b", $time, ss.en, bb.din, bb.dout, bb.flag);
     end
     //$display("t=%0t encrypt=%h mystery=%h", $time,dout_encrypt, dout_mystery);
   end
 endtask
  
 initial begin
   $dumpfile("dump.vcd"); $dumpvars(0, tb);
   
   repeat (2) @(posedge clk); #1;
   	$display("after reset: dout=%h flag=%b", dout, flag);
   rst_n = 1;
   // Experiment 1: what happens when en is low?
   step(0, 4'h5); 
   step(0, 4'h9);
   // Experiment 2: ... your experiments here ...
   for(i=0;i<20;i=i+1) begin
      //$display("i=%0d", i);
      step(1, 4'h5); 
   end
   for(i=0;i<20;i=i+1) begin
     //$display("i=%0d", i);
     step(1, 4'h9); 
   end

   for(i=0;i<20;i=i+1) begin
      //$display("i=%0d", i);
      step(1, 4'h2); 
   end
   for(j=0;j<20;j=j+1) begin 
   	for(i=0;i<20;i=i+1) begin
        //$display("i=%0d", i);
        step(1, j); 
     end
   end
   $display("what happens to counter when rst is 0?");

   rst_n = 0;
   step(1, 4'h5); 

   repeat (4) @(posedge clk); #1;

   rst_n = 1;
   step(1, 4'h5); 
   step(0, 4'h5); 
   step(0, 4'h5); 

   step(1, 4'h5); 
   $display("what happens to counter?");
   step(1, 4'h5); 
   step(1, 4'h5); 

   
   //random testing
   for(i=0;i<30000;i=i+1) begin
     rst_n = 1;
        //$display("i=%0d", i);
     if (i % 30 == 0) begin
       step(0, $random); 
	 end
     else if (i % 190 == 0) begin
       rst_n = 0;
       step(1, $random); 
	 end
     step(1, $random); 
    end

   
   rst_n = 0;
   repeat (4) 
     @(posedge clk);
   #1;
   rst_n = 1;
   step(1,6);
   step(1,3);
   step(1,'hb);
   step(1,9);
   
   rst_n = 0;
   repeat (4) 
     @(posedge clk);
   #1;
   rst_n = 1;
   step(1, 4'h6); 
   step(1, 4'h3); 
   step(1, 4'hB);
   rst_n = 0;
   repeat (2) 
     @(posedge clk);
   #1;
   rst_n = 1;
	step(1, 4'h9);

   rst_n = 0;
   repeat (4) 
     @(posedge clk);
   #1;
   rst_n = 1;
   
   step(1, 4'h6); 
   step(1, 4'h3);
   step(0, 4'h0);
   step(1, 4'hB); 
   step(1, 4'h9);

   rst_n = 0;
   repeat (4) 
     @(posedge clk);
   #1;
   rst_n = 1;
   step(1, 4'h6); 
   step(1, 4'h3); 
   step(1, 4'hB); 
   step(1, 4'h9);
   step(0, 4'h0); 
   step(0, 4'h0);
   step(0, 4'h0);
   step(1, 4'h0);
/*
 
for (p = 0; p < 65536; p = p + 1) begin
  // reset to start a new message
  @(negedge clk); rst_n = 0; en = 0;
  @(negedge clk); rst_n = 1;
  // apply 4 nibbles, most significant first
  step(1, p[15:12]);
  step(1, p[11:8]);
  step(1, p[7:4]);
  step(1, p[3:0]);
  if (flag) begin
    $display("FOUND password = %h", p[15:0]);
    $display("word= %h", {p[15:12] + 4'd6 , p[11:8] + 4'd7 , p[7:4] + 4'd4 , p[3:0] + 4'd5});

  end
  
end
*/
   
   $display("correct_count = %d",correct_count);
   $display("error_count = %d",error_count);
   if (error_count == 0) 
     $display("PASS");
   
   $finish;
 end
  initial begin
    $monitor("flag =%b ",flag);
  end
endmodule
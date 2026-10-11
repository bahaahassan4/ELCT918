//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
// Cipher: position-dependent additive cipher on 4-bit nibbles.
//       ciphertext = (din + key_k) mod 16,   key sequence 6, 7, 4, 5 and repeat
//   dout = {number of encryptions since reset (mod 16)(counter ya3ne keda), ciphertext}
//   flag = 1 when the last four ciphertext nibbles spell 16'hCAFE (password)
//
// rst_n is synchronous and active-low; it wins over en.
// When en is low every register holds its value.
/////////////////////////////////////////////////////////////////////////////
module solution(clk, rst_n, en, din, dout, flag);
	input clk;
	input [3:0] din;
	input en;
	input rst_n;

	output reg flag;
	output reg [7:0] dout;

	parameter IDLE=3'b000;
	parameter S1=3'b001;
	parameter S2=3'b010;
	parameter S3=3'b011;
	parameter S4=3'b100;

  reg [2:0] cs , ns;
  reg [3:0] counter;
  reg [15:0] history_buffer;
  reg [3:0] key;

  //
  always @(posedge clk) begin
    if(~rst_n) begin
      cs <= IDLE;
      counter <= 0;
      history_buffer <= 0;
      
      dout <= 0;
      flag <= 0;

    end
    else begin
      cs <= ns;
      if(en)begin
      	counter <= counter +1;
        
        dout <= {counter + 4'd1, din + key};
        history_buffer <= {history_buffer[11:0], din + key};
        flag <= ({history_buffer[11:0], din + key} == 16'hCAFE);
      end
      end
  end
  
  //next state logic
  always @(*)begin
    case(cs)
      IDLE:begin
        if(~rst_n)
          ns = IDLE;
        else if(en)
          ns = S1;
        else
          ns = cs;
      	end
      S1:begin       
        if(~rst_n)
          ns = IDLE;
        else if(en)
          ns = S2;
        else
          ns = cs;
      	end
      S2:begin       
        if(~rst_n)
          ns = IDLE;
        else if(en)
          ns = S3;
        else
          ns = cs;
      	end
      S3:begin       
        if(~rst_n)
          ns = IDLE;
        else if(en)
          ns = S4;
        else
          ns = cs;
      	end
      S4:begin       
        if(~rst_n)
          ns = IDLE;
        else if(en)
          ns = S1;
        else
          ns = cs;
      	end
      default: ns = cs;
    endcase
  end
  //output logic
    always @(*) begin
    case (ns)
      S1: key = 4'd6;
      S2: key = 4'd7;
      S3: key = 4'd4;
      S4: key = 4'd5;
      default: key = 4'd0;
    endcase
  end
  
endmodule
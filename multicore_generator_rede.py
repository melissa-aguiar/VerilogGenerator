def main():

    #  ########################################## PARAMETROS ###########################################################
    procs = 72  # numero de processadores pra gerar o multicore.v e multicore_tb.v
    freq = 3125  # frequencia do clock no _tb
    mlt = 0  # numero de multiplicadores pra colocar entre as entradas do .asm
    nbmant = 19  # numero de bits da mantissa
    nbexpo = 8  # numero de bits do expoente
    nubits = 1
    extra = 4  # numero a mais de MLT pra colocar na saida pra atrasar ela e sincronizar as janelas de entrada

    #  ########################################## GERAR O .ASM #########################################################
    f1 = open("assembler_in.txt", "w+")
    for i in range(10):
        f1.write("LOAD 0" + '\n')
        for j in range(mlt):
            f1.write("MLT -1" + '\n')
        f1.write("PUSH" + '\n' + "IN" + '\n' + "SET mainy" + str(i) + '\n')
    f1.close()

    f2 = open("assembler_out.txt", "w+")

    for i in range(extra):
        f2.write("MLT -1" + '\n')

    f2.close()

    #  ################################################  MULTICORE #####################################################

    f12 = open("C:/Users/melis/Desktop/GitDesk/rede_taylor/rede_taylor/Hardware/rede_taylor_H/multicore.v", "w+")
    #  f12 = open("top_level.txt","w+")
    f12.write("module multicore (" + '\n')
    f12.write("\tinput clk," + '\n')
    f12.write("\tinput signed [" + str(nbmant-1) + ":0] io_in," + '\n')
    f12.write("\toutput signed [" + str(nbmant+nbexpo) + ":0] ")
    for i in range(procs):
        f12.write("io_out" + str(i) + ", ")
    f12.write('\n')
    f12.write("\toutput [3:0] ")
    for i in range(procs):
        f12.write("req_in" + str(i) + ", ")
    f12.write('\n')
    f12.write("\toutput [3:0] ")
    for i in range(procs-1):
        f12.write("out_en" + str(i) + ", ")
    f12.write("out_en" + str(procs-1) + '\n' + ");")
    f12.write('\n')
    f12.write('\n')

    f12.write("reg ")
    for i in range(procs-1):
        f12.write("rst" + str(i) + ", ")
    f12.write("rst" + str(procs-1) + ";")
    f12.write('\n')
    f12.write("reg signed [" + str(nbmant+nbexpo) + ":0] my_io_out;")
    f12.write('\n')
    f12.write("reg [3:0] my_out_en;")
    f12.write('\n')
    f12.write("reg [8:0] q;" +'\n' + "reg [12:0] cnt;" + '\n')
    f12.write('\n')
    f12.write('\n')

    f12.write("initial begin" + '\n')
    for i in range(procs):
        f12.write("\trst" + str(i) + " = 1;" + '\n')
    f12.write("\tq = 0;" + '\n')
    f12.write("\tcnt = 0;" + '\n')
    f12.write("end" + '\n')
    f12.write('\n')

    f12.write("always @(posedge clk) begin" + '\n')
    f12.write("\tcase (q)" + '\n')
    for i in range(procs):
        f12.write('\t\t' + str(i) + ": begin rst" + str(i) +
                  " <= 0; if (cnt <= 11'd" + str(mlt+2) +
                  ") cnt=cnt+11'd1; else begin q <= q+9'd1; cnt=0; end	end" + '\n')
    f12.write("\t\tdefault: q <= 9'd147;" + '\n')
    f12.write("\tendcase" + '\n')
    f12.write("end" + '\n')
    f12.write('\n')

    f12.write("always @(*) begin" + '\n')
    for i in range(procs):
        f12.write("\tif (out_en" + str(i) + " == 1) begin my_io_out <= io_out" + str(i) + "; my_out_en <= out_en" +
                  str(i) + "; end else" + '\n')
    f12.write("\tbegin my_io_out <= 0; my_out_en <= 0; end" + '\n')
    f12.write("end" + '\n')
    f12.write('\n')

    for i in range(procs):
        f12.write("rede_taylor rede_taylor" + str(i) + " (clk, rst" + str(i) + ", io_in, io_out" + str(i) + ", req_in" +
                  str(i) + ", out_en" + str(i) + ");" + '\n')
    f12.write("endmodule" + '\n')
    f12.write('\n')
    f12.close()

    #  ################################################ TESTBENCH MULTICORE ############################################
    f13 = open("C:/Users/melis/Desktop/GitDesk/rede_taylor/rede_taylor/Hardware/rede_taylor_H/multicore_tb.v", "w+")
    #  f13 = open("testbench.txt","w+")
    f13.write("module multicore_tb();" + '\n')
    f13.write("\treg clk;" + '\n')
    f13.write("\twire [3:0] ")
    for i in range(procs - 1):
        f13.write("req_in" + str(i) + ", ")
    f13.write("req_in" + str(procs - 1) + ";" + '\n')
    f13.write("\treg signed [" + str(nbmant-1) + ":0] in;" + '\n')
    f13.write("\twire signed [" + str(nbmant+nbexpo) + ":0] ")
    for i in range(procs - 1):
        f13.write("io_out" + str(i) + ", ")
    f13.write("io_out" + str(procs - 1) + ";" + '\n')
    f13.write("\twire [3:0] ")
    for i in range(procs - 1):
        f13.write("out_en" + str(i) + ", ")
    f13.write("out_en" + str(procs - 1) + ";" + '\n')
    f13.write("\tinteger data_file, scan_file, my_output;" + '\n')
    f13.write('\n')

    f13.write("initial begin " + '\n')
    f13.write("\tdata_file = $fopen(\"sinal_entrada.txt\", \"r\");" + '\n')
    f13.write("\tmy_output = $fopen(\"myoutput.txt\", \"w\");" + '\n')
    f13.write("\tscan_file = $fscanf(data_file, \"%d\\n\", in);" + '\n')
    f13.write("\tclk = 0;" + '\n')
    f13.write("end" + '\n')
    f13.write('\n')

    f13.write("always #" + str(freq) + " clk = ~clk;" + '\n')
    f13.write('\n')

    f13.write("always @(posedge clk) begin" + '\n')
    f13.write("\tif ((")
    for i in range(procs - 1):
        f13.write("req_in" + str(i) + " || ")
    f13.write("req_in" + str(procs - 1) + ") == 4'd1)" + '\n')
    f13.write("\t\tscan_file = $fscanf(data_file, \"%d\\n\", in);" + '\n')
    f13.write("end" + '\n')
    f13.write('\n')

    f13.write("always @(posedge clk) begin" + '\n')
    for i in range(procs):
        f13.write("\tif (out_en" + str(i) + " == 4'd1) $fwrite(my_output, \"%d\\n\", io_out" + str(i) + ");" + '\n')
    f13.write("end" + '\n')
    f13.write('\n')

    f13.write("multicore multicore(clk,in,")
    for i in range(procs):
        f13.write("io_out" + str(i) + ",")
    for i in range(procs):
        f13.write("req_in" + str(i) + ",")
    for i in range(procs-1):
        f13.write("out_en" + str(i) + ",")
    f13.write("out_en" + str(procs-1) + ");" + '\n')
    f13.write('\n')
    f13.write("endmodule")
    f13.write('\n')
    f13.close()

    #  ################################################  BLACKBOX ######################################################

    #  f5 = open("C:/Users/melis/Desktop/GitDesk/ssf/ssf/Hardware/ssf_H/ssfblackbox.v", "w+")
    f5 = open("ssfblackbox.txt","w+")
    f5.write("module ssfblackbox (" + '\n')
    f5.write("\tinput clk," + '\n')
    f5.write("\tinput signed [" + str(nubits-1) + ":0] io_in," + '\n')
    f5.write("\toutput signed [" + str(nubits-1) + ":0] my_io_out," + '\n')
    f5.write("\toutput [1:0] my_req_in," + '\n')
    f5.write("\toutput [1:0] my_out_en" + '\n' "\t);")
    f5.write('\n')
    f5.write('\n')

    f5.write("reg [1:0] out_en, req_in;" + '\n')
    f5.write("reg signed [" + str(nubits-1) + ":0] io_out;" + '\n')
    f5.write('\n')

    f5.write("wire [1:0] ")
    for i in range(procs - 1):
        f5.write("req_in" + str(i) + ", ")
    f5.write("req_in" + str(procs - 1) + ";")
    f5.write('\n')

    f5.write("wire [1:0] ")
    for i in range(procs - 1):
        f5.write("out_en" + str(i) + ", ")
    f5.write("out_en" + str(procs - 1) + ";")
    f5.write('\n')
    f5.write('\n')

    f5.write("wire signed [" + str(nubits-1) + ":0] ")
    for i in range(procs - 1):
        f5.write("io_out" + str(i) + ", ")
    f5.write("io_out" + str(procs - 1) + ";")
    f5.write('\n')
    f5.write('\n')

    f5.write("reg ")
    for i in range(procs - 1):
        f5.write("rst" + str(i) + ", ")
    f5.write("rst" + str(procs - 1) + ";")
    f5.write('\n')
    f5.write('\n')

    f5.write("reg [8:0] q;" + '\n' + "reg [12:0] cnt;" + '\n')
    f5.write('\n')
    f5.write('\n')

    f5.write("initial begin" + '\n')
    for i in range(procs):
        f5.write("\trst" + str(i) + " = 1;" + '\n')
    f5.write("\tq = 0;" + '\n')
    f5.write("\tcnt = 0;" + '\n')
    f5.write("end" + '\n')
    f5.write('\n')

    f5.write("always @(posedge clk) begin" + '\n')
    f5.write("\tcase (q)" + '\n')
    for i in range(procs):
        f5.write('\t\t' + str(i) + ": begin rst" + str(i) +
                 " <= 0; if (cnt <= 11'd" + str(55*(mlt+4)-2) +
                 ") cnt=cnt+11'd1; else begin q <= q+9'd1; cnt=0; end	end" + '\n')

    f5.write("\t\tdefault: q <= 9'd147;" + '\n')
    f5.write("\tendcase" + '\n')
    f5.write("end" + '\n')
    f5.write('\n')

    f5.write("always @(*) begin" + '\n')
    for i in range(procs):
        f5.write("\tif (req_in" + str(i) + " == 1) begin req_in <= req_in" + str(i) + "; end else" + '\n')
    f5.write("\tbegin req_in <= 0; end" + '\n')
    f5.write("end" + '\n')
    f5.write('\n')

    f5.write("always @(*) begin" + '\n')
    for i in range(procs):
        f5.write("\tif (out_en" + str(i) + " == 1) begin io_out <= io_out" + str(i) + "; out_en <= out_en" +
                 str(i) + "; end else" + '\n')
    f5.write("\tbegin io_out <= 0; out_en <= 0; end" + '\n')
    f5.write("end" + '\n')
    f5.write('\n')

    f5.write("assign my_io_out = io_out;" + '\n')
    f5.write("assign my_out_en = out_en;" + '\n')
    f5.write("assign my_req_in = req_in;" + '\n')
    f5.write('\n')
    f5.write('\n')

    for i in range(procs):
        f5.write("ssf ssf" + str(i) + " (clk, rst" + str(i) + ", io_in, io_out" + str(i) + ", req_in" +
                  str(i) + ", out_en" + str(i) + ");" + '\n')
    f5.write('\n')
    f5.write("endmodule" + '\n')
    f5.write('\n')
    f5.close()

    #  ################################################# TESTBENCH BLACKBOX ############################################
    #  f6 = open("C:/Users/melis/Desktop/GitDesk/ssf/ssf/Hardware/ssf_H/ssfblackbox_tb.v", "w+")
    f6 = open("ssfblackbox_tb.txt", "w+")
    f6.write("module ssfblackbox_tb();" + '\n')
    f6.write("\treg clk;" + '\n')
    f6.write("\twire [1:0] req_in;" + '\n')
    f6.write("\treg signed [" + str(nubits - 1) + ":0] in;" + '\n')
    f6.write("\twire signed [" + str(nubits - 1) + ":0] my_io_out;" + '\n')
    f6.write("\twire [1:0] my_out_en;" + '\n')
    f6.write("\tinteger data_file, scan_file, my_output;" + '\n')
    f6.write('\n')

    f6.write("initial begin " + '\n')
    f6.write("\tdata_file = $fopen(\"signalN.txt\", \"r\");" + '\n')
    f6.write("\tmy_output = $fopen(\"myoutput.txt\", \"w\");" + '\n')
    f6.write("\tscan_file = $fscanf(data_file, \"%d\\n\", in);" + '\n')
    f6.write("\tclk = 0;" + '\n')
    f6.write("end" + '\n')
    f6.write('\n')

    f6.write("always #" + str(freq) + " clk = ~clk;" + '\n')
    f6.write('\n')

    f6.write("always @(posedge clk) begin" + '\n')
    f6.write("\tif (req_in == 1'd1) scan_file = $fscanf(data_file, \"%d\\n\", in);" + '\n')
    f6.write("end" + '\n')
    f6.write('\n')

    f6.write("always @(posedge clk) begin" + '\n')
    f6.write("\tif (my_out_en == 1'd1) $fwrite(my_output, \"%d\\n\", my_io_out);" + '\n')
    f6.write("end" + '\n')
    f6.write('\n')

    f6.write("ssfblackbox ssfblackbox(clk,in,my_io_out,req_in,my_out_en);" + '\n')
    f6.write('\n')

    f6.write("endmodule")
    f6.write('\n')
    f6.close()


if __name__ == "__main__":
    main()

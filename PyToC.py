VNT = {} #Variable Name Types
C_common_headers = {"printf":"stdio.h",
                    "bool":"stdbool.h"}
headers_needed = []

class pylexers():
  def str_vint(inp):
    if '"' in inp or "'" in inp:
      return str
    
    else:
      return int

  def int_var(inp):
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    VAR=0
    for i in alphabet:
      if i in inp:
        VAR = 1
        break
      
    if VAR==1:
      return "var"
    else:
      return int
  
  def int_float(inp):
    if "." in inp:
      return float
            
    elif "." != inp:
      return int
  
  def array_not(inp):
    if "[" in inp or "," in inp:
      return list
    else:
      return None
      
  def pass_(inp):
    pass
  
  def branching_tree(inp,functs={str:None,"var":None,int:None,float:None}):
    string_or_other = pylexers.str_vint(inp)
    if string_or_other == str:
      try:
        functs[str]()
      except:
        pass
      return str
    else:
      Var_or_int = pylexers.int_var(inp)
      if Var_or_int == "var":
        try:
          functs["var"]()
        except:
          pass
        return "var"
      else:
        Int_or_float = pylexers.int_float(inp)
        if Int_or_float == int:
          try:
            functs[int]()
          except:
            pass
          return int
        else:
          try:
            functs[float]()
          except:
              pass
          return float
  
class C():
  main = ["int main(){"]
  ending = ["}"]
  int = ["int"]
  str = ["char"]
  space = [" "]
  Nl = ["\n"]
  semi_cln = [";"]
  equal = ["="]
  rtn = ["return"]
  open_p = ["("]
  close_p = [")"]
  open_b = ["["]
  close_b = ["]"]
  indent = [" "]
  comment_1 = ["//"]
  print_ = ["printf"]
  _STR = ['"']
  _comma = [","]
  require = ["#include"]
  _over = ["<"]
  _under = [">"]
  
def turn_to_C(file):
  read_file = open(file,"r")
  C_code = open(file.split(".")[0]+".c","w")
  fcode_seq = []
  fcode_seq += C.main+C.Nl
  for line in read_file:
    line = line.replace("\n","")
    if line.startswith("#"):
      fcode_seq += C.indent+C.comment_1+[line.split("#")[1]]+C.Nl
      
    elif "=" in line:
      var_name = line.split("=")[0].replace(" ","")
      VD = line.split("=")[1]
      try:
        var_data = VD[VD.index('"'):] if " " in VD[:VD.index('"')] else VD
      except:
        try:
          var_data = VD[VD.index("'"):] if " " in VD[:VD.index("'")] else VD
        except:
          var_data = int(VD)
      type_ = pylexers.str_vint(str(var_data))
      VNT[var_name] = [var_data,type_]
      if type_ == int:
        fcode_seq += C.indent+C.int+C.space+[var_name]+C.space+C.equal+C.space+[var_data]+C.semi_cln+C.Nl
      if type_ == str:
        fcode_seq += C.indent+C.str+C.space+[var_name]+C.open_b+[str(len(var_data[1:-1]))]+C.close_b+C.space+C.equal+C.space+[var_data]+C.semi_cln+C.Nl
    
    elif "print" in line:
      possibles = {"print(":["(",")"],
                   "print[":["[","]"],
                   "print{":["[","]"]}
      t_ = possibles[line.replace(" ","")[:6]]
      data = line[line.index(t_[0])+1:line.index(t_[1])]
      headers_needed.append(C_common_headers["printf"])
      def _var():
        if VNT[data][1]==int:
          fcode_seq+=C.indent+C.print_+C.open_p+C._STR+["%d"]+C._STR+C.close_p+[data]+C.semi_cln+C.Nl
          
      
      fcode_seq+=C.indent+C.print_+C.open_p+C._STR+["%d"]+C._STR+C._comma+[data]+C.close_p+C.semi_cln+C.Nl
      
      pylexers.branching_tree(data,{"var":_var})
  
  
  
  fcode_seq+=C.indent+C.rtn+C.space+["0"]+C.semi_cln+C.Nl+C.ending+C.Nl
  headers = [C.require+C._over+[x]+C._under+C.Nl for x in headers_needed]
  headers += fcode_seq
  
  flatcode = []
  for item in headers:
    if type(item) == list:
      flatcode+=item
    else:
      flatcode.append(item)
      
  for i in flatcode:
    C_code.write(i)

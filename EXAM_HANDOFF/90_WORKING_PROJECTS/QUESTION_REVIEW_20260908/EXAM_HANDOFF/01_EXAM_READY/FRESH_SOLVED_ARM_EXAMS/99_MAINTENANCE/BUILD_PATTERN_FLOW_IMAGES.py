"""Build production example C at O0 for modeled execution; native projects are a separate gate."""
from pathlib import Path
import argparse,json,subprocess,hashlib
from pattern_runnable import HERE,OUT,TEMPLATE,all_specs

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--compiler-bin',type=Path,required=True);ap.add_argument('--device-include',type=Path,required=True);a=ap.parse_args()
 dest=HERE/'.pattern-flow-images';dest.mkdir(exist_ok=True)
 source=TEMPLATE/'Source'
 def run(cmd):
  p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
  if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 flags=['--target=arm-arm-none-eabi','-mcpu=cortex-m3','-mthumb','-O0','-g']
 for p in [source,*[p for p in source.iterdir() if p.is_dir()],a.device_include]:flags+=['-I',str(p)]
 support=dest/'support.c';support.write_text('#include <stdint.h>\nuint32_t SystemFrequency=100000000u;\nvoid SystemInit(void){SystemFrequency=100000000u;}\n')
 common=[source/p for p in ['exam_api/exam_api.c','RIT/lib_RIT.c','timer/lib_timer.c','led/lib_led.c','led/funct_led.c','button_EXINT/lib_button.c','systick/lib_systick.c','joystick/lib_joystick.c','adc/lib_adc.c']]+[support]
 objs=[]
 for i,p in enumerate(common):
  obj=dest/f'common-{i}.o';run([a.compiler_bin/'armclang.exe',*flags,'-c',p,'-o',obj]);objs.append(obj)
 records={}
 for key in all_specs():
  if key.startswith('algorithm-'):continue
  p=OUT/key/'Source/sample.c';obj=dest/(key+'.o');asm=OUT/key/'Objects/asm_funct.o'
  run([a.compiler_bin/'armclang.exe',*flags,'-c',p,'-o',obj])
  run([a.compiler_bin/'armlink.exe','--entry=main','--no_remove','--ro_base=0x10000','--rw_base=0x10000000',*objs,obj,asm,OUT/key/'Objects/startup_lpc17xx.o','-o',dest/(key+'.axf')])
  records[key]={'main':hashlib.sha256(p.read_bytes()).hexdigest(),'assembly':hashlib.sha256((OUT/key/'Source/ASM_funct.s').read_bytes()).hexdigest()}
  print(key,'simulation image built',flush=True)
 (HERE/'PATTERN_FLOW_IMAGE_SOURCES.json').write_text(json.dumps({'method':'Native Arm Compiler O0 C plus native assembly objects; SystemInit substituted at100MHz; normal Keil project builds reported separately','projects':records},indent=2)+'\n')
if __name__=='__main__':main()

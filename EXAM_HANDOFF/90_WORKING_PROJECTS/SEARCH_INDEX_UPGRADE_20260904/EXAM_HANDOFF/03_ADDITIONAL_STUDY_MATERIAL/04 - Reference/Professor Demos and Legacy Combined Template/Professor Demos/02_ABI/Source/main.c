
extern int ASM_funct(int, int, int, int, int, int, int*);



int main(void){

	unsigned int i=1, j=2, k=3, l=4, m=5, n=6;
	int vett[100];
	volatile int r=0;
	
	vett[0]=0x55aa55aa;
	vett[1]=0xFEDEFEDE;

	r = ASM_funct(i, j, k, l, m, n, vett);
		
	while(1);
}

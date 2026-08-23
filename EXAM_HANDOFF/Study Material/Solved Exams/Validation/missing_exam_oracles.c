#include <assert.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

uint32_t oracle_kaprekar(uint32_t value)
{
    uint32_t digits[4], i, j, ascending = 0, descending = 0;
    for (i = 0; i < 4; ++i) { digits[i] = value % 10u; value /= 10u; }
    for (i = 0; i < 3; ++i) for (j = i + 1; j < 4; ++j)
        if (digits[j] < digits[i]) { uint32_t t=digits[i]; digits[i]=digits[j]; digits[j]=t; }
    for (i = 0; i < 4; ++i) { ascending=ascending*10u+digits[i]; descending=descending*10u+digits[3u-i]; }
    return descending - ascending;
}

int32_t oracle_sdiv64(int32_t upper, uint32_t lower, int32_t divisor, int *overflow)
{
    int64_t dividend = ((int64_t)upper << 32) | lower;
    if (divisor == 0) { *overflow=1; return 0; }
    int64_t q = dividend / divisor;
    *overflow = q > INT32_MAX || q < INT32_MIN;
    return (int32_t)q;
}

uint32_t oracle_digit_sum(uint32_t value)
{
    uint32_t sum=0; do { sum += value % 10u; value /= 10u; } while(value); return sum;
}

uint32_t oracle_digit_addition(uint32_t *series, uint32_t n)
{
    uint32_t i, total;
    if (!series || n == 0) return 0;
    total=oracle_digit_sum(series[0]);
    for(i=1;i<n;++i) { uint32_t add=oracle_digit_sum(series[i-1]); uint32_t next=series[i-1]+add;
        if(next<series[i-1]) return 0;
        series[i]=next;
        total+=oracle_digit_sum(next);
    }
    return total;
}

uint32_t oracle_maze_solver(uint32_t rows,uint32_t cols,uint8_t *m)
{
    uint32_t iterations=0, changed, r,c;
    if(rows<2||cols<2||!m) return 0;
    do {
        changed=0;
        for(r=1;r+1<rows;++r) for(c=1;c+1<cols;++c) { uint32_t k=r*cols+c; if(m[k]!=' ') continue;
            if(m[k-cols]>='a'&&m[k-cols]<='z') {m[k]='N';changed=1;}
            else if(m[k+1]>='a'&&m[k+1]<='z') {m[k]='E';changed=1;}
            else if(m[k+cols]>='a'&&m[k+cols]<='z') {m[k]='S';changed=1;}
            else if(m[k-1]>='a'&&m[k-1]<='z') {m[k]='W';changed=1;}
        }
        if(changed) { for(r=1;r+1<rows;++r) for(c=1;c+1<cols;++c) {uint32_t k=r*cols+c;if(m[k]>='A'&&m[k]<='Z')m[k]=(uint8_t)(m[k]+('a'-'A'));} ++iterations; }
    } while(changed);
    return iterations;
}

uint32_t oracle_shortest_path(uint32_t rows,uint32_t cols,uint8_t *m)
{
    uint32_t distance=0,changed,r,c;
    if(rows<3||cols<3||!m)return 0;
    for(;;){changed=0;for(r=1;r+1<rows;++r)for(c=1;c+1<cols;++c){uint32_t k=r*cols+c;if(m[k]=='e'){
        if(m[k-1]<=distance||m[k+1]<=distance||m[k-cols]<=distance||m[k+cols]<=distance)return distance;
      } else if(m[k]==' ' && (m[k-1]==distance||m[k+1]==distance||m[k-cols]==distance||m[k+cols]==distance)) {m[k]=(uint8_t)(distance+1u);changed=1;}}
      if(!changed)return 0;
      ++distance;
    }
}

static uint32_t choose_neighbor(uint32_t right,uint32_t bottom,uint32_t left,uint32_t top)
{ if(!right)return 1;if(!bottom)return 2;if(!left)return 3;if(!top)return 4;return 0; }

void oracle_depth_first(uint8_t *m,uint32_t rows,uint32_t cols,uint32_t start)
{
    uint32_t stack[1024],sp=0,current=start;
    assert(rows*cols<=1024u);m[current]|=1u;
    for(;;){uint32_t right=m[current+1]&1u,bottom=m[current+cols]&1u,left=m[current-1]&1u,top=m[current-cols]&1u;
      uint32_t d=choose_neighbor(right,bottom,left,top),next;
      if(!d){if(!sp)break;current=stack[--sp];continue;}
      stack[sp++]=current;
      if(d==1){next=current+1;m[current]|=2u;m[next]|=8u;}
      else if(d==2){next=current+cols;m[current]|=4u;m[next]|=16u;}
      else if(d==3){next=current-1;m[current]|=8u;m[next]|=2u;}
      else {next=current-cols;m[current]|=16u;m[next]|=4u;}
      m[next]|=1u;current=next;
    }
}

static void merge_labels(uint8_t *maze,uint32_t n,uint8_t a,uint8_t b)
{uint8_t lo=a<b?a:b,hi=a<b?b:a;uint32_t i;for(i=0;i<n;++i)if(maze[i]==hi)maze[i]=lo;}

int oracle_kruskal(uint8_t *maze,uint8_t *h,uint8_t *v,uint32_t rows,uint32_t cols,uint32_t y,uint32_t x)
{
    uint32_t n=rows*cols,guard=0,i; if(!n||!y)return -1;
    while(guard++<n*n*16u){x+=y;if(x<n){if(h[x]==1u&&maze[x]!=maze[x+1u]){h[x]=0;merge_labels(maze,n,maze[x],maze[x+1u]);}else if(h[x]==0u)++y;}
      else{x-=n;if(x<n){if(v[x]==1u&&maze[x]!=maze[x+cols]){v[x]=0;merge_labels(maze,n,maze[x],maze[x+cols]);}else if(v[x]==0u)++y;}}
      for(i=1;i<n&&maze[i]==maze[0];++i) { }
      if(i==n)return 0;
    }
    return -1;
}

int main(void)
{
    uint32_t s[5]={47}; int ov;
    assert(oracle_kaprekar(3075)==7173);assert(oracle_kaprekar(7173)==6354);assert(oracle_kaprekar(8352)==6174);
    assert(oracle_sdiv64(-1,0xFFFFFFDDu,-5,&ov)==7&&!ov);
    assert(oracle_digit_addition(s,5)==62);assert(s[4]==95);
    {uint8_t m[25]={'*','*','n','*','*','*',' ',' ',' ','*','*',' ','*',' ','*','*',' ',' ',' ','*','*','*','s','*','*'};assert(oracle_maze_solver(5,5,m)>0);}
    {uint8_t m[25]={'X','X','X','X','X','X',0,' ',' ','X','X',' ','X',' ','X','X',' ',' ','e','X','X','X','X','X','X'};assert(oracle_shortest_path(5,5,m)>0);}
    {uint8_t m[30];uint32_t r,c;memset(m,0,sizeof m);for(r=0;r<6;++r)for(c=0;c<5;++c)if(!r||r==5||!c||c==4)m[r*5+c]=255;oracle_depth_first(m,6,5,7);for(r=1;r<5;++r)for(c=1;c<4;++c)assert(m[r*5+c]&1u);}
    {uint8_t maze[12],h[12],v[12];uint32_t i;for(i=0;i<12;++i){maze[i]=(uint8_t)i;h[i]=(i%4==3)?2:1;v[i]=(i>=8)?2:1;}assert(oracle_kruskal(maze,h,v,3,4,4,2)==0);for(i=1;i<12;++i)assert(maze[i]==maze[0]);}
    puts("seven missing-exam C oracles passed");return 0;
}

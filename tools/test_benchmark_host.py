#!/usr/bin/env python3
"""Compile the real benchmark.c against host stubs. No hardware data is generated.

The only header substitution replaces the Xtensa cycle-register reader with a
host clock. The C assertions exercise failed network/authentication attempts,
sample SD, attempt IDs, successful-sample denominators and invalid sample counts.
"""
import argparse
import os
from pathlib import Path
import re
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='cc')
    parser.add_argument('--zig-linux', action='store_true')
    parser.add_argument('--compile-only', action='store_true')
    args = parser.parse_args()
    out = ROOT/'build/benchmark-host'
    out.mkdir(parents=True, exist_ok=True)
    header = (ROOT/'firmware/main/benchmark.h').read_text(encoding='utf-8')
    header = re.sub(r'static inline uint32_t benchmark_get_cycles\(void\) \{.*?\n\}',
                    'uint32_t benchmark_get_cycles(void);', header, flags=re.S)
    (out/'benchmark.h').write_text(header, encoding='utf-8')
    common = r'''
#pragma once
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#define CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ 160
#define MALLOC_CAP_DEFAULT 0
#define ESP_OK 0
#define HTTP_METHOD_POST 1
#define pdMS_TO_TICKS(n) (n)
typedef int esp_err_t;
typedef void* esp_http_client_handle_t;
typedef struct { const char *url; int method; int timeout_ms; } esp_http_client_config_t;
void host_log(const char *, ...);
#define ESP_LOGI(tag,...) host_log(__VA_ARGS__)
#define ESP_LOGW(tag,...) host_log(__VA_ARGS__)
#define ESP_LOGE(tag,...) host_log(__VA_ARGS__)
size_t heap_caps_get_free_size(int);
int64_t esp_timer_get_time(void);
void vTaskDelay(int);
const char* esp_err_to_name(int);
esp_http_client_handle_t esp_http_client_init(const esp_http_client_config_t*);
int esp_http_client_set_header(void*,const char*,const char*);
int esp_http_client_set_post_field(void*,const char*,int);
int esp_http_client_open(void*,int);
int esp_http_client_write(void*,const char*,int);
int esp_http_client_fetch_headers(void*);
int esp_http_client_get_status_code(void*);
int esp_http_client_read(void*,char*,int);
int esp_http_client_cleanup(void*);
int esp_http_client_perform(void*);
'''
    (out/'common.h').write_text(common, encoding='utf-8')
    for name in ('sdkconfig.h','esp_log.h','esp_heap_caps.h','esp_timer.h','esp_http_client.h',
                 'freertos/FreeRTOS.h','freertos/task.h','mbedtls/ssl.h','mbedtls/ctr_drbg.h','mbedtls/entropy.h'):
        path=out/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('#include "common.h"\n',encoding='utf-8')
    test = r'''
#include "common.h"
#include "benchmark.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
static int scenario[8], attempt, csv_count, ids[8];
static int64_t ticks;
void host_log(const char* fmt, ...) {
    va_list ap; va_start(ap,fmt);
    if(strncmp(fmt,"CSV_DATA,",9)==0) ids[csv_count++]=(int)va_arg(ap,unsigned int);
    va_end(ap);
}
uint32_t benchmark_get_cycles(void){return (uint32_t)(ticks*160);}
int64_t esp_timer_get_time(void){return ticks;}
size_t heap_caps_get_free_size(int x){(void)x;return 100000;}
void vTaskDelay(int x){ticks+=(int64_t)x*1000;}
const char* esp_err_to_name(int x){(void)x;return "test-error";}
void hybrid_init(hybrid_ctx_t* c,handshake_mode_t m){memset(c,0,sizeof(*c));c->mode=m;attempt++;}
int hybrid_keygen(hybrid_ctx_t* c){(void)c;ticks+=250;return scenario[attempt]==3?-1:0;}
int hybrid_pack_pubkeys(hybrid_ctx_t* c,uint8_t* b,size_t n){(void)c;(void)b;(void)n;return 1249;}
int hybrid_process_server_response(hybrid_ctx_t* c,const uint8_t* b,size_t n){
    (void)c;(void)b;(void)n;ticks+=(attempt%2==0?1000:2500);return scenario[attempt]==2?-1:0;
}
void hybrid_cleanup(hybrid_ctx_t* c){(void)c;}
const char* hybrid_mode_name(handshake_mode_t m){(void)m;return "test";}
esp_http_client_handle_t esp_http_client_init(const esp_http_client_config_t* c){(void)c;return (void*)1;}
int esp_http_client_set_header(void*c,const char*k,const char*v){(void)c;(void)k;(void)v;return 0;}
int esp_http_client_set_post_field(void*c,const char*v,int n){(void)c;(void)v;(void)n;return 0;}
int esp_http_client_open(void*c,int n){(void)c;(void)n;return scenario[attempt]==1?-1:0;}
int esp_http_client_write(void*c,const char*b,int n){(void)c;(void)b;return n;}
int esp_http_client_fetch_headers(void*c){(void)c;return 1168;}
int esp_http_client_get_status_code(void*c){(void)c;return 200;}
int esp_http_client_read(void*c,char*b,int n){(void)c;memset(b,0,(size_t)n);return n;}
int esp_http_client_cleanup(void*c){(void)c;return 0;}
int esp_http_client_perform(void*c){(void)c;return 0;}
static void reset(void){memset(scenario,0,sizeof(scenario));attempt=-1;csv_count=0;ticks=0;}
int main(void){
    benchmark_stats_t s;
    reset();
    assert(benchmark_run_campaign(MODE_HYBRID,2,"host",1,&s)==0);
    assert(s.iterations==2 && s.successful_runs==2 && s.failed_runs==0);
    assert(fabsf(s.mean_total_ms-2.0f)<0.00001f);
    assert(fabsf(s.stddev_total_ms-sqrtf(1.125f))<0.00001f);
    assert(csv_count==2 && ids[0]==1 && ids[1]==2);
    reset();scenario[0]=1;scenario[2]=2;
    assert(benchmark_run_campaign(MODE_HYBRID,4,"host",1,&s)==-1);
    assert(s.iterations==4 && s.successful_runs==2 && s.failed_runs==2);
    assert(fabsf(s.mean_total_ms-2.75f)<0.00001f);
    assert(csv_count==2 && ids[0]==2 && ids[1]==4);
    reset();scenario[0]=3;scenario[1]=1;
    assert(benchmark_run_campaign(MODE_HYBRID,2,"host",1,&s)==-1);
    assert(s.successful_runs==0 && s.failed_runs==2 && csv_count==0);
    reset();assert(benchmark_run_campaign(MODE_HYBRID,0,"host",1,&s)==-1);
    reset();assert(benchmark_run_campaign(MODE_HYBRID,1,"host",1,&s)==0);
    assert(isnan(s.stddev_total_ms));
    assert(fabsf(cycles_to_ms(160000)-1.0f)<0.00001f);
    puts("PASS: benchmark host assertions (success, failure, IDs, sample SD, clock conversion).");
    return 0;
}
'''
    (out/'test.c').write_text(test,encoding='utf-8')
    binary=out/'benchmark-test'
    command=[args.compiler]
    if args.zig_linux:
        command += ['cc','-target','x86_64-linux-gnu']
    command += ['-std=c11','-O1','-UNDEBUG','-Wall','-Wextra','-I',str(out),'-I',str(ROOT/'firmware/main'),
                '-I',str(ROOT/'firmware/components/mlkem768/include'),'-include',str(out/'common.h'),
                '-include',str(out/'benchmark.h'),str(ROOT/'firmware/main/benchmark.c'),str(out/'test.c'),
                '-lm','-o',str(binary)]
    subprocess.run(command,check=True)
    if not args.compile_only:
        subprocess.run([str(binary)],check=True)
    print('Compiled benchmark host test:',binary)


if __name__=='__main__':
    main()

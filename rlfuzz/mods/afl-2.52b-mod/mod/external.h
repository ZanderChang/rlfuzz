/*
 * This has to do with external fuzzer link
 *
 */
#ifndef _HAVE_EXTERNAL_H
#define _HAVE_EXTERNAL_H

#include "types.h"
#include "config.h"

// 最大输入文件大小
#define MAX_INPUT_SIZE (1 << 16) // 64KB

#define SEM_PING_SIGNAL_NAME_HEAD "/afl-ping-signal"
#define SEM_PONG_SIGNAL_NAME_HEAD "/afl-pong-signal"
#define SHARED_MEM_NAME_HEAD "/afl-shared-mem"

u8 *SEM_PING_SIGNAL_NAME;
u8 *SEM_PONG_SIGNAL_NAME;
u8 *SHARED_MEM_NAME;

#pragma pack(1)
typedef struct ping_msg_hdr
{
    u32 msgid;
    u32 inputsize;
} PING_MSG_HDR;

typedef struct pong_msg
{
    u32 msgid;
    u32 status;
    u8 trace_bits[MAP_SIZE]; // 1 << 16
} PONG_MSG;

#pragma pack()

#define SHM_SIZE MAX(sizeof(PONG_MSG), MAX_INPUT_SIZE + sizeof(PING_MSG_HDR))

// defines for pong_msg_hdr->status
#define STATUS_CRASHED 0x80000000
#define STATUS_HANGED 0x40000000
#define STATUS_ERROR 0x20000000
#define STATUS_OK 0

#endif

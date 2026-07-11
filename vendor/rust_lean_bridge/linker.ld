ENTRY(_start)

SECTIONS {
    . = 1M;

    .text : ALIGN(4K) {
        KEEP(*(.text._start))
        *(.text .text.*)
        . = ALIGN(4K);
    }

    .rodata : ALIGN(4K) {
        *(.rodata .rodata.*)
        *(.data .data.*)
        *(.data.rel.ro .data.rel.ro.*)
        . = ALIGN(4K);
    }

    .bss (NOLOAD) : ALIGN(4K) {
        *(.bss .bss.*)
        *(COMMON)
        . = ALIGN(4K);
    }

    /DISCARD/ : {
        *(.eh_frame)
        *(.eh_frame_hdr)
        *(.got .got.*)
        *(.comment)
    }
}